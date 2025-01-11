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
            return json.loads(f.read())
    except Exception as e:
        logger.error(f"读取配置文件失败: {str(e)}")
        raise

class TypechoClient:
    def __init__(self, xmlrpc_url, username, password):
        self.server = ServerProxy(xmlrpc_url)
        self.username = username
        self.password = password
        self.blogid = 1
        self.current_file_name = None

    def get_posts(self):
        """获取已发布文章列表"""
        try:
            posts = self.server.metaWeblog.getRecentPosts(
                self.blogid, 
                self.username, 
                self.password, 
                1000
            )
            return [{"id": post["postid"], "link": post.get("link", "")} for post in posts]
        except Exception as e:
            logger.error(f"获取文章列表失败: {str(e)}")
            raise

    def _build_post_data(self, title, content, categories, tags, publish=True):
        """构建文章数据，用于新建和编辑文章"""
        post = {
            "title": title,
            "description": "<!--markdown-->" + content,
            "categories": categories,
            "mt_keywords": ",".join(tags) if tags else "",
            "post_type": "post",
            "post_status": "publish" if publish else "draft",
            "markdown": 1
        }

        if self.current_file_name:
            post["wp_slug"] = self.current_file_name
                
        return post

    def new_post(self, title, content, categories, tags, publish=True):
        """发布新文章"""
        try:
            post = self._build_post_data(title, content, categories, tags, publish)
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

    def edit_post(self, post_id, title, content, categories, tags, publish=True):
        """更新文章"""
        try:
            post = self._build_post_data(title, content, categories, tags, publish)
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
        username = os.environ.get("USERNAME") or load_config().get("USERNAME")
        password = os.environ.get("PASSWORD") or load_config().get("PASSWORD")
        xmlrpc_php = os.environ.get("XMLRPC_PHP") or load_config().get("XMLRPC_PHP")

        if not all([username, password, xmlrpc_php]):
            raise ValueError("缺少必要的配置信息")

        domain = re.match(r'https?://([^/]+)', xmlrpc_php).group(1)
        return TypechoClient(xmlrpc_php, username, password), domain
    except Exception as e:
        logger.error(f"初始化客户端失败: {str(e)}")
        raise

def get_md_list(dir_path):
    """获取目录下的markdown文件列表"""
    try:
        return [os.path.join(dir_path, f) for f in os.listdir(dir_path) 
                if f.endswith('.md')]
    except Exception as e:
        logger.error(f"获取Markdown文件列表失败: {str(e)}")
        raise

def read_md(file_path):
    """读取Markdown文件内容和元信息"""
    try:
        with open(file_path, encoding='utf-8') as f:
            post = frontmatter.load(f)
            metadata = post.metadata
            
            # 只处理必要的字段
            title = str(metadata.get('title', '')).strip() or "未命名文章"
            
            # 处理分类
            categories = metadata.get('categories', [])
            if isinstance(categories, str):
                categories = [x.strip() for x in categories.split(',') if x.strip()]
            
            # 处理标签
            tags = metadata.get('tags', [])
            if isinstance(tags, str):
                tags = [x.strip() for x in tags.split(',') if x.strip()]
            
            return post.content, title, categories, tags
    except Exception as e:
        logger.error(f"读取Markdown文件失败 {file_path}: {str(e)}")
        raise

def get_sha1(filename):
    """计算文件的SHA1值"""
    try:
        sha1_obj = sha1()
        with open(filename, 'rb') as f:
            sha1_obj.update(f.read())
        return sha1_obj.hexdigest()
    except Exception as e:
        logger.error(f"计算文件SHA1失败 {filename}: {str(e)}")
        raise

def get_md_sha1_dic(file):
    """获取或创建SHA1字典"""
    try:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            with open(file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            return {}
    except Exception as e:
        logger.error(f"获取SHA1字典失败: {str(e)}")
        raise

def rebuild_md_sha1_dic(file, md_dir):
    """重建SHA1字典"""
    try:
        md_sha1_dic = {}
        for md in get_md_list(md_dir):
            key = os.path.basename(md).split(".")[0]
            md_sha1_dic[key] = {
                "hash_value": get_sha1(md),
                "file_name": key,
                "encode_file_name": urllib.parse.quote(key, safe='').lower()
            }

        md_sha1_dic["update_time"] = time.strftime('%Y-%m-%d-%H-%M-%S')
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(md_sha1_dic, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"重建SHA1字典失败: {str(e)}")
        raise

def insert_index_info_in_readme(domain_name):
    """更新README.md的文章目录"""
    try:
        md_list = get_md_list(os.path.join(os.getcwd(), "_posts"))
        insert_info = []
        md_list.sort(reverse=True)

        for md in md_list:
            content, title, _, _ = read_md(md)
            if title:
                file_name = os.path.basename(md).split('.')[0]
                post_url = f"https://{domain_name}/index.php/p/{file_name}.html"
                insert_info.append(f"[{title}]({post_url})\n\n")

        insert_text = f"---start---\n## 目录({time.strftime('%Y年%m月%d日')}更新)\n{''.join(insert_info)}---end---"

        readme_path = os.path.join(os.getcwd(), "README.md")
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(re.sub(r'---start---(.|\n)*---end---', insert_text, content))

    except Exception as e:
        logger.error(f"更新README.md失败: {str(e)}")
        raise

def main():
    try:
        client, domain_name = init_typecho_client()
        post_link_id_list = client.get_posts()
        link_id_dic = {post["link"]: post["id"] for post in post_link_id_list}
        
        md_sha1_dic = get_md_sha1_dic(os.path.join(os.getcwd(), ".md_sha1"))
        md_list = get_md_list(os.path.join(os.getcwd(), "_posts"))

        for md in md_list:
            sha1_key = os.path.basename(md).split(".")[0]
            sha1_value = get_sha1(md)
            
            if (sha1_key in md_sha1_dic and 
                sha1_value == md_sha1_dic[sha1_key].get("hash_value")):
                continue
            
            content, title, categories, tags = read_md(md)
            link = f"https://{domain_name}/index.php/p/{sha1_key}.html"
            
            if link not in link_id_dic:
                client.current_file_name = sha1_key
                client.new_post(title, content, categories, tags)
            else:
                client.edit_post(link_id_dic[link], title, content, categories, tags)

        rebuild_md_sha1_dic(
            os.path.join(os.getcwd(), ".md_sha1"),
            os.path.join(os.getcwd(), "_posts")
        )
        
        insert_index_info_in_readme(domain_name)
        logger.info("同步完成")
        
    except Exception as e:
        logger.error(f"同步过程发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    main()