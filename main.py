from xmlrpc.client import ServerProxy
import frontmatter
import time
import os
from hashlib import sha1
import json
import re
import urllib.parse
import logging
from datetime import datetime

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('typecho_sync.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config():
    """读取配置文件"""
    config_file_txt = ""
    if os.path.exists(os.path.join(os.getcwd(), "diy_config.txt")):
        config_file_txt = os.path.join(os.getcwd(), "diy_config.txt")
    else:
        config_file_txt = os.path.join(os.getcwd(), "config.txt")

    try:
        with open(config_file_txt, 'rb') as f:
            config_info = json.loads(f.read())
            return config_info
    except Exception as e:
        logger.error(f"读取配置文件失败: {str(e)}")
        raise

class TypechoClient:
    def __init__(self, xmlrpc_url, username, password):
        self.server = ServerProxy(xmlrpc_url)
        self.username = username
        self.password = password
        self.blogid = 1  # Typecho默认blogid为1
        self.current_file_name = None

    def get_posts(self):
        """获取已发布文章列表"""
        try:
            posts = self.server.metaWeblog.getRecentPosts(
                self.blogid, 
                self.username, 
                self.password, 
                1000  # 获取最近1000篇文章
            )
            # 添加日志来查看实际的链接格式
            if posts:
                logger.info(f"Sample post link: {posts[0].get('link', '')}")
            return [{"id": post["postid"], "link": post.get("link", "")} for post in posts]
        except Exception as e:
            logger.error(f"获取文章列表失败: {str(e)}")
            raise

    def _build_custom_fields(self, metadata):
        """构建文章自定义字段，只返回有值的字段"""
        custom_fields = []
        
        # 处理所有可能的自定义字段
        str_fields = ['postType', 'description', 'location', 'thumbnail']
        for key in str_fields:
            value = metadata.get(key, '').strip()
            if value:  # 只添加有值的字段
                custom_fields.append({
                    "key": key,
                    "value": value
                })

        logger.info(f"生成的 custom_fields:{custom_fields}")   
             
        # 处理 keywords 数组
        keywords = metadata.get('keywords', [])
        if keywords:
            custom_fields.append({
                "key": "keywords",
                "value": ",".join(map(str, keywords))
            })
        
        # 如果没有任何自定义字段，返回 None
        return custom_fields or None

    def new_post(self, title, content, categories, tags, metadata, publish=True):
        """发布新文章"""
        try:    
            # 添加 markdown 标记
            marked_content = "<!--markdown-->" + content
            
            post = {
                "title": title,
                "description": marked_content,
                "categories": categories,
                "mt_keywords": ",".join(tags) if tags else "",
                "post_type": metadata.get('postType', 'post'),
                "post_status": "publish" if publish else "draft",
                "wp_slug": self.current_file_name
            }
            
            # 只有在有自定义字段时才添加
            custom_fields = self._build_custom_fields(metadata)
            if custom_fields:
                post["custom_fields"] = custom_fields
            
            post_id = self.server.metaWeblog.newPost(
                self.blogid,
                self.username,
                self.password,
                post,
                publish
            )
            return post_id
        except Exception as e:
            logger.error(f"发布文章失败: {str(e)}")
            raise

    def edit_post(self, post_id, title, content, categories, tags, metadata, publish=True):
        """更新文章"""
        try:                
            # 添加 markdown 标记
            marked_content = "<!--markdown-->" + content
            
            post = {
                "title": title,
                "description": marked_content,
                "categories": categories,
                "mt_keywords": ",".join(tags) if tags else "",
                "post_type": metadata.get('postType', 'post'),
                "post_status": "publish" if publish else "draft"
            }
            
            # 只有在有自定义字段时才添加
            custom_fields = self._build_custom_fields(metadata)
            if custom_fields:
                post["custom_fields"] = custom_fields
            
            result = self.server.metaWeblog.editPost(
                post_id,
                self.username,
                self.password,
                post,
                publish
            )
            return result
        except Exception as e:
            logger.error(f"更新文章失败: {str(e)}")
            raise

def init_typecho_client():
    """初始化Typecho客户端"""
    try:
        # 优先使用环境变量
        username = os.environ.get("USERNAME")
        password = os.environ.get("PASSWORD")
        xmlrpc_php = os.environ.get("XMLRPC_PHP")

        if not all([username, password, xmlrpc_php]):
            # 如果环境变量不存在，尝试从配置文件读取
            config_info = load_config()
            username = config_info.get("USERNAME")
            password = config_info.get("PASSWORD")
            xmlrpc_php = config_info.get("XMLRPC_PHP")

        if not all([username, password, xmlrpc_php]):
            raise ValueError("缺少必要的配置信息")

        # 从 XMLRPC_PHP 中提取域名
        domain = re.match(r'https?://([^/]+)', xmlrpc_php).group(1)

        return TypechoClient(xmlrpc_php, username, password), domain

    except Exception as e:
        logger.error(f"初始化客户端失败: {str(e)}")
        raise

def get_md_list(dir_path):
    """获取目录下的markdown文件列表"""
    try:
        md_list = []
        dirs = os.listdir(dir_path)
        for i in dirs:
            if os.path.splitext(i)[1] == ".md":
                md_list.append(os.path.join(dir_path, i))
        logger.info(f"找到 {len(md_list)} 个Markdown文件")
        return md_list
    except Exception as e:
        logger.error(f"获取Markdown文件列表失败: {str(e)}")
        raise

def read_md(file_path):
    """读取Markdown文件内容和元信息"""
    try:
        with open(file_path, encoding='utf-8') as f:
            post = frontmatter.load(f)
            metadata = post.metadata
            
            # 处理基础字段，确保字符串类型
            metadata['title'] = str(metadata.get('title', '')).strip() or "未命名文章"
            metadata['description'] = str(metadata.get('description', '')).strip()
            metadata['location'] = str(metadata.get('location', '')).strip()
            metadata['thumbnail'] = str(metadata.get('thumbnail', '')).strip()
            
            # 处理数组类字段
            try:
                metadata['categories'] = list(metadata.get('categories', []))
            except:
                metadata['categories'] = []
                
            try:
                metadata['tags'] = list(metadata.get('tags', []))
            except:
                metadata['tags'] = []
                
            try:
                metadata['keywords'] = list(metadata.get('keywords', []))
            except:
                metadata['keywords'] = []
            
            # 处理 postType
            post_type = str(metadata.get('postType', '')).strip().lower()
            metadata['postType'] = 'shuoshuo' if post_type == 'shuoshuo' else 'post'
            
            return post.content, metadata
    except Exception as e:
        logger.error(f"读取Markdown文件失败 {file_path}: {str(e)}")
        raise

def get_sha1(filename):
    """计算文件的SHA1值"""
    try:
        sha1_obj = sha1()
        with open(filename, 'rb') as f:
            sha1_obj.update(f.read())
        result = sha1_obj.hexdigest()
        return result
    except Exception as e:
        logger.error(f"计算文件SHA1失败 {filename}: {str(e)}")
        raise

def get_md_sha1_dic(file):
    """获取或创建SHA1字典"""
    try:
        if os.path.exists(file):
            return read_dic_from_file(file)
        else:
            write_dic_info_to_file({}, file)
            return {}
    except Exception as e:
        logger.error(f"获取SHA1字典失败: {str(e)}")
        raise

def write_dic_info_to_file(dic_info, file):
    """将字典信息写入文件"""
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(dic_info, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"写入文件失败 {file}: {str(e)}")
        raise

def read_dic_from_file(file):
    """从文件读取字典信息"""
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"读取文件失败 {file}: {str(e)}")
        raise

