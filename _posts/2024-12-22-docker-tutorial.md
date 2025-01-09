---
title: 手把手教学，更适合前端宝宝的Docker教程
categories: [教学]
tags: [Docker,项目部署]
---

# 从安装到会用，更适合前端宝宝的Docker教程

以`Express`为例，手把手教学从本地开发到项目部署上线，**还学不会的我再想想办法**。

建议先**成功运行起来**，这一步我觉得很重要，通过一个非常简单的例子先开心一下，**如果没有成功就没有动力去了解为什么**。

最后再仔细看解释。

为什么选`Express`，几个文件就能搞定，按照下面的步骤来就可以了，而且API接口还能做实际测试，先从`Express`开始，学会了可以部署前端的`Vue`,`React`,`Next`等等。

## 0.前言

刚入门前端以及刚开始找工作的时候，时不时会刷到这样的招聘信息：

![](https://image.xukucha.cn/blog/lQDPJwyhGhzl7UHNBMnNAzyw9kRysqOiMWIHXYzVjDWzAA_828_1225.jpg)

刚入行：`Docker`又是什么东西，我刚学完那些东西怎么还要学？我他妈就是不想学了！

工作时：明明在我电脑上能跑起来，在你电脑上怎么就有bug？

两年后：啥也不说了，先打个`Docker`试一下。



对我而言，**`Docker`就是为了解决“在我这能行，在你那不行”的一个工具**，借用`Docker`官网的一句话就是：**Develop faster. Run anywhere.**



## 1.准备`demo`

本地先创建一个`Express`文件夹，名字就叫`docker-demo`

```bash
# 进入docker-demo执行：
npm install express
```

创建`app.js`文件

```js
const express = require('express');

const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.json({
    message: 'Hello Docker!',
    time: new Date().toISOString()
  });
});

app.listen(port, () => {
  console.log(`应用已启动，监听端口 ${port}`);
});
```

![](https://image.xukucha.cn/blog/20250104145434.png)

运行起来在本地测试：

```bash
node app.js
```

![](https://image.xukucha.cn/blog/20250104145558.png)

访问`https://localhost:3000`

![](https://image.xukucha.cn/blog/20250104145718.png)



## 2.下载安装`Docker Desktop`

[Docker官网](httpss://www.docker.com/)，你是什么系统就下载什么对应系统的就行了。

我已经安装过了，安装步骤省略，有什么疑难杂症请自行百度。

![](https://image.xukucha.cn/blog/20250104135219.png)



验证一下安装：

```bash
docker --version
docker-compose --version
```

![](https://image.xukucha.cn/blog/20250104141440.png)



点击桌面图标运行`Docker Desktop`：
![](https://image.xukucha.cn/blog/20250104141048.png)



## 4.配置镜像源

这里不得不解释一下了，因为我们从官方仓库里获取一些东西，由于国内网络可能会非常慢或者获取不到，这个时候就要设置一些镜像源才行。
**不理解的想一下`npm`镜像源应该马上就能理解了。**

![](https://image.xukucha.cn/blog/20250104151307.png)

去百度搜索一下“docker最新镜像”，复制粘贴几个替换一下就行了，代码格式如下：

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "features": {
    "buildkit": true
  },
  "registry-mirrors": [
    "httpss://hub.geekery.cn",
    "httpss://hub.littlediary.cn",
    "httpss://docker.rainbond.cc"
  ]
}
```



## 3.创建`Dockerfile`

什么是`Dockerfile`，它的作用就是告诉`Docker`要怎么去制作镜像，需要准备什么东西。（什么是镜像？第4步有说明）

在`docker-demo`项目根目录下创建一个`Dockerfile`文件：

做了一些很基础的解释，可以先看一下。

```dockerfile
# 使用 Node.js 18 作为基础镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json（如果存在）
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制所有源代码
COPY . .

# 应用将监听 3000 端口
EXPOSE 3000

# 启动应用
CMD ["node", "app.js"]
```

![](https://image.xukucha.cn/blog/20250104150506.png)



## 4.构建`Docker`镜像

这一步又不得不解释一下了：这是根据刚刚写的`Dockerfile`制作出来的镜像，也就是`Image`。

**Docker 镜像 (Image)就像是一个"模板"或者"快照"，它包含了运行应用所需的所有内容：代码、运行环境、依赖、配置等**

觉得很抽象的话，就把镜想象你现在编写好了一个App，现在要给这个App打包一下，制作成一个安装包。

```bash
# 在项目文件夹中执行下面的命令，docker-demo 可以替换成你喜欢的名字
# 注意 docker-demo 后面是空格 还有一个点
docker build -t docker-demo .
```

成功`build`：（如果出现了一些报错，那大概就是镜像源失效了，再去第四步换一些最新的镜像源）

![](https://image.xukucha.cn/blog/20250104152320.png)

在`Docker Desktop`可以看到：

![](https://image.xukucha.cn/blog/20250104152903.png)



## 5.运行容器

这一步又不得不解释一下了：

**Docker 容器 (Container)就是运行镜像的运行实例，专门用来运行Image的一个盒子，每个盒子之间相互独立互不影响**

觉得很抽象的话，就把容器理解为一个小小的、轻量的系统，现在要把你刚刚制作的App安装到这个系统中。

![](https://image.xukucha.cn/blog/20250104154255.png)

![](https://image.xukucha.cn/blog/image-20250104154317961.png)

![](https://image.xukucha.cn/blog/20250104154541.png)

![](https://image.xukucha.cn/blog/20250104155635.png)

![](https://image.xukucha.cn/blog/20250104155820.png)





## 6.一些基本的命令

在之前的操作中，我们基本上都是通过用鼠标点击`Docker Desktop`完成操作的，为了后续能够顺利进项下去，还需要掌握一些指令。

**镜像相关命令**：

```bash
# 列出本地所有镜像
docker images

# 构建镜像
# 如果不写tag就会给默认的latest
docker build -t [name]:[tag] .

# 删除镜像
docker rmi [image_id]

# 查看镜像详细信息
docker inspect [image_id]

# 使用镜像ID打标签
docker tag [image_id] [name]:[tag]

# 推送镜像
# docker push 用户名/仓库名:标签
docker push xxxx/xxxx/xxxx:[tag]
```

**容器相关命令**：

```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括已停止的）
docker ps -a

# 运行容器
# 如果不写 --name [container_name] 会给一个默认的容器名
# 如果不写 [image_tag] 会使用tag为latest的那个镜像
# 8080对应容器3000端口
docker run -d -p 8080:3000 --name [container_name] [image_name]:[image_tag]

# 停止容器
docker stop [container_id]

# 启动已停止的容器
docker start [container_id]

# 重启容器
docker restart [container_id]

# 删除容器
docker rm [container_id]
```

**清理命令：**

```bash
# 删除所有已停止的容器
docker container prune

# 删除所有未使用的镜像
docker image prune

# 删除所有未使用的资源
docker system prune
```



## 7.整理一下`Dockerfile`、镜像、容器之前的关系

```
# 1. 我们写一个 Dockerfile（一个清单，打包App需要哪些东西）
FROM node:18-alpine
WORKDIR /app
COPY . .
...

# 2. 使用 Dockerfile 去做一个App
docker build -t docker-demo .

# 3. 基于这个App给他准备了一个独立的盒子
docker run docker-demo

# 4. 可以同时拥有多个这样的盒子
docker run docker-demo  # 容器 1
docker run docker-demo  # 容器 2
```



## 8.准备镜像仓库

就像准备一个代码仓库一样，代码仓库是把你写好的代码提交到远程仓库，那么在`docker`中也是同样的道理，把你制作好的镜像提交到远程仓库。

随意选择一个厂商的镜像仓库，这里我选择的是[容器镜像服务 ACR](httpss://cn.aliyun.com/product/acr?from_alibabacloud=&channel=yy_yc)，有免费试用的，自己去处理一下，我用的就是免费的。

![](https://image.xukucha.cn/blog/20250104170705.png)

![](https://image.xukucha.cn/blog/20250104165908.png)

![](https://image.xukucha.cn/blog/20250104171206.png)

![](https://image.xukucha.cn/blog/20250104171305.png)

![](https://image.xukucha.cn/blog/20250104174348.png)



## 9.推送镜像到镜像仓库

根据阿里云的操作指南中的第三步来就行了，复制他的那些指令，替换一下参数就行了。

先登录：

```bash
docker login --username=yourname crpi-xxxxxxx.aliyuncs.com
```

![](https://image.xukucha.cn/blog/20250104171630.png)

然后给准备推送的镜像打上一个tag，这个名字虽然很长，但是不要去修改它，改一下tag就行了：

```bash
docker tag c3ee118a8f74 crpi-xxxxx.aliyuncs.com/xxxxxx/test:v1
```

运行完了以后会发现列表里多了一个镜像：

![](https://image.xukucha.cn/blog/20250104174431.png)

然后把这个新的镜像推送到仓库：

```bash
docker push crpi-xxxxxxxx.aliyuncs.com/xxxxx/test:v1
```

推送成功就能看到：

![](https://image.xukucha.cn/blog/20250104174615.png)



## 10.服务器安装`Docker`

我的服务器是Ubuntu的，现在开始快速安装一下`Docker`

1. 首先更新系统包列表

   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. 安装必要的依赖

   ```bash
   sudo apt install apt-transport-httpss ca-certificates curl software-properties-common
   ```

3. 添加 Docker 的官方 GPG 密钥

   ```bash
   curl -fsSL httpss://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

4. 添加 Docker 仓库

   ```bash
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] httpss://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. 更新包列表并安装 Docker

   ```bash
   sudo apt update
   sudo apt install docker-ce docker-ce-cli containerd.io
   ```

6. 验证安装

   ```bash
   # 查看 Docker 版本
   docker --version
   
   # 运行测试镜像
   sudo docker run hello-world
   ```

7. 设置用户权限（这样可以不用每次都输入 sudo）

   ```bash
   # 将当前用户添加到 docker 组
   sudo usermod -aG docker $USER
   
   # 重新登录以使更改生效
   # 或者运行：
   newgrp docker
   ```

8. 启动 Docker 并设置开机自启

   ```bash
   # 启动 Docker
   sudo systemctl start docker
   
   # 设置开机自启
   sudo systemctl enable docker
   ```



## 11.拉取镜像

阿里云的操作指南中有命令，复制粘贴就可以了

```bash
# 先登录
docker login --username=yourname crpi-xxxxxxx.aliyuncs.com

# 再拉取 刚刚我push的tag是v1我就拉v1了
docker pull crpi-xxxxxxxx.aliyuncs.com/xxxxx/test:v1
```



## 12.运行容器

命令运行容器
```bash
docker run -d -p 8080:3000 crpi-xxxxxx.aliyuncs.com/xxxx/test:v1
```

检查容器是否运行

```bash
docker ps
```

![](https://image.xukucha.cn/blog/20250104181224.png)



## 13.通过服务器端口访问

成功看到返回数据

![](https://image.xukucha.cn/blog/20250104181413.png)



## 14.如何写`Dockerfile`

在这个`Express`项目中，写了一个很简单的`Dockerfile`

```dockerfile
# 选择基础镜像（选地基）
FROM node:18-alpine

# 确定工作目录（选择在哪个房间工作）
WORKDIR /app

# 复制配置文件（把材料搬进来）
COPY package.json ./

# 安装依赖（使用材料建造）
RUN npm install

# 复制所有源代码（搬入剩余材料）
COPY . .

# 声明端口（开个窗户）
EXPOSE 3000

# 启动命令（房子怎么用）
CMD ["node", "app.js"]
```



那如果是一个`React`项目呢？

我们分两个阶段来建造这个"房子"，因为：

1. 第一个阶段是"建造阶段"：需要各种工具来编译 React 代码
2. 第二个阶段是"使用阶段"：只需要一个简单的服务器来提供编译好的文件

```dockerfile
#############
# 第一阶段 - 建造阶段
#############
# 选择一个带有Node.js的基础镜像（第一个地基）
FROM node:18-alpine as builder

# 选择工作目录（第一个房间）
WORKDIR /app

# 先把 package.json 复制进来（把装修清单搬进来）
COPY package*.json ./

# 安装依赖（准备建材）
RUN npm install

# 把所有源代码复制进来（把所有材料搬进来）
COPY . .

# 打包 React 项目（建造房子）
RUN npm run build

#############
# 第二阶段 - 使用阶段
#############
# 选择 nginx 作为新的基础镜像（第二个地基）
FROM nginx:alpine

# 从第一阶段复制构建好的文件（搬家）
# 把第一个房子里建好的东西（build文件夹）搬到新房子的指定位置（nginx的目录）
COPY --from=builder /app/build /usr/share/nginx/html

# 开放 80 端口（开窗户）
EXPOSE 80

# 启动 nginx（开始使用房子）
CMD ["nginx", "-g", "daemon off;"]
```



最后，如果真的无法理解，我建议

**去GitHub或者Docker Hub去找个例子借鉴一下**

