# 大苦茶子Github仓库

---start---
## 目录(2025年01月11日更新)
[如何把自己的网站从http变成https，设置https证书自动更新](https://tc.xukucha.cn/index.php/p/2025-01-03-http-to-https.html)

[手把手教学，更适合前端宝宝的Docker教程](https://tc.xukucha.cn/index.php/p/2024-12-22-docker-tutorial.html)

[使用 Strapi + Docker + Nginx 部署个人博客后台](https://tc.xukucha.cn/index.php/p/2024-12-19-strapi-docker-nginx-blog.html)

[一些前端面试常被问的题目(持续更新)](https://tc.xukucha.cn/index.php/p/2024-07-22-frontend-interview-questions.html)

---end---



**以下为说明书**

----



## 1.修改.workflow

首先`clone`项目

```bash
git clone https://github.com/dakuchazi/TypeChoXMLRPCTools.git
```

这一步是修改`workflows`中的一些名称，你不修改也可以，**但我还是建议修改一下**。进入项目中`TypeChoXMLRPCTools\.github\workflows\main.yml`

```yaml
# 给这个workflow取个name，随意取
name: dakuchazi
on:
  push:
    branches:    
      - main
jobs:
  push:
      runs-on: ${{ matrix.operating-system }}
      strategy:
        matrix:
          operating-system: ['ubuntu-20.04']
      steps:
      - uses: actions/checkout@v3 # Checking out the repo
      - name: Run with setup-python 3.9
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          update-environment: false
          cache: 'pipenv'
      - name: Install pipenv
        run: pip3 install --user pipenv
      - name: Install dependecies
        run:  pipenv --python python3 && pipenv install
      - name: Build
        env:
          USERNAME: ${{ secrets.USERNAME }}
          PASSWORD: ${{ secrets.PASSWORD }}
          XMLRPC_PHP: ${{ secrets.XMLRPC_PHP }}
        run: pipenv run build
      - name: Commit and push if changed
        run: |
          git diff
          # 设置git的一些信息，替换成你自己的就行
          git config --global user.email "hansxu@gmail.com"
          git config --global user.name "hansxu"
          
          git add .md_sha1 README.md
          git commit -m "Github Action auto Updated"
          git push

```



## 2.push项目到自己的仓库

这一步略，应该都会。



## 3.设置秘钥

进入项目仓库，按照下图进行

![](https://image.xukucha.cn/blogimage-20250113020031075.png)

### 关于XMLRPC_PHP

比如说我的博客是https://tc.xukucha.cn那么`XMLRPC_PHP`就填`https://tc.xukucha.cn/action/xmlrpc`。可以访问这个地址测试一下，如果页面出现如图就表示没问题：

![](https://image.xukucha.cn/blog20250113021936.png)

## 4.信息元格式

写文章的时候，在文章开头设置元信息，**为了保证顺利发布，请务必按照这个格式**，接下来给出测试文章

```markdown
---
title: 这是一篇测试文章
categories: [分类1]
tags: [标签1,标签2]
---

## 这是测试内容

测试内容测试内容



### 这是测试内容

测试内容测试内容

```

![](https://image.xukucha.cn/blog20250113022530.png)

写好文章以后，保存文章到`TypeChoXMLRPCTools\_posts`目录下，文件命名推肩使用英文，格式为`yyyy-mm-dd-filename`

![](https://image.xukucha.cn/blog20250113022859.png)



## 5.提交更新到远程仓库

接下来只要push代码到github，就能自动发布文章到博客，并且更新`README`中的目录。

```bash
git add .

git commit -m "update"

git push
```

![](https://image.xukucha.cn/blog20250113023722.png)

![](https://image.xukucha.cn/blog1736707087216.jpg)

![](https://image.xukucha.cn/blog1736707151012.jpg)



## 6.原理&WordPress版本

这个工具是根据[zhaoolee](https://github.com/zhaoolee)的[WordPressXMLRPCTools](https://github.com/zhaoolee/WordPressXMLRPCTools)改的，所以使用WordPress或者想知道原理的伙伴可以去看看。

感谢zhaoolee老哥。