def rebuild_md_sha1_dic(file, md_dir):
    """重建SHA1字典"""
    try:
        md_sha1_dic = {}
        md_list = get_md_list(md_dir)

        for md in md_list:
            key = os.path.basename(md).split(".")[0]
            value = get_sha1(md)
            md_sha1_dic[key] = {
                "hash_value": value,
                "file_name": key,
                "encode_file_name": urllib.parse.quote(key, safe='').lower()
            }

        md_sha1_dic["update_time"] = time.strftime('%Y-%m-%d-%H-%M-%S')
        write_dic_info_to_file(md_sha1_dic, file)
        logger.info("重建SHA1字典成功")
    except Exception as e:
        logger.error(f"重建SHA1字典失败: {str(e)}")
        raise

def insert_index_info_in_readme(domain_name):
    """更新README.md的文章目录"""
    try:
        md_list = get_md_list(os.path.join(os.getcwd(), "_posts"))
        insert_info = ""
        md_list.sort(reverse=True)

        for md in md_list:
            content, metadata = read_md(md)
            title = metadata.get("title", "")
            if title:
                file_name = os.path.basename(md).split('.')[0]
                post_url = f"https://{domain_name}/index.php/p/{file_name}.html"
                insert_info += f"[{title}]({post_url})\n\n"

        insert_info = f"---start---\n## 目录({time.strftime('%Y年%m月%d日')}更新)\n{insert_info}---end---"

        readme_path = os.path.join(os.getcwd(), "README.md")
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_md_content = f.read()

        new_readme_md_content = re.sub(r'---start---(.|\n)*---end---', insert_info, readme_md_content)

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_readme_md_content)

        logger.info("更新README.md成功")
        return True
    except Exception as e:
        logger.error(f"更新README.md失败: {str(e)}")
        raise

