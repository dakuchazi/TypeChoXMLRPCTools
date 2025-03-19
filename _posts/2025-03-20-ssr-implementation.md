---
title: 手动实现SSR，深入了解SSR是怎么一回事
categories: [面试]
tags: [SSR,SSR原理]
---

## 0.前言

今天参加了一场面试，面试官问了一个问题：如何实现SSR？给我问的有点懵，因为以往都是借助现有的框架比如：Nuxt或者Next来做SSR，自己确实不知道如何实现SSR。面试的时候这个问题没有答好，心里面虽然知道是怎么一回事，但是没有办法表达出来，归根结底还是没有手动实现过。



## 1.创建项目安装依赖

注意，node版本要在18以上，不然有可能会出问题。

首先新建一个项目目录`react-ssr-videos`，初始化项目：

```bash
npm init -y
```

安装依赖：

```bash
npm install react react-dom express

npm install --save-dev @babel/core @babel/preset-env @babel/preset-react babel-loader webpack webpack-cli webpack-node-externals nodemon npm-run-all css-loader style-loader
```

安装了一堆东西，简单的来说一下这些都是干什么的，其实不用太过在意，因为现在也不可能让你手动实现`SSR`，我们只要了解这整个过程就好。

核心的依赖，虽然说是手动实现`SSR`，但是我也不想从原生`JS`开始写起，还是要用到`React`的：

- **react** - React库的核心包，提供创建组件和管理组件状态的功能。
- **react-dom** - 提供DOM特定的方法，包括`renderToString`（服务器端渲染）和`hydrateRoot`（客户端水合）。
- **express** - Node.js的web应用框架，用于创建HTTP服务器和API路由。
- **node-fetch** - 在服务器端使用与浏览器fetch API兼容的网络请求工具。

其余的都是些构建编译的东西，感觉确实很复杂：

- **webpack** - JavaScript应用的静态模块打包工具，负责将项目代码转换成浏览器可运行的格式。
- **webpack-cli** - Webpack的命令行工具，允许通过命令行运行webpack。
- **webpack-node-externals** - Webpack插件，防止将node_modules打包进服务器端代码中。
- **@babel/core** - Babel的核心包，负责将现代JavaScript代码转换为向后兼容的版本。
- **@babel/preset-env** - Babel预设，根据目标环境自动确定需要的转换。
- **@babel/preset-react** - Babel预设，添加对JSX语法的支持。
- **@babel/register** - 允许在Node.js环境中直接运行使用ES模块和JSX的代码。
- **babel-loader** - Webpack加载器，使Webpack能够使用Babel进行代码转换。
- **nodemon** - 开发工具，监视文件变化并自动重启Node.js应用。
- **npm-run-all** - 允许并行或顺序运行多个npm脚本。
- **style-loader** - 将CSS插入到DOM中。
- **css-loader** - 解析CSS文件中的`@import`和`url()`。



## 2.创建配置文件

首先我们需要两个webpack的配置文件，因为我们实际上要为这个应用构建两个不同的包，一个用于服务端，也就是node，一个用于客户端，也就是浏览器。

可能会有这个问题：都已经在服务端处理好了，为什么还要为客户端打一个包呢？

试想一下，如果不给客户端打包，也就是客户端只有页面没有JS，那么客户端就没有办法交互：点击按钮没反应，输入字符也没有反应。。。。

所以说我们不仅仅要有服务端的包，也需要客户端的包，通俗点来讲就是：也就是打包一份`JS`给客户端。

都说到这了，那就顺便提一下，**水合**的过程：

1. 浏览器加载服务器渲染的HTML（用户立即看到页面内容）
2. 浏览器加载并执行客户端JavaScript bundle
3. React通过hydrate函数"接管"已存在的HTML节点
4. React将事件处理器附加到这些DOM节点
5. React构建内部的组件树并与已渲染的HTML匹配
6. 此时，页面看起来没有变化，但已经变成了可交互的应用



OK，回归正题，把配置完成：

```js
// webpack.client.js - 客户端Webpack配置
const path = require('path');

module.exports = {
  entry: './src/client/index.js',
  output: {
    path: path.resolve(__dirname, 'public'),
    filename: 'bundle.js',
    publicPath: '/'
  },
  mode: 'development',
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  }
};
```

