---
title: 使用 Strapi + Docker + Nginx 部署个人博客后台
categories: [建站相关]
tags: [Docker,Strapi,Nginx]
---

# 使用 Strapi + Docker + Nginx 部署个人博客后台

本教程介绍如何在云服务器上部署 Strapi 博客后台系统，实现：

- 使用 Docker 容器化部署 Strapi 应用
- Nginx 反向代理和多域名配置
- SSL 证书自动申请和更新
- MySQL 远程连接配置
- 全站 HTTPS 安全访问

## 1. 环境准备

### 1.1 更新系统并安装基础工具

```bash
# 更新包管理器
sudo apt update && sudo apt upgrade -y

# 安装必要的工具
sudo apt install -y curl git build-essential
```

### 1.2 安装 Node.js (推荐使用 nvm 管理)

```bash
# 安装 nvm 
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 重新加载配置
source ~/.bashrc

# 安装 Node.js LTS 版本
nvm install --lts
nvm use --lts

# 验证安装
node --version
npm --version
```

### 1.3 安装和配置 MySQL

```bash
# 安装 MySQL
sudo apt install -y mysql-server

# 启动 MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# 配置 MySQL 安全性
sudo mysql_secure_installation

# 登录 MySQL 创建数据库和用户
sudo mysql

# 创建数据库
CREATE DATABASE strapi_blog;

# 创建用户并允许远程访问
# 注意：在生产环境中应该限制允许访问的 IP 地址
# 这里用 '%' 而不是 'localhost' 以允许远程连接

# 本来是 GRANT ALL PRIVILEGES ON strapi_blog.* TO 'strapi_user'@'localhost';
# 	    CREATE USER 'strapi_user'@'localhost' IDENTIFIED BY 'password';

CREATE USER 'strapi_user'@'%' IDENTIFIED BY 'password';  
GRANT ALL PRIVILEGES ON strapi_blog.* TO 'strapi_user'@'%';
FLUSH PRIVILEGES;
EXIT;
```

### 1.4 配置 MySQL 远程访问

```bash
# 编辑 MySQL 配置文件
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# 修改绑定地址
bind-address = 0.0.0.0
mysqlx-bind-address = 0.0.0.0

# 重启 MySQL
sudo systemctl restart mysql

# 验证 MySQL 是否监听所有地址：
sudo netstat -tlnp | grep mysql

# 安装防火墙
sudo apt install -y ufw

# 配置防火墙
sudo ufw allow 3306/tcp

# 注意：记得在云服务器控制台开放 3306 端口
# 建议：限制允许访问的 IP 地址，提高安全性
```

## 2. Strapi 本地开发配置

### 2.1 创建 Strapi 项目

```bash
npx create-strapi-app@latest my-blog

# 选择 Custom 安装以配置远程数据库
# 选择 MySQL 数据库
# 填写远程数据库连接信息
```

### 2.2 Docker 配置

创建 Dockerfile：

```dockerfile
FROM node:18-alpine

# 安装必要的系统依赖
RUN apk update && \
    apk add --no-cache build-base gcc autoconf automake zlib-dev libpng-dev vips-dev python3

# 设置工作目录
WORKDIR /opt/app

# 复制项目文件
COPY package*.json ./
RUN npm install
COPY . .

# 构建应用
RUN npm run build

EXPOSE 1337
CMD ["npm", "run", "start"]
```

## 3. 服务器部署

### 3.1 安装 Docker

```bash
# 移除旧版本 
sudo apt remove docker-compose docker.io -y
sudo apt autoremove -y

# 安装新版本
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

### 3.2 使用阿里云容器镜像服务

```bash
# 本地登录阿里云容器镜像服务
docker login --username=your_username your_registry_url

# 构建镜像
docker build -t strapi-blog-admin:v1 .

# 打标签
docker tag strapi-blog-admin:v1 your_registry_url/your_namespace/strapi-blog-admin:v1

# 推送镜像
docker push your_registry_url/your_namespace/strapi-blog-admin:v1

# 服务器上拉取和运行
docker pull your_registry_url/your_namespace/strapi-blog-admin:v1
docker run -d -p 1337:1337 --name strapi-blog your_registry_url/your_namespace/strapi-blog-admin:v1
```

### 3.3 Nginx 配置

```bash
# 安装 Nginx
sudo apt install nginx

# 创建配置文件
sudo nano /etc/nginx/sites-available/admin.xukucha.cn