def main():
    try:
        # 初始化Typecho客户端
        client, domain_name = init_typecho_client()
        
        # 1. 获取网站数据库中已有的文章列表
        post_link_id_list = client.get_posts()
        link_id_dic = {post["link"]: post["id"] for post in post_link_id_list}
        
        # 2. 获取md_sha1_dic
        md_sha1_dic = get_md_sha1_dic(os.path.join(os.getcwd(), ".md_sha1"))
        
        # 3. 开始同步
        md_list = get_md_list(os.path.join(os.getcwd(), "_posts"))

        for md in md_list:
            sha1_key = os.path.basename(md).split(".")[0]
            sha1_value = get_sha1(md)
            
            # 检查文件是否需要更新
            if (sha1_key in md_sha1_dic and 
                "hash_value" in md_sha1_dic[sha1_key] and 
                sha1_value == md_sha1_dic[sha1_key]["hash_value"]):
                logger.info(f"{md} 无需同步")
                continue
            
            logger.info(f"开始同步 {md}")
            content, metadata = read_md(md)
            
            title = metadata.get('title', '未命名文章')
            categories = metadata.get('categories', [])
            tags = metadata.get('tags', [])
            link = f"https://{domain_name}/index.php/p/{sha1_key}.html"
            
            if link not in link_id_dic:
                # 发布新文章
                client.current_file_name = sha1_key
                client.new_post(
                    title=title,
                    content=content,
                    categories=categories,
                    tags=tags,
                    metadata=metadata
                )
                logger.info(f"创建新文章成功: {link}")
            else:
                # 更新已有文章
                client.edit_post(
                    post_id=link_id_dic[link],
                    title=title,
                    content=content,
                    categories=categories,
                    tags=tags,
                    metadata=metadata
                )
                logger.info(f"更新文章成功: {link}")

        # 4. 重建md_sha1_dic
        rebuild_md_sha1_dic(
            os.path.join(os.getcwd(), ".md_sha1"),
            os.path.join(os.getcwd(), "_posts")
        )
        
        # 5. 更新README.md
        insert_index_info_in_readme(domain_name)
        
        logger.info("同步完成")
        
    except Exception as e:
        logger.error(f"同步过程发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    main()