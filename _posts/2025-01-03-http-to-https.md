---
title: 如何把自己的网站从http变成https，设置https证书自动更新
categories: [教学]
tags: [http,https]
---

# 手把手教会你如何把自己的网站从`http`变成`https` | 设置`https`证书自动更新，保姆级教学

## 0.前言

搭建了一个自己的博客|官网|或者其他，开开心心的发给朋友，结果朋友来了一句：”你这个网站浏览器阻止我访问啊“，瞬间心情跌落谷底。**感觉自己像是写了一个成人网站都不如的项目**，心里暗暗发誓，我一定要把`http`变成`https`！



## 1.准备demo

1. 准备项目

   准备一个`Nextjs`项目，制作了一个`docker`镜像放到自己的服务器上跑起来试试，设置的端口是`8080`，现在已经能通过端口访问了。

   ![docker][docker1]

   `Docker`教程：[点击这里](https://blog.xukucha.cn/article-detail/lglxvk879bewhxqmz9yg8dms)

2. 准备域名

   以我自己的域名`api.xukucha.cn`为例，下面用的都是这个子域名。

   

## 2.安装&配置`Nginx`

1. 安装`Nginx`

   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. 创建`Nginx`配置文件

   ```bash
   sudo nano /etc/nginx/sites-available/api.xukucha.cn
   ```

3. 写入配置
   ```nginx
   server {
       listen 80;
       server_name api.xukucha.cn;
   
       location / {
           proxy_pass http://localhost:3000;  # Next.js默认运行在3000端口
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
           
           # 跨域（如果需要）
           add_header 'Access-Control-Allow-Origin' '*';
           add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
           add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
       }
   }
   ```

4. 创建软链接启用站点
   ```bash
   sudo ln -s /etc/nginx/sites-available/api.xukucha.cn /etc/nginx/sites-enabled/
   ```

5. 测试`Nginx`配置
   ```bash
   sudo nginx -t
   ```

   ![nginx][nginx1]

6. 重启`Nginx`

   ```bash
   sudo systemctl restart nginx
   ```

7. 测试访问子域名

   ![subdomain][subdomain1]



## 4.安装`acme.sh`

1. 安装`acme.sh`

   ```bash
   # 替换成你自己的邮箱
   curl https://get.acme.sh | sh -s email=hansxu27@gmail.com
   ```

   ![acme.sh][acme.sh1]

2. 添加 `acme.sh` 到当前 shell 环境

   ```bash
   source ~/.bashrc
   ```

3. 验证安装是否成功

   ```bash
   acme.sh --version
   ```

   ![acme.sh][acme.sh2]

4. 更新到最新版本

   ```bash
   acme.sh --upgrade
   ```

5. 设置默认 CA 为 Let's Encrypt

   ```bash
   acme.sh --set-default-ca --server letsencrypt
   ```

   ![acme.sh][acme.sh3]



## 5.申请证书

使用`Nginx`模式申请证书

这里还能使用其他模式，我选择`Nginx`模式，因为要调整的东西比较少，简化了过程。

我把所有的子域名一起处理了`blog.xukucha.cn`,`admin.xukucha.cn`,`api.xukucha.cn`,`www.xukucha.cn`,`xukucha.cn`，

```bash
# 加入了 --force 是因为我之前已经申请过了，为了确保能进行下去所以加 --foce
~/.acme.sh/acme.sh --issue -d xukucha.cn -d www.xukucha.cn -d api.xukucha.cn -d admin.xukucha.cn -d blog.xukucha.cn --nginx --force
```

注意这里容易出错，如果出错了（我就出错了。。。），那就一个个单独处理。
以`api.xukucha.cn`为例

```bash
# 加了参数 --force 是因为我刚刚操作过一次了，不加 --force 后面没办法进行
~/.acme.sh/acme.sh --issue -d api.xukucha.cn --nginx --force
```

![acme.sh][acme.sh4]



## 6.拷贝证书

成功以后需要执行这个拷贝命令，这个命令的作用是将`acme.sh` 生成的证书复制到 `Nginx `可以读取的位置，并在证书更新时自动重新加载 `Nginx`。

**如果你不执行这一步，证书更新后，`Nginx` 不会自动重新加载。这意味着即使证书已更新，`Nginx `可能仍在使用旧证书，直到下次手动重启或重载。**

```bash
# 创建一个文件夹用来放证书，确保这个文件夹有读写的权限
sudo mkdir -p /etc/nginx/ssl/api.xukucha.cn/
```

```bash
# 拷贝的路径待会要添加到nginx配置中（第7步）
acme.sh --install-cert -d api.xukucha.cn \
--key-file       /etc/nginx/ssl/api.xukucha.cn/api.xukucha.cn.key  \
--fullchain-file /etc/nginx/ssl/api.xukucha.cn/fullchain.cer \
--reloadcmd     "service nginx force-reload"
```



## 7.再次配置`Nginx`

再次编辑对应的`Nginx`配置文件

```bash
sudo nano /etc/nginx/sites-enabled/api.xukucha.cn
```

添加完整的`https`配置：

```nginx
# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name api.xukucha.cn;
    return 301 https://$server_name$request_uri;
}

# HTTPS 配置
server {
    listen 443 ssl;
    server_name api.xukucha.cn;

    # SSL 证书配置（使用第6步创建的路径）
    ssl_certificate /etc/nginx/ssl/api.xukucha.cn/fullchain.cer;
    ssl_certificate_key /etc/nginx/ssl/api.xukucha.cn/api.xukucha.cn.key;

    # SSL 增强安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

测试并重启`Nginx`

```bash
# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

访问`https://api.xukucha.cn/`，成功咯！
![acme.sh][acme.sh5]

剩下的几个域名重复这一步的操作就行了。



## 8.感谢

感谢现在的领导&前辈 [zhaoolee](https://github.com/zhaoolee) ，这个教程也是跟着他的文档一步一步学会然后自己实操的，能和他共事我觉得很开心。









[docker1]:https://image.xukucha.cn/blog/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20250103110440.png
[nginx1]:https://image.xukucha.cn/blog/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20250103120627.png
[subdomain1]:https://image.xukucha.cn/blog/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20250103121526.png
[acme.sh1]:https://image.xukucha.cn/blog/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20250103140649.png
[acme.sh2]:https://image.xukucha.cn/blog/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20250103140833.png
[acme.sh3]:https://image.xukucha.cn/blog/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20250103142050.png
[acme.sh4]:https://image.xukucha.cn/blog/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20250103181903.png
[acme.sh5]:https://image.xukucha.cn/blog/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20250103182147.png