# admin.xukucha.cn 的 Nginx 配置：
server {
    listen 80;
    server_name admin.xukucha.cn;

    location /.well-known/acme-challenge/ {
        root /var/www/ssl_verify;
    }

    location / {
        proxy_pass http://localhost:1337;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# 主域名的 Nginx 配置：
server {
    listen 80;
    server_name xukucha.cn www.xukucha.cn;

    location /.well-known/acme-challenge/ {
        root /var/www/ssl_verify;
    }

    location / {
        return 301 https://blog.xukucha.cn$request_uri;
    }
}

# 创建软链接并重启 Nginx
sudo ln -s /etc/nginx/sites-available/admin.xukucha.cn /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/xukucha-main /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3.4 SSL 证书配置

```bash
# 安装 acme.sh
curl https://get.acme.sh | sh -s email=your_email@example.com

# 创建验证目录
sudo mkdir -p /var/www/ssl_verify
sudo chown -R www-data:www-data /var/www/ssl_verify
sudo chmod -R 755 /var/www/ssl_verify

# 为所有域名申请证书
~/.acme.sh/acme.sh --issue -d xukucha.cn -d www.xukucha.cn -d admin.xukucha.cn -w /var/www/ssl_verify

# 创建存放证书的目录
sudo mkdir -p /etc/nginx/ssl

# 安装证书
~/.acme.sh/acme.sh --install-cert -d xukucha.cn \
--key-file       /etc/nginx/ssl/xukucha.cn.key  \
--fullchain-file /etc/nginx/ssl/fullchain.cer \
--reloadcmd     "sudo systemctl reload nginx"
```

### 3.5 配置 HTTPS：

```nginx
# 主域名的HTTPS配置
server {
    listen 80;
    server_name xukucha.cn www.xukucha.cn;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name xukucha.cn www.xukucha.cn;

    ssl_certificate /etc/nginx/ssl/fullchain.cer;
    ssl_certificate_key /etc/nginx/ssl/xukucha.cn.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;

    location /.well-known/acme-challenge/ {
        root /var/www/ssl_verify;
    }

    location / {
        return 301 https://blog.xukucha.cn$request_uri;
    }
}
```

```nginx
# 后台项目的HTTPS配置
server {
    listen 80;
    server_name admin.xukucha.cn;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name admin.xukucha.cn;

    ssl_certificate /etc/nginx/ssl/fullchain.cer;
    ssl_certificate_key /etc/nginx/ssl/xukucha.cn.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;

    location /.well-known/acme-challenge/ {
        root /var/www/ssl_verify;
    }

    location / {
        proxy_pass http://localhost:1337;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 重启Nginx
sudo nginx -t
sudo systemctl restart nginx

# 开放必要端口
# 在 UFW 防火墙中开放端口
sudo ufw allow 80
sudo ufw allow 443

# 记得在阿里云控制台的安全组中也要开放这些端口
```

## 4. 维护指南

### 4.1 更新 Strapi

1. 构建新版本 Docker 镜像
2. 推送到镜像仓库
3. 在服务器上拉取新镜像并重启容器

### 4.2 数据备份

1. 定期备份 MySQL 数据库
2. 备份 Strapi 上传的文件
3. 备份 Nginx 和 SSL 配置

### 4.3 证书续期

acme.sh 会自动创建定时任务，每天检查证书是否需要更新。可以手动检查：

```bash
~/.acme.sh/acme.sh --cron
```

## 5. 故障排查

### 5.1 Docker 相关

- 检查容器状态：`docker ps -a`
- 查看容器日志：`docker logs strapi-blog`
- 检查镜像拉取：`docker pull --verbose`

### 5.2 Nginx 相关

- 检查配置：`nginx -t`
- 查看错误日志：`tail -f /var/log/nginx/error.log`
- 检查访问日志：`tail -f /var/log/nginx/access.log`

### 5.3 SSL 相关

- 检查证书状态：`~/.acme.sh/acme.sh --list`
- 强制更新证书：`~/.acme.sh/acme.sh --renew -d your_domain.com --force`
- 查看证书信息：`openssl x509 -in /etc/nginx/ssl/fullchain.cer -text -noout`

## 安全建议

1. 限制 MySQL 远程访问的 IP 地址
2. 使用强密码并定期更换
3. 及时更新系统和依赖包
4. 配置防火墙，只开放必要端口
5. 定期检查系统和应用日志
6. 备份重要数据和配置文件