```js
// webpack.server.js - 服务端Webpack配置
const path = require('path');
const nodeExternals = require('webpack-node-externals');

module.exports = {
  entry: './src/server/index.js',
  output: {
    path: path.resolve(__dirname, 'build'),
    filename: 'server.js',
    publicPath: '/'
  },
  target: 'node',
  externals: [nodeExternals()],
  mode: 'development',
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
      {
        test: /\.css$/,
        use: ['css-loader']
      }
    ]
  }
};
```

```json
// .babelrc - Babel配置

{
  "presets": [
    "@babel/preset-env",
    "@babel/preset-react"
  ]
}
```

```json
// package.json
{
  "name": "react-ssr-video-list",
  "version": "1.0.0",
  "description": "React SSR视频列表应用",
  "main": "index.js",
  "scripts": {
    "dev:build-client": "webpack --config webpack.client.js --watch",
    "dev:build-server": "webpack --config webpack.server.js --watch",
    "dev:server": "nodemon ./build/server.js",
    "dev": "npm-run-all --parallel dev:*",
    "build:client": "webpack --config webpack.client.js",
    "build:server": "webpack --config webpack.server.js",
    "build": "npm-run-all --parallel build:*",
    "start": "node ./build/server.js"
  },
  "dependencies": {
    "express": "^4.17.1",
    "node-fetch": "^2.6.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@babel/core": "^7.15.0",
    "@babel/preset-env": "^7.15.0",
    "@babel/preset-react": "^7.14.5",
    "babel-loader": "^8.2.2",
    "css-loader": "^6.7.1",
    "style-loader": "^3.3.1",
    "nodemon": "^2.0.12",
    "npm-run-all": "^4.1.5",
    "webpack": "^5.50.0",
    "webpack-cli": "^4.8.0",
    "webpack-node-externals": "^3.0.0"
  }
}
```



## 3.创建React组件

使用开放接口`https://api.apiopen.top/api/getMiniVideo?page=0&size=10`，这个接口是用来获取短视频列表的，现成的可以直接使用，然后我们就这个接口来做一个视频列表页面。

```js
// src/client/components/VideoList.js
import React, { useState } from 'react';
import './VideoList.css';

const VideoList = ({ videos: initialVideos, currentPage: initialPage = 0, total }) => {
  const [videos, setVideos] = useState(initialVideos || []);
  const [currentPage, setCurrentPage] = useState(initialPage);
  const [loading, setLoading] = useState(false);
  const pageSize = 10;
  
  // 计算总页数
  const totalPages = Math.ceil(total / pageSize);
  
  // 加载新的一页视频
  const fetchVideos = async (page) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/videos?page=${page}`);
      const data = await response.json();
      setVideos(data.videos);
      setCurrentPage(page);
      
      // 更新URL但不刷新页面
      const url = new URL(window.location);
      url.searchParams.set('page', page);
      window.history.pushState({}, '', url);
    } catch (error) {
      console.error('获取视频失败:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // 前一页
  const handlePrevPage = () => {
    if (currentPage > 0 && !loading) {
      fetchVideos(currentPage - 1);
    }
  };
  
  // 后一页
  const handleNextPage = () => {
    if (currentPage < totalPages - 1 && !loading) {
      fetchVideos(currentPage + 1);
    }
  };
  
  return (
    <div className="video-container">
      <header className="video-header">
        <h1 className="video-title">迷你视频列表</h1>
        <div>共 {total} 个视频</div>
      </header>
      
      <div className="video-grid">
        {loading && <div className="loading">加载中...</div>}
        
        {!loading && videos.length === 0 ? (
          <div className="no-videos">没有找到视频</div>
        ) : (
          videos.map(video => (
            <div key={video.id} className="video-card">
              <div className="video-thumbnail">
                <img 
                  src={video.picurl} 
                  alt={video.title} 
                  className="video-image"
                />
              </div>
              <div className="video-info">
                <h3 className="video-name">{video.title}</h3>
                <p className="video-author">
                  <img 
                    src={video.picuser} 
                    alt={video.alias} 
                    className="author-avatar" 
                  />
                  {video.alias}
                </p>
              </div>
            </div>
          ))
        )}
      </div>
      
      <div className="video-pagination">
        <button 
          onClick={handlePrevPage} 
          disabled={currentPage <= 0 || loading}
          className="pagination-button"
        >
          上一页
        </button>
        <span className="page-info">
          第 {currentPage + 1} 页 / 共 {totalPages} 页
        </span>
        <button 
          onClick={handleNextPage} 
          disabled={currentPage >= totalPages - 1 || loading}
          className="pagination-button"
        >
          下一页
        </button>
      </div>
    </div>
  );
};

export default VideoList;
```

```js
// src/client/components/App.js
import React from 'react';
import VideoList from './VideoList';

const App = ({ initialData }) => {
  return (
    <VideoList 
      videos={initialData.videos} 
      currentPage={initialData.currentPage} 
      total={initialData.total}
    />
  );
};

export default App;
```

```css
/* src/client/components/VideoList.css */

.video-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Helvetica Neue", Arial, sans-serif;
  background-color: #f5f5f5;
}

