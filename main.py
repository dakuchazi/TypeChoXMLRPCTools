from xmlrpc.client import ServerProxy
import frontmatter
import time
import os
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

    def get_posts(self):
        """获取已发布文章列表"""
        try:
            posts = self.server.metaWeblog.getRecentPosts(
                self.blogid, 
                self.username, 
                self.password, 
                1000  # 获取最近1000篇文章
            )
            return [{"id": post["postid"], "link": post.get("link", "")} for post in posts]
        except Exception as e:
            logger.error(f"获取文章列表失败: {str(e)}")
            raise

    def new_post(self, title, content, categories, tags, publish=True):
        """发布新文章"""
        try:
            post = {
                "title": title,
                "description": content,
                "categories": categories,
                "mt_keywords": ",".join(tags) if tags else "",
                "post_type": "post",
                "post_status": "publish" if publish else "draft"
            }
            
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
            post = {
                "title": title,
                "description": content,
                "categories": categories,
                "mt_keywords": ",".join(tags) if tags else "",
                "post_type": "post",
                "post_status": "publish" if publish else "draft"
            }
            
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
        # 例如从 https://tc.xukucha.cn/action/xmlrpc 提取 tc.xukucha.cn
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
            
            # 如果没有标题，设置为默认标题
            if not metadata.get('title'):
                metadata['title'] = "未命名文章"
                logger.warning(f"{file_path} 没有设置标题，使用默认标题: 未命名文章")
            
            return post.content, metadata
    except Exception as e:
        logger.error(f"读取Markdown文件失败 {file_path}: {str(e)}")
        raise

def main():
    try:
        # 初始化Typecho客户端
        client, domain = init_typecho_client()
        
        # 获取已发布文章列表
        posts = client.get_posts()
        post_dict = {post["link"]: post["id"] for post in posts}
        
        # 获取本地文章列表
        md_list = get_md_list(os.path.join(os.getcwd(), "_posts"))
        
        # 同步文章
        for md_file in md_list:
            try:
                content, metadata = read_md(md_file)
                
                title = metadata.get('title', '未命名文章')
                categories = metadata.get('categories', [])
                tags = metadata.get('tags', [])
                
                # 获取文章链接
                file_name = os.path.basename(md_file).split('.')[0]
                link = f"https://{domain}/index.php/p/{file_name}.html"  # 完整的文章链接
                
                if link in post_dict:
                    # 更新已存在的文章
                    client.edit_post(
                        post_dict[link],
                        title,
                        content,  # 直接使用Markdown内容
                        categories,
                        tags
                    )
                    logger.info(f"更新文章成功: {title}")
                else:
                    # 发布新文章
                    post_id = client.new_post(
                        title,
                        content,  # 直接使用Markdown内容
                        categories,
                        tags
                    )
                    logger.info(f"发布新文章成功: {title}")
                    
            except Exception as e:
                logger.error(f"处理文章 {md_file} 失败: {str(e)}")
                continue
        
        logger.info("同步完成")
        
    except Exception as e:
        logger.error(f"同步过程发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    main()