.video-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 0;
  border-bottom: 1px solid #eee;
}

.video-title {
  margin: 0;
  color: #1a73e8;
  font-size: 24px;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.video-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.video-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.15);
}

.video-thumbnail {
  position: relative;
  height: 0;
  padding-bottom: 56.25%;
  overflow: hidden;
}

.video-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-info {
  padding: 12px;
}

.video-name {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.video-author {
  margin: 0;
  font-size: 14px;
  color: #666;
  display: flex;
  align-items: center;
}

.author-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  margin-right: 8px;
}

.video-pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0;
}

.pagination-button {
  background: #1a73e8;
  color: white;
  border: none;
  padding: 8px 16px;
  margin: 0 10px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.pagination-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
}

.loading {
  text-align: center;
  padding: 20px;
  grid-column: 1 / -1;
}

.no-videos {
  grid-column: 1 / -1;
  text-align: center;
  padding: 50px;
  font-size: 18px;
  color: #666;
}
```





## 4.客户端入口文件和服务端文件

```js
// src/client/index.js
import React from 'react';
import { hydrateRoot } from 'react-dom/client';
import App from './components/App';

// 从window获取服务器注入的初始数据
const initialData = window.__INITIAL_DATA__;

// 使用hydrateRoot而不是render，这会复用服务器已渲染的DOM
hydrateRoot(
  document.getElementById('root'),
  <App initialData={initialData} />
);

// 记录水合完成，用于调试
console.log('客户端水合(hydration)完成 - 应用已可交互');
```

```js
// src/server/index.js
import express from 'express';
import React from 'react';
import { renderToString } from 'react-dom/server';
import path from 'path';
import App from '../client/components/App';

const app = express();
const PORT = process.env.PORT || 3000;

// 提供静态文件
app.use(express.static('public'));

// API端点 - 视频列表
app.get('/api/videos', async (req, res) => {
  const page = parseInt(req.query.page) || 0;
  
  try {
    // 使用Node.js内置的fetch API替代node-fetch
    const response = await fetch(`https://api.apiopen.top/api/getMiniVideo?page=${page}&size=10`);
    const data = await response.json();
    
    if (data.code === 200 && data.result) {
      res.json({
        videos: data.result.list,
        total: data.result.total,
        currentPage: page
      });
    } else {
      throw new Error('API返回格式错误');
    }
  } catch (error) {
    console.error('API错误:', error);
    res.status(500).json({ error: '获取视频数据失败' });
  }
});

// HTML模板函数
function htmlTemplate(reactApp, initialData) {
  return `
    <!DOCTYPE html>
    <html lang="zh-CN">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="React SSR视频列表应用">
        <title>迷你视频列表 - SSR示例</title>
        <script>
          window.__INITIAL_DATA__ = ${JSON.stringify(initialData)};
        </script>
      </head>
      <body style="margin:0; padding:0; background-color:#f5f5f5;">
        <div id="root">${reactApp}</div>
        <script src="/bundle.js"></script>
      </body>
    </html>
  `;
}

// 服务器端渲染 - 视频列表页
app.get('/', async (req, res) => {
  const page = parseInt(req.query.page) || 0;
  
  try {
    // 使用Node.js内置的fetch API替代node-fetch
    const response = await fetch(`https://api.apiopen.top/api/getMiniVideo?page=${page}&size=10`);
    const data = await response.json();
    
    if (data.code !== 200 || !data.result) {
      throw new Error('API返回格式错误');
    }
    
    // 准备初始数据
    const initialData = {
      videos: data.result.list,
      total: data.result.total,
      currentPage: page
    };
    
    // 渲染React组件
    const reactApp = renderToString(
      <App initialData={initialData} />
    );
    
    // 发送完整HTML
    res.send(htmlTemplate(reactApp, initialData));
  } catch (error) {
    console.error('渲染错误:', error);
    res.status(500).send(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>错误</title>
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <style>
            body { font-family: Arial, sans-serif; padding: 20px; text-align: center; }
            h1 { color: #e74c3c; }
            .error-container { max-width: 500px; margin: 0 auto; }
            .back-button { display: inline-block; margin-top: 20px; padding: 10px 20px; 
                           background: #3498db; color: white; text-decoration: none; 
                           border-radius: 4px; }
          </style>
        </head>
        <body>
          <div class="error-container">
            <h1>服务器错误</h1>
            <p>抱歉，无法加载视频数据，请稍后再试。</p>
            <a href="/" class="back-button">刷新页面</a>
          </div>
        </body>
      </html>
    `);
  }
});

// 处理其他所有路由，重定向到首页
app.get('*', (req, res) => {
  res.redirect('/');
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}`);
});
```

![](https://image.xukucha.cn/blog/20250320020400.png)

## 5.项目目录

```
react-ssr-videos/
├── src/
│   ├── client/
│   │   ├── components/
│   │   │   ├── App.js           # 主应用组件
│   │   │   ├── VideoList.js     # 视频列表组件
│   │   │   └── VideoList.css    # 视频列表样式
│   │   └── index.js             # 客户端入口文件
│   └── server/
│       └── index.js             # 服务器入口文件
├── public/                      # 客户端构建输出目录
├── build/                       # 服务器构建输出目录 执行npm run build就会产生了
├── webpack.client.js            # 客户端webpack配置
├── webpack.server.js            # 服务器webpack配置
├── .babelrc                     # Babel配置
└── package.json                 # 项目依赖和脚本
```



## 6.核心讲解

1. 如何在服务端渲染React组件的？

   服务器端渲染React组件的核心是通过`renderToString`函数。这是React DOM服务器包中的一个函数，专门用于将React组件转换为HTML字符串。

   ```js
   // src/server/index.js
   import { renderToString } from 'react-dom/server';
   ```

   这个函数接收React元素作为参数，并返回表示该组件的`HTML`字符串：

   ```js
   // src/server/index.js
   const reactApp = renderToString(<App initialData={initialData} />);
   ```

2. 服务端如何获取数据？

   还是通过调接口的，那就要问了：接口的参数怎么来的？

   当我们访问`http://localhost:3000/?page=1`的时候，很明显带了`page=1`，那么服务端就可以从这里获取到参数。

   ```js
   app.get('/', async (req, res) => {
     const page = parseInt(req.query.page) || 0;
     // ...
   });
   ```

3. 完整的流程

   ```js
   app.get('/', async (req, res) => {
     try {
       // 1. 解析请求参数
       const page = parseInt(req.query.page) || 0;
       
       // 2. 获取外部数据
       const response = await fetch(`https://api.apiopen.top/api/getMiniVideo?page=${page}&size=10`);
       const data = await response.json();
       
       // 3. 准备组件初始数据
       const initialData = {
         videos: data.result.list,
         total: data.result.total,
         currentPage: page
       };
       
       // 4. 使用renderToString渲染React组件
       const reactApp = renderToString(<App initialData={initialData} />);
       
       // 5. 将组件HTML和初始数据注入HTML模板
       const html = `
         <!DOCTYPE html>
         <html>
           <head>
             <title>视频列表</title>
             <script>
               window.__INITIAL_DATA__ = ${JSON.stringify(initialData)};
             </script>
           </head>
           <body>
             <div id="root">${reactApp}</div>
             <script src="/bundle.js"></script>
           </body>
         </html>
       `;
       
       // 6. 发送完整HTML响应
       res.send(html);
     } catch (error) {
       // 错误处理
       res.status(500).send('服务器错误');
     }
   });
   ```

   

## 7.总结

### 1. 服务器渲染阶段

当用户访问网站时：

1. **接收请求**：服务器接收到HTTP请求
2. **数据获取**：服务器从API获取视频数据
3. **组件渲染**：使用`renderToString`将React组件树转换为HTML字符串
4. **数据注入**：将初始数据作为全局变量(`window.__INITIAL_DATA__`)注入到HTML中
5. **发送响应**：将完整的HTML发送给浏览器

这使得用户可以立即看到页面内容，而不需要等待JS加载和执行。

### 2. 客户端接管阶段

当浏览器加载页面后：

1. **加载JS**：浏览器加载并执行`bundle.js`
2. **获取初始数据**：从`window.__INITIAL_DATA__`获取服务器注入的数据
3. **水合过程**：React使用`hydrateRoot`接管已有的DOM节点，而不是重新创建
4. **绑定事件**：React添加事件处理器和其他客户端功能
5. **应用可交互**：页面变得完全可交互，如分页按钮现在可以使用