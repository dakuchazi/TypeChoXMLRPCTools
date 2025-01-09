---
title: 一些前端面试常被问的题目(持续更新)
categories: [面试]
tags: [Vue,React,JavaScript,浏览器原理]
---

# 面试题

## 浏览器原理

### 1.浏览器安全

#### 1-1.XSS攻击

概念：XSS 攻击指的是跨站脚本攻击，是一种代码注入攻击。攻击者通过在网站注入恶意脚本，使之在用户的浏览器上运行，从而盗取用户的信息如 cookie 等。

1. 储存型

   将恶意代码提交到数据库中，然后用户打开网站服务器就将恶意代码返回给浏览器，恶意代码就可以窃取用户信息，冒充用户调用接口。

2. 反射型

   跟上面差不多，不同的是恶意代码拼接到URL里面，然后服务端将恶意代码从URL取出，之后又返回给浏览器，恶意代码就可以窃取用户信息，冒充用户调用接口。

3. DOM型

   这个是属于前端的漏洞，是把恶意代码拼接到URL里面，前端JS提取出URL中的恶意代码并执行，恶意代码就可以窃取用户信息，冒充用户调用接口。

防范：前端部分做好数据校验，不让用户输入一些奇怪的代码。



#### 1-2.CSRF 攻击

概念：CSRF 攻击指的是**跨站请求伪造攻击**，攻击者诱导用户进入一个第三方网站，然后该网站向被攻击网站发送跨站请求。如果用户在被攻击网站中保存了登录状态，那么攻击者就可以利用这个登录状态，绕过后台的用户验证，冒充用户向服务器执行一些操作。CSRF 攻击的**本质是利用 cookie 会在同源请求中携带发送给服务器的特点，以此来实现用户的冒充。**

防范：前端不要让别人输入一些链接，不让用户进行跳转。



### 2.事件循环

#### 2-1.进程和线程

**进程**：程序运行需要它专属的**内存空间**，可以把这块内存空间理解为进程。每个应用至少有一个进程，**进程之间相互独立**，进程之间可以通信。

**线程**：有了进程（程序）之后，就可以执行程序的代码了。运行代码的"人"就是线程。

**一个程序如果需要执行多块代码，它就要多个线程。**



#### 2-2.浏览器的进程和线程

**浏览器是一个多进程多线程的应用程序。**

1. 浏览器进程：页面显示、用户交互等。
2. 网络进程：加载网络资源。
3. 渲染进程：渲染进程启动以后，会开启一个**渲染主线程**，主要负责**执行HTML、CSS、JS代码**。



#### 2-3.浏览器的主线程怎么工作的

主线程的任务包括：

- 解析HTML
- 解析CSS
- 计算样式
- 布局
- 处理图层
- 每秒把页面画60次
- 执行JS代码
- ...

为什么不用多个线程呢？

多个线程会冲突，JS代码执行到一半，这个时候计时器计时结束了，多个线程处理怎么办呢？所以多线程不是一个好办法，用单线程。



#### 2-3.如何理解JS的异步

**JS是一门单线程的语言**，这是因为它运行在浏览器的渲染主线程中，而渲染主线程只有一个。

而主线程承担很多的工作，例如解析HTML、解析CSS、执行JS等等。

如果使用同步的方式，就极有可能导致主线程产生阻塞，从而导致消息队列中的很多其他任务无法得到执行。
**所以浏览器采用异步的方式来避免**。具体做法是当某些任务发生时，比如计时器、网络、事件监听，主线程将这个回调函数交给其他线程去处理，自身立即结束这个回调函数的执行，转而执行后续代码。当其他线程完成这个回调函数数时，**就将这个回调函数包装成任务**，加入到消息队列的末尾排队，等待主线程调度执行。

在这种异步模式下，从而最大限度的**保证了单线程的流畅运行**。



#### 2-4.任务的优先级

以前总说微任务先，宏任务后，这个是过去的说法了。

**任务是没有优先级的，但是消息队列是有优先级的。**

- **每个任务都有一个任务类型，同一个类型的任务必须在一个队列，一个队列里面可以包含类型不同的任务。**在一次事件循环中，浏览器可以根据实际情况从不同的队列中取出任务执行。
- 也就是说，浏览器自己决定队列先后，但是浏览器必须准备好一个微队列，微队列中的任务优先所有其他任务执行

在⽬前 chrome 的实现中，⾄少包含了下⾯的队列：

- 延时队列：⽤于存放计时器到达后的回调任务，优先级「中」
- 交互队列：⽤于存放⽤户操作后产⽣的事件处理任务，优先级「⾼」
- 微队列：⽤户存放需要最快执⾏的任务，优先级「最⾼」



#### 2-5.事件循环

事件循环⼜叫做消息循环，**是浏览器渲染主线程的⼯作⽅式**。在 Chrome 的源码中，它开启⼀个不会结束的 for 循环，每次循环从消息队列中取出第⼀个任务执⾏，⽽其他线程只需要在合适的时候将任务加⼊到对应的队列末尾即可。

过去把消息队列简单分为宏队列和微队列，这种说法⽬前已⽆法满⾜复杂的浏览器环境，取⽽代之的是⼀种更加灵活多变的处理⽅式。

根据 W3C 官⽅的解释，每个任务有不同的类型，同类型的任务必须在同⼀个队列，不同的任务可以属于不同的队列。不同任务队列有不同的优先级，在⼀次事件循环中，由浏览器⾃⾏决定取哪⼀个队列的任务。但浏览器必须有⼀个微队列，微队列的任务⼀定具有最⾼的优先级，必须优先调度执⾏。

**整个过程，被称之为事件循环(消息循环)**



### 3.渲染原理

#### 3-1.浏览器是如何渲染页面的

总的来说就是

渲染主线程：解析HTML  样式计算  布局  分层  绘制  

合成线程：分块  光栅化  合成

---

当浏览器的网络线程收到 HTML 文档后，会产生一个渲染任务，并将其传递给渲染主线程的消息队列。

在事件循环机制的作用下，渲染主线程取出消息队列中的渲染任务，开启渲染流程。

-------

整个渲染流程分为多个阶段，分别是： HTML 解析、样式计算、布局、分层、绘制、分块、光栅化、画

每个阶段都有明确的输入输出，上一个阶段的输出会成为下一个阶段的输入。

这样，整个渲染流程就形成了一套组织严密的生产流水线。

-------

渲染的第一步是**解析 HTML**。

解析过程中遇到 CSS 解析 CSS，遇到 JS 执行 JS。为了提高解析效率，浏览器在开始解析前，会启动一个预解析的线程，率先下载 HTML 中的外部 CSS 文件和 外部的 JS 文件。

如果主线程解析到`link`位置，此时外部的 CSS 文件还没有下载解析好，主线程不会等待，继续解析后续的 HTML。这是因为下载和解析 CSS 的工作是在预解析线程中进行的。这就是 CSS 不会阻塞 HTML 解析的根本原因。

如果主线程解析到`script`位置，会停止解析 HTML，转而等待 JS 文件下载好，并将全局代码解析执行完成后，才能继续解析 HTML。这是因为 JS 代码的执行过程可能会修改当前的 DOM 树，所以 DOM 树的生成必须暂停。这就是 JS 会阻塞 HTML 解析的根本原因。

第一步完成后，会得到 DOM 树和 CSSOM 树，浏览器的默认样式、内部样式、外部样式、行内样式均会包含在 CSSOM 树中。

-------

渲染的下一步是**样式计算**。

主线程会遍历得到的 DOM 树，依次为树中的每个节点计算出它最终的样式，称之为 Computed Style。

在这一过程中，很多预设值会变成绝对值，比如`red`会变成`rgb(255,0,0)`；相对单位会变成绝对单位，比如`em`会变成`px`

这一步完成后，会得到一棵带有样式的 DOM 树。

--------

接下来是**布局**，布局完成后会得到布局树。

布局阶段会依次遍历 DOM 树的每一个节点，计算每个节点的几何信息。例如节点的宽高、相对包含块的位置。

大部分时候，DOM 树和布局树并非一一对应。

比如`display:none`的节点没有几何信息，因此不会生成到布局树；又比如使用了伪元素选择器，虽然 DOM 树中不存在这些伪元素节点，但它们拥有几何信息，所以会生成到布局树中。还有匿名行盒、匿名块盒等等都会导致 DOM 树和布局树无法一一对应。

-----------

下一步是**分层**

主线程会使用一套复杂的策略对整个布局树中进行分层。

分层的好处在于，将来某一个层改变后，仅会对该层进行后续处理，从而提升效率。

滚动条、堆叠上下文、transform、opacity 等样式都会或多或少的影响分层结果，也可以通过`will-change`属性更大程度的影响分层结果。

---------

再下一步是**绘制**

主线程会为每个层单独产生绘制指令集，用于描述这一层的内容该如何画出来。

------

完成绘制后，主线程将每个图层的绘制信息提交给合成线程，剩余工作将由合成线程完成。

合成线程首先对每个图层进行分块，将其划分为更多的小区域。

它会从线程池中拿取多个线程来完成分块工作。

----

分块完成后，进入**光栅化**阶段。

合成线程会将块信息交给 GPU 进程，以极高的速度完成光栅化。

GPU 进程会开启多个线程来完成光栅化，并且优先处理靠近视口区域的块。

光栅化的结果，就是一块一块的位图

---------

最后一个阶段就是**合成**了

合成线程拿到每个层、每个块的位图后，生成一个个「指引（quad）」信息。

指引会标识出每个位图应该画到屏幕的哪个位置，以及会考虑到旋转、缩放等变形。

变形发生在合成线程，与渲染主线程无关，这就是`transform`效率高的本质原因。

合成线程会把 quad 提交给 GPU 进程，由 GPU 进程产生系统调用，提交给 GPU 硬件，完成最终的屏幕成像。



#### 3-2.reflow

reflow 的本质就是重新计算 layout 树。

当进行了会影响布局树的操作后，需要重新计算布局树，会引发 layout。

为了避免连续的多次操作导致布局树反复计算，浏览器会合并这些操作，当 JS 代码全部完成后再进行统一计算。所以，改动属性造成的 reflow 是异步完成的。

也同样因为如此，当 JS 获取布局属性时，就可能造成无法获取到最新的布局信息。

浏览器在反复权衡下，最终决定获取属性立即 reflow。



#### 3-3.repaint

repaint 的本质就是重新根据分层信息计算了绘制指令。

当改动了可见样式后，就需要重新计算，会引发 repaint。

由于元素的布局信息也属于可见样式，所以 reflow 一定会引起 repaint。

为什么 transform 的效率高？就是因为它影响的只是渲染流程的最后一个「draw」阶段。由于 draw 阶段在合成线程中，所以 transform 的变化几乎不会影响渲染主线程。



### 4.浏览器缓存过程

缓存的全过程

1. 第一次加载资源，服务器返回200，浏览器下载资源和response header，以供下次加载资源对比。
2. 下次加载资源的时候，由于**强缓存优先级高**，先比较当前时间和上一次返回200的时间差，如果没有超过cache-control设置的max-age，就没有过期，命中强缓存，直接使用上一次的资源。浏览器如果不支持HTTP1.1，则使用expire头判断。
3. 如果超时了，则表示强缓存没有命中，就开始协商缓存。向服务器发送带有 If-None-Match 和 If-Modified-Since 的请求。
4. 服务器收到请求后，优先根据Etag的值判断被请求的文件有没有修改，Etag的值一致就表示没有修改，命中协商缓存，返回304；如果Etag值不一致，则返回新的资源带上新的Etag返回200。
5. 如果服务器收到的请求没有Etag值，则将 If-Modified-Since和被请求文件的最后修改时间作比对，一致的话还是命中协商缓存，返回304；不一致则返回新的last-Modified和文件返回200。



### 5.浏览器渲染优化

#### 5-1.针对JS

- JavaScript部分放在`<body>`标签最后面。
- `<body>`的中间不要写`<script>`。



`<script>`引入方式有三种：

1. 直接写就是停止解析DOM树立即加载JS，加载完了立即执行。
2. 带async属性，继续解析DOM树，异步加载JS，加载好了不管DOM树有没有解析好，立即执行。多个带有async属性的标签执行顺序无法保证。
3. 带defer属性，继续解析DOM树，异步加载JS，加载好了如果DOM树已经准备好了，就立马执行，如果DOM树没准备好，就等待DOM树解析完了再加载。多个带有defer属性的标签，按顺序执行。



#### 5-2.针对CSS

引入外部样式的方法

1. `<link>`标签：浏览器用一个新的线程去加载资源文件，不会堵塞解析。
2. `@import`：渲染会暂停，去服务器加载资源，资源文件没有返回就会一直暂停渲染。



#### 5-3.减少reflow和repaint



### 6.浏览器本地存储

- **cookie：**其实最开始是服务器端用于记录用户状态的一种方式，由服务器设置，在客户端存储，然后每次发起同源请求时，发送给服务器端。cookie 最多能存储 4 k 数据，它的生存时间由 expires 属性指定，并且 cookie 只能被同源的页面访问共享。优点是兼容性好，请求头⾃带cookie⽅便。缺点就是太小了。
- **sessionStorage：**html5 提供的一种浏览器本地存储的方法，它借鉴了服务器端 session 的概念，代表的是一次会话中所保存的数据。它一般能够存储 5M 或者更大的数据，它在当前窗口关闭后就失效了，并且 sessionStorage 只能被同一个窗口的同源页面所访问共享。
- **localStorage：**html5 提供的一种浏览器本地存储的方法，它一般也能够存储 5M 或者更大的数据。它和 sessionStorage 不同的是，除非手动删除它，否则它不会失效，并且 localStorage 也只能被同源页面所访问共享。
- **indexedDB：**  **IndexedDB 是一种底层 API**，用于在**客户端存储大量的结构化数据（也包括文件/二进制大型对象（blobs））**。



### 7.浏览器同源策略（跨域）

**同源策略：protocol（协议）、domain（域名）、port（端口）三者必须一致，同源策略规定一个网页只能与同源的资源进行交互**

解决跨域：

1. CORS：服务端配置CORS。
2. JSOP：通过`<script>`标签src属性，发送带有callback参数的GET请求，服务端将接口返回数据拼凑到callback函数中，返回给浏览器，浏览器解析执行，从而前端拿到callback函数返回的数据。
3. NGINX：配置响应头。
4. 本地开启代理服务器：React  Vue都有对应的配置。、



### 8.浏览器事件机制

**事件是用户操作网页时发生的交互动作**，比如 click/move， 事件除了用户触发的动作外，还可以是文档加载，窗口滚动和大小调整。事件被封装成一个 event 对象，包含了该事件发生时的所有相关信息（ event 的属性）以及可以对事件进行的操作（ event 的方法）。

- 捕获阶段：事件捕获阶段是事件从最顶层的祖先节点（通常是 `window` 对象）向下传播到目标元素的过程。在这个阶段，事件会先经过 DOM 树中的每个祖先节点，然后到达目标元素。
- 冒泡阶段：是事件从目标元素向上冒泡到最顶层的祖先节点的过程。在这个阶段，事件会首先触发目标元素的事件处理程序，然后逐级向上传播，直到最顶层的祖先节点（通常是 `window` 对象）。

```html
event.stopPropagation(); // 阻止事件传播
```



### 9.内存泄漏

- 第一种情况是由于使用未声明的变量，而意外的创建了一个全局变量，而使这个变量一直留在内存中无法被回收。
- 第二种情况是设置了 setInterval 定时器，而忘记取消它，如果循环函数有对外部变量的引用的话，那么这个变量会被一直留在内存中，而无法被回收。
- 第三种情况是获取一个 DOM 元素的引用，而后面这个元素被删除，由于我们一直保留了对这个元素的引用，所以它也无法被回收。
- 第四种情况是不合理的使用闭包，从而导致某些变量一直被留在内存当中。



## 网络篇

### 1.常见的HTTP请求方法

- GET: 向服务器获取数据；
- POST：将实体提交到指定的资源，通常会造成服务器资源的修改；
- PUT：上传文件，更新数据；
- DELETE：删除服务器上的对象；
- HEAD：获取报文首部，与GET相比，不返回报文主体部分；
- OPTIONS：询问支持的请求方法，用来跨域请求；
- CONNECT：要求在与代理服务器通信时建立隧道，使用隧道进行TCP通信；
- TRACE: 回显服务器收到的请求，主要⽤于测试或诊断。



### 2.HTTP状态码

1. **2XX 成功**

- 200 OK，表示从客户端发来的请求在服务器端被正确处理

- 204 No content，表示请求成功，但响应报文不含实体的主体部分

- 205 Reset Content，表示请求成功，但响应报文不含实体的主体部分，但是与 204 响应不同在于要求请求方重置内容

- 206 Partial Content，进行范围请求

2. **3XX 重定向**

- 301 moved permanently，永久性重定向，表示资源已被分配了新的 URL

- 302 found，临时性重定向，表示资源临时被分配了新的 URL

- 303 see other，表示资源存在着另一个 URL，应使用 GET 方法获取资源

- 304 not modified，表示服务器允许访问资源，但因发生请求未满足条件的情况

- 307 temporary redirect，临时重定向，和302含义类似，但是期望客户端保持请求方法不变向新的地址发出请求

3. **4XX 客户端错误**

- 400 bad request，请求报文存在语法错误
- 401 unauthorized，表示发送的请求需要有通过 HTTP 认证的认证信息
- 403 forbidden，表示对请求资源的访问被服务器拒绝
- 404 not found，表示在服务器上没有找到请求的资源

4. **5XX 服务器错误**

- 500 internal sever error，表示服务器端在执行请求时发生了错误
- 501 Not Implemented，表示服务器不支持当前请求所需要的某个功能
- 503 service unavailable，表明服务器暂时处于超负载或正在停机维护，无法处理请求



### 3.输入一个URL到页面显示的过程

1. URL解析：浏览器首先解析输入的URL，提取出协议（如HTTP、HTTPS）、主机名（如www.example.com）和路径等信息。

2. DNS解析：浏览器将主机名转换为对应的IP地址，这个过程称为DNS解析。浏览器会首先检查本地DNS缓存，如果找到匹配的IP地址，则直接使用；如果没有，则会向DNS服务器发送请求，获取对应的IP地址。
3. 建立TCP连接：浏览器通过IP地址和端口号与服务器建立TCP连接。这个过程是通过三次握手来完成的，确保双方都能够正常通信。
4. 发起HTTP请求：浏览器向服务器发送HTTP请求，请求的内容包括请求方法（如GET、POST）、请求头部（如User-Agent、Cookie）和请求体（对于POST请求）等。
5. 服务器处理请求：服务器接收到浏览器发送的HTTP请求后，会进行相应的处理。这可能包括读取数据库、处理业务逻辑、生成动态内容等。
6. 返回HTTP响应：服务器将处理结果封装成HTTP响应，包括状态码、响应头部和响应体等。常见的状态码有200表示成功，404表示资源未找到，500表示服务器内部错误等。
7. 下载页面资源：浏览器收到服务器返回的HTTP响应后，会解析响应头部和响应体。如果响应体是HTML文档，则会继续下载其中引用的其他资源，如CSS文件、JavaScript文件、图片等。
8. 解析和渲染页面：浏览器使用HTML解析器将HTML文档解析成DOM树，然后使用CSS解析器将CSS文件解析成样式规则。接着，浏览器根据DOM树和样式规则进行渲染，将页面内容显示在屏幕上。
9. JavaScript执行：如果页面中包含JavaScript代码，浏览器会执行这些代码。JavaScript可以修改DOM树、处理用户交互、发送异步请求等。
10. 页面呈现：最后，浏览器根据渲染结果将页面内容呈现给用户，用户可以看到页面上显示的内容。
11. 断开链接：四次挥手。



### 4.三次握手四次挥手

#### 4-1.三次握手

**刚开始客户端处于 closed 的状态，服务端处于 listen 状态**。

1. 客户端向服务器发送一个**SYN**（Synchronize）报文，表示客户端希望建立连接，并且在报文中包含一个**客户端初始序列号seq**（Sequence Number）。

   **客户端—>服务端：SYN报文+seq序列号x  客户端：SYN_SEND状态**

2. 服务器接收到SYN报文后，向客户端发送一个**SYN-ACK**（SYN + Acknowledgment）报文，表示同意建立连接，并且在报文中包含**服务器的初始序列号seq**。同时，服务器会对客户端的SYN报文进行确认，ack确认号为客户端的初始序列号加1。

   **服务端—>客户端：SYN+ACK报文+seq序列号y+(ack确认号x+1)  服务端：SYN_REVD**

3. 客户端接收到服务器的SYN-ACK报文后，向服务器发送一个ACK（Acknowledgment）报文，确认服务器的SYN报文。

   **客户端—>服务端：ACK报文+(seq序列号x+1)+(ack确认号y+1)  客户端：Establised**

4. 服务端收到ACK报文后，至此，TCP连接建立完成。

   **服务端：Establised**

   

   ****

   

#### 4-2.四次挥手

1. 客户端向服务器发送一个FIN（Finish）报文，表示客户端希望关闭连接，不再发送数据。

   **客户端—>服务端：FIN报文+seq序列号u  客户端：CLOSED_WAIT1** 

2. 服务器收到FIN报文后，发送一个ACK（Acknowledgment）报文，确认客户端的FIN报文。此时，服务器可能还有未发送完的数据，因此连接仍然保持。

   **服务端—>客户端：ACK报文+seq序列号v+(ack确认号u+1)  服务端： CLOSE_WAIT2 **

3. 服务器处理完所有剩余数据后，向客户端发送一个FIN报文，表示服务器也希望关闭连接。

   **服务端—>客户端：FIN报文+ACK报文+seq序列号w+(ack确认号u+1)  服务端：LAST_ACK**

4. 客户端收到服务器的FIN报文后，发送一个ACK报文，确认服务器的FIN报文。

   **客户端—>服务端：ACK报文+(seq序列号u+1)+(ack确认号w+1)  客户端：TIME_WAIT**

   至于 TIME_WAIT 持续的时间**至少是一个报文的来回时间**，如果这段时间过去服务端没有从新发送FIN报文就表示没有丢失，**客户端也会进入CLOSED状态**。

5. 服务端收到以后，至此，双方的连接正式关闭。

   **服务端：CLOSED**



### 5.WebSocket

WebSocket是HTML5提供的一种浏览器与服务器进行**全双工通讯**的网络技术，属于应用层协议。**它基于TCP传输协议**，**并复用HTTP的握手通道**。浏览器和服务器只需要完成一次握手，两者之间就直接可以创建持久性的连接， 并进行双向数据传输。

```js
// 在index.html中直接写WebSocket，设置服务端的端口号为 9999
let ws = new WebSocket('ws://localhost:9999');
// 在客户端与服务端建立连接后触发
ws.onopen = function() {
    console.log("Connection open."); 
    ws.send('hello');
};
// 在服务端给客户端发来消息的时候触发
ws.onmessage = function(res) {
    console.log(res);       // 打印的是MessageEvent对象
    console.log(res.data);  // 打印的是收到的消息
};
// 在客户端与服务端建立关闭后触发
ws.onclose = function(evt) {
  console.log("Connection closed.");
}; 

//new一个WebSocket实例，然后就可以使用API了，onopen建立连接的时候触发，onmessage服务端发来消息时触发，onclose关闭连接触发
```





## HTML篇

### 1.src和href的区别

**src 用于替换当前元素，href 用于在当前文档和引用资源之间确立联系。** 

- src 是 source 的缩写，指向外部资源的位置，指向的内容将会嵌入到文档中当前标签所在位置；在请求 src 资源时会将其指向的资源下载并应用到文档内，例如 js 脚本，img 图片和 frame 等元素。 

  ```js
  <script src =”js.js”></script>
  ```

- href 是 Hypertext Reference 的缩写，指向网络资源所在位置，建立和当前元素（锚点）或当前文档（资源）之间的链接。

  

### 2.对HTML语义化的理解

**语义化是指根据内容的结构化（内容语义化），选择合适的标签（代码语义化）。**

语义化的优点如下：

- 对机器友好，带有语义的文字表现力丰富，更适合搜索引擎的爬虫爬取有效信息，**有利于SEO**。除此之外，语义类还支持读屏软件，根据文章可以自动生成目录；
- 对开发者友好，使用语义类标签增强了**代码可读性**，结构更加清晰，开发者能清晰的看出网页的结构，便于团队的开发与维护。



### 3.DOCTYPE(文档类型) 的作用

它的目的是**告诉浏览器（解析器）应该以什么样（html或xhtml）的文档类型定义**来解析文档



### 4.常用的meta标签有哪些

1. `charset`，用来描述HTML文档的编码类型：

   ```html
   <meta charset="UTF-8" >
   ```

2.  `keywords`，页面关键词：

   ```html
   <meta name="keywords" content="关键词" />
   ```

3. `description`，页面描述：

   ```html
   <meta name="description" content="页面描述内容" />
   ```

4. `refresh`，页面重定向和刷新：

   ```html
   <meta http-equiv="refresh" content="0;url=" />
   ```

5. `viewport`，适配移动端，可以控制视口的大小和比例：

   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
   ```

6. 搜索引擎索引方式：

   ```html
   <meta name="robots" content="index,follow" />
   ```



### 5.img的srcset属性的作用？

响应式页面中经常用到根据屏幕密度设置不同的图片。这时就用到了 img 标签的srcset属性。srcset属性用于设置不同屏幕密度下，img 会自动加载不同的图片。用法如下：

```html
<img src="image-128.png" srcset="image-256.png 2x" />
```



### 6.HTML5的离线储存怎么使用，它的工作原理是什么

1. 应用缓存Application Cache(已弃用)

   写`<html lang="en" manifest="index.manifest">`，然后创建一个manifest文件，写要存储的资源。

2. Service Workers 和 Cache API 

   在入口文件写注册Service Worker，然后在同级的目录下添加service-worker.js；在service-worker.js写入要存储的资源和监听事件。



### 7.iframe的使用

在网页嵌入另一个网页

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Iframe Example</title>
</head>
<body>
  <h1>Embedding an External Webpage</h1>
  <iframe src="https://www.example.com" width="600" height="400" title="Example Website"></iframe>
</body>
</html>
```

**优点：**

- 用来加载速度较慢的内容（如广告）
- 可以使脚本可以并行下载
- 可以实现跨子域通信

**缺点：**

- iframe 会阻塞主页面的 onload 事件
- 无法被一些搜索引擎索识别
- 会产生很多页面，不容易管理



### 8.Canvas和SVG的区别

​	canvas按像素渲染，svg按xml绘制，所以canvas缩放会更模糊，但是动态效果更好，svg则反之。



### 9.`<head>` 标签有什么作用，其中什么标签必不可少？

`<head>`标签用于定义文档的头部，它是所有头部元素的容器。`<head>`中的元素可以引用脚本、指示浏览器在哪里找到样式表、提供元信息等。
`<title>`是必不可少的。（刚刚试了一下没有问题，可以不写）



## CSS篇

### 1.CSS选择器及其优先级

对于选择器的**优先级**：

- 标签选择器、伪元素选择器：1；
- 类选择器、伪类选择器、属性选择器：10；
- id 选择器：100；
- 内联样式：1000



### 2.隐藏元素的方法有哪些

- **display: none**：渲染树不会包含该渲染对象，因此该元素不会在页面中占据位置，也不会响应绑定的监听事件。
- **visibility: hidden**：元素在页面中仍占据空间，但是不会响应绑定的监听事件。
- **opacity: 0**：将元素的透明度设置为 0，以此来实现元素的隐藏。元素在页面中仍然占据空间，并且能够响应元素绑定的监听事件。
- **position: absolute**：通过使用绝对定位将元素移除可视区域内，以此来实现元素的隐藏。
- **z-index: 负值**：来使其他元素遮盖住该元素，以此来实现隐藏。
- **clip/clip-path** ：使用元素裁剪的方法来实现元素的隐藏，这种方法下，元素仍在页面中占据位置，但是不会响应绑定的监听事件。
- **transform: scale(0,0)**：将元素缩放为 0，来实现元素的隐藏。这种方法下，元素仍在页面中占据位置，但是不会响应绑定的监听事件。



### 3.伪元素和伪类选择器的区别和作用

- 伪元素：用于创建一些不在DOM树中的元素，并为其添加样式。

  ```css
  p::before {content:"第一章：";}
  p::after {content:"Hot!";}
  p::first-line {background:red;}
  p::first-letter {font-size:30px;}
  ```

- 伪类选择器：将特殊的效果添加到特定选择器上。它是已有元素上添加类别的，不会产生新的元素。

  ```css
  a:hover {color: #FF00FF}
  p:first-child {color: red}
  ```

  

### 4.对盒模型的理解

标准盒模型和IE盒模型的区别在于设置width和height时，所对应的范围不同：

- 标准盒模型的width和height属性的范围只包含了content，
- IE盒模型的width和height属性的范围包含了border、padding和content。



### 5.为什么有时候用translate来改变位置而不是定位？

transform:translate(x,y)文档上面提到过transform只会引起合成线程的最后一步**合成**，并不会重新生成layout树，也就是不会引起reflow。



### 6.对 CSSSprites 的理解

也就是雪碧图，把所有的小图标放在一个大图里面，这样的话请求资源只要请求一张大图就行了。



### 7.什么是物理像素，逻辑像素和像素密度

物理像素：就是真实的手机像素

逻辑像素：简单的理解为css像素

在高倍屏上，1逻辑像素等于多个物理像素



### 8.单行、多行文本溢出隐藏

单行文本溢出

```css
overflow: hidden;            // 溢出隐藏
text-overflow: ellipsis;      // 溢出用省略号显示
white-space: nowrap;         // 规定段落中的文本不进行换行
```

多行文本溢出

```css
overflow: hidden;            // 溢出隐藏
text-overflow: ellipsis;     // 溢出用省略号显示
display:-webkit-box;         // 作为弹性伸缩盒子模型显示。
-webkit-box-orient:vertical; // 设置伸缩盒子的子元素排列方式：从上到下垂直排列
-webkit-line-clamp:3;        // 显示的行数
```



### 9.如何判断元素是否到达可视区域 

以图片显示为例：

- `window.innerHeight` 是浏览器可视区的高度；
- `document.body.scrollTop || document.documentElement.scrollTop` 是浏览器滚动的过的距离；
- `imgs.offsetTop` 是元素顶部距离文档顶部的高度（包括滚动条的距离）；
- 内容达到显示区域的：`img.offsetTop < window.innerHeight + document.body.scrollTop;`



### 10.定位与浮动

- 给父级div定义`height`属性
- 最后一个浮动元素之后添加一个空的div标签，并添加`clear:both`样式
- 包含浮动元素的父级标签添加`overflow:hidden`或者`overflow:auto`
- 使用 :after 伪元素。



### 11.对BFC的理解，如何创建BFC

块格式化上下文（Block Formatting Context，BFC）是Web页面的可视化CSS渲染的一部分，是布局过程中生成块级盒子的区域，也是浮动元素与其他元素的交互限定区域。

**创建BFC的条件：**

- 元素设置浮动：float 除 none 以外的值；
- 元素设置绝对定位：position (absolute、fixed)；
- display 值为：inline-block、table-cell、table-caption、flex等；
- overflow 值为：hidden、auto、scroll；



**BFC的作用：**

- **解决margin的重叠问题**：由于BFC是一个独立的区域，内部的元素和外部的元素互不影响，将两个元素变为两个BFC，就解决了margin重叠的问题。
- **解决高度塌陷的问题**：在对子元素设置浮动后，父元素会发生高度塌陷，也就是父元素的高度变为0。解决这个问题，只需要把父元素变成一个BFC。常用的办法是给父元素设置`overflow:hidden`。



### 12.什么是margin重叠问题？如何解决？

两个**块级元素**的上外边距和下外边距可能会合并（折叠）为一个外边距，其大小会取其中外边距值大的那个，这种行为就是外边距折叠。需要注意的是，**浮动的元素和绝对定位**这种脱离文档流的元素的外边距不会折叠。重叠只会出现在**垂直方向**。

触发BFC就好了。



### 13. 元素的层叠顺序

1. 背景和边框：建立当前层叠上下文元素的背景和边框。
2. 负的z-index：当前层叠上下文中，z-index属性值为负的元素。
3. 块级盒：文档流内非行内级非定位后代元素。
4. 浮动盒：非定位浮动元素。
5. 行内盒：文档流内行内级非定位后代元素。
6. z-index:0：层叠级数为0的定位元素。
7. 正z-index：z-index属性值为正的定位元素。



### 14.画一条0.5px的线

- **采用transform: scale()的方式**，该方法用来定义元素的2D 缩放转换：

  ```css
  transform: scale(1,0.5);
  ```

- **采用meta viewport的方式**

  ```css
  <meta name="viewport" content="width=device-width, initial-scale=0.5, minimum-scale=0.5, maximum-scale=0.5"/>
  ```

- **同理画一条1px的线在2倍屏上**

  简单来说就是用伪元素+transform

  ```css
  .scale-1px::after{
    content: '';
    position: absolute;
    bottom: 0;
    background: #000;
    width: 100%;
    height: 1px;
    -webkit-transform: scaleY(0.5);
    transform: scaleY(0.5);
    -webkit-transform-origin: 0 0;
    transform-origin: 0 0;
  }
  ```




## JS篇

### 1.JS有哪些数据类型

#### 1-1.基本数据类型

1. **Number**:

   表示数字，包括整数和浮点数。例如，`42` 或 `3.14`。

2. **String**:

   表示文本数据。例如，`"Hello, World!"` 或 `'JavaScript'`。

3. **Boolean**:

   表示布尔值，只有两个可能的值：`true` 和 `false`。

4. **Undefined**:

   表示一个变量未被赋值。例如，`let x;` 中的 `x` 是 `undefined`。

5. **Null**:

   表示一个空值或不存在的对象。例如，`let y = null;`。

6. **Symbol**:

   表示一个独一无二且不可变的基本数据类型，通常用于对象属性的唯一标识符。例如，`let sym = Symbol();`。

7. **BigInt**:

   表示任意精度的整数，可以处理超过 `Number` 类型所能表示的最大数字。例如，`let bigInt = 1234567890123456789012345678901234567890n;`。

#### 1-2.复杂数据类型

1. **Object**:

   用于存储键值对和更复杂的实体。例如，`let obj = { name: "Alice", age: 25 };`。

2. **Array**:

   一种特殊的对象，用于存储有序集合。例如，`let arr = [1, 2, 3];`。

3. **Function**:

   一种特殊的对象，用于定义可调用的代码块。例如，`function greet() { console.log("Hello!"); }`。

4. **Date**:

   用于处理日期和时间的对象。例如，`let date = new Date();`。

5. **RegExp**:

   用于匹配字符串模式的对象（正则表达式）。例如，`let regex = /abc/;`。



### 2.数据类型检测的方式有哪些

1. **typeof**

   其中数组、对象、null都会被判断为object，其他判断都正确。

   ```js
   console.log(typeof 2);               // number
   console.log(typeof true);            // boolean
   console.log(typeof 'str');           // string
   console.log(typeof []);              // object    
   console.log(typeof function(){});    // function
   console.log(typeof {});              // object
   console.log(typeof undefined);       // undefined
   console.log(typeof null);            // object
   ```

2. **instanceof**

   `instanceof`可以正确判断对象的类型，其内部运行机制是**判断在其原型链中能否找到该类型的原型**，但是不**能用来判断基本数据类型**。

   ```js
   console.log(2 instanceof Number);                    // false
   console.log(true instanceof Boolean);                // false 
   console.log('str' instanceof String);                // false 
    
   console.log([] instanceof Array);                    // true
   console.log(function(){} instanceof Function);       // true
   console.log({} instanceof Object);                   // true
   ```

3. **constructor**

   ```js
   console.log((2).constructor === Number); // true
   console.log((true).constructor === Boolean); // true
   console.log(('str').constructor === String); // true
   console.log(([]).constructor === Array); // true
   console.log((function() {}).constructor === Function); // true
   console.log(({}).constructor === Object); // true
   ```

   `constructor`有两个作用，一是判断数据的类型，二是对象实例通过 `constrcutor` 对象访问它的构造函数。需要注意，如果创建一个对象来改变它的原型，`constructor`就不能用来判断数据类型了：

   ```js
   function Fn(){};
    
   Fn.prototype = new Array();
    
   var f = new Fn();
    
   console.log(f.constructor===Fn);    // false
   console.log(f.constructor===Array); // true
   ```

4. **Object.prototype.toString.call()**

   `Object.prototype.toString.call()` 使用 Object 对象的原型方法 toString 来判断数据类型

   ```js
   var a = Object.prototype.toString;
    
   console.log(a.call(2));
   console.log(a.call(true));
   console.log(a.call('str'));
   console.log(a.call([]));
   console.log(a.call(function(){}));
   console.log(a.call({}));
   console.log(a.call(undefined));
   console.log(a.call(null));
   ```



### 3.判断数组的方式有哪些

1. 通过Object.prototype.toString.call()做判断

   ```js
   Object.prototype.toString.call(obj).slice(8,-1) === 'Array';
   ```

2. 通过原型链做判断

   ```js
   obj.__proto__ === Array.prototype;
   ```

3. Array.isArrray(obj);

   ```js
   Array.isArrray(obj);
   ```

4. 通过instanceof做判断

   ```js
   obj instanceof Array
   ```

5. 通过Array.prototype.isPrototypeOf

   ```js
   Array.prototype.isPrototypeOf(obj)
   ```

   

### 4.原型和原型链

- 原型

  每个函数都有`prototype`属性，称之为原型或者原型对象。原型可以存放一些属性和方法，共享给实例对象使用，原型可以继承

- 原型链

  每个对象都有`__proto__`属性，这个属性指向他的原型对象，原型对象也是对象，也有`__proto__`属性，这个属性指向`Object`的原型，这样一层一层的形成的链式结构叫做原型链，最顶层的是找不到则返回`null`。

  另外，`函数本身也是对象`，所有的函数都是通过 `new Function()`得来的，所以函数也有`__proto__`属性，指向`Function`的原型对象，`Fcuntion`的原型对象再往上的`__proto__`又指向`Object`的原型对象。



### 5.intanceof 操作符的实现原理及实现

```js
function myInstanceof(left, right) {
  // 获取对象的原型
  let proto = Object.getPrototypeOf(left)
  // 获取构造函数的 prototype 对象
  let prototype = right.prototype; 
 
  // 判断构造函数的 prototype 对象是否在对象的原型链上
  while (true) {
    if (!proto) return false;
    if (proto === prototype) return true;
    // 如果没有找到，就继续从其原型上找，Object.getPrototypeOf方法用来获取指定对象的原型
    proto = Object.getPrototypeOf(proto);
  }
}
```



### 6.为什么0.1+0.2 ! == 0.3，如何让其相等

做数学运算的时候用第三方库可以避免。



### 7. typeof NaN 的结果是什么

number



###  8.|| 和 && 操作符的返回值

- &&

  遇到false立即返回false，否则就一直运行到最后一个。

- ||

  遇到true立即返回true，否则就一直运行到最后一个。



### 9.Object.is()

使用 Object.is 来进行相等判断时，一般情况下和三等号的判断相同，它处理了一些特殊的情况，比如 -0 和 +0 不再相等，两个 NaN 是相等的。

```js
// NaN 与 NaN
console.log(Object.is(NaN, NaN)); // true
console.log(NaN === NaN); // false

// -0 与 +0
console.log(Object.is(-0, +0)); // false
console.log(-0 === +0); // true
```



### 10.什么是 JavaScript 中的包装类型？

在 JavaScript 中，基本类型是没有属性和方法的，但是为了便于操作基本类型的值，在调用基本类型的属性或方法时 JavaScript 会在后台隐式地将基本类型的值转换为对象，如：

```js
const a = "abc";  //其实就是进行了new String("abc")
a.length; // 3
a.toUpperCase(); // "ABC"
```



### 11.object.assign和扩展运算法是深拷贝还是浅拷贝，两者区别

都是浅拷贝



### 12.如何判断一个对象是空对象

1. 使用JSON自带的.stringify方法来判断：

   ```js
   if(Json.stringify(Obj) == '{}' ){
       console.log('空对象');
   }
   ```

2. 使用ES6新增的方法Object.keys()来判断：

   ```js
   if(Object.keys(Obj).length < 0){
       console.log('空对象');
   }
   ```



### 13.var let const的区别

1. **作用域**：
   - `var` 具有函数作用域或全局作用域。
   - `let` 和 `const` 具有块级作用域。
2. **提升（Hoisting）**：
   - `var` 声明的变量会被提升到作用域的顶部，但初始化不会被提升。
   - `let` 和 `const` 声明的变量会被提升，但在声明之前不能访问（暂时性死区）。
3. **重复声明**：
   - `var` 允许在同一作用域内重复声明同一个变量。
   - `let` 和 `const` 不允许在同一作用域内重复声明同一个变量。
4. **初始化和赋值**：
   - `var` 声明的变量可以在声明后再赋值。
   - `let` 声明的变量可以在声明后再赋值。
   - `const` 声明的变量必须在声明时初始化，并且不能再被赋值。





### 16.箭头函数和普通函数的区别

1. 箭头函数的形式更加简洁。
2. 箭头函数没有自己的this，继承自定义时的外层作用域。
3. 箭头函数继承来的this指向永远不会改变，即使是用了call()  aplly()  bind()方法也不能改变。
4. 箭头函数没有自己的arguments。
5. 箭头函数没有prototype。



### 15. 如果new一个箭头函数的会怎么样

先来看看new操作符做了什么

1. 创建一个对象。
2. 将构造函数的作用域赋给新对象（也就是将对象的`__proto__`属性指向构造函数的prototype属性）。
3. 将构造函数的 `this` 绑定到新对象上，并执行构造函数。
4. 返回新对象，除非构造函数显式返回一个对象。

箭头函数没有自己的prototype，没有自己的this。



### 16.JS中this的指向问题

1. **全局上下文**：指向全局对象（`window` 或 `global`）。
2. **普通函数**：在非严格模式下指向全局对象，严格模式下为 `undefined`。
3. **方法调用**：指向调用该方法的对象。
4. **箭头函数**：继承自定义时的外层作用域。
5. **构造函数**：指向新创建的实例对象。
6. **`call`、`apply` 和 `bind`**：显式地设置 `this` 指向。
7. **类的方法**：指向类的实例。



### 17.手写一个new

```js
function myNew(constructor, ...args) {
  // 1. 创建一个新的空对象
  const newObj = Object.create(constructor.prototype);

  // 2. 绑定 `this` 并执行构造函数
  const result = constructor.apply(newObj, args);

  // 3. 如果构造函数返回一个对象，则返回该对象；否则返回新对象
  return result instanceof Object ? result : newObj;
}
```



### 18.Object.create

`Object.create(proto, propertiesObject)`：创建一个新对象，并将其原型设置为 `proto`，同时定义新对象的属性。

```js
const Person = function(name){
	this.name = name
}
cosnt zs = Object.create(Person.prototype,'zs')
Person.call(zs,'张三')
```



### 19.map和Object的区别

`Map` 和 `Object` 是 JavaScript 中用于存储键值对的两种数据结构。虽然它们有很多相似之处，但也有一些重要的区别。以下是它们的主要区别和各自的特点：

1. 键的类型

   - **Object**：键必须是字符串或符号。即使你使用其他类型作为键，它们也会被强制转换为字符串。
   - **Map**：键可以是任意类型，包括对象、函数和基本类型。

2. 键值对的顺序

   - **Object**：没有保证键值对的存储顺序，尽管现代 JavaScript 引擎通常会按照插入顺序遍历对象的键。
   - **Map**：键值对按照插入顺序存储，并且遍历时也会按照插入顺序返回。

3. 属性和方法

   - **Object**：对象的键值对通过普通属性访问。对象还继承了 `Object.prototype` 上的方法和属性，这可能会导致键名冲突。
   - **Map**：提供了专门的方法来操作键值对，如 `set`、`get`、`has`、`delete` 和 `clear`。`Map` 不继承任何原型方法，因此没有键名冲突的问题。
     - **size**： `map.size` 返回Map结构的成员总数。
     - **set(key,value)**：设置键名key对应的键值value，然后返回整个Map结构，如果key已经有值，则键值会被更新，否则就新生成该键。（因为返回的是当前Map对象，所以可以链式调用）
     - **get(key)**：该方法读取key对应的键值，如果找不到key，返回undefined。
     - **has(key)**：该方法返回一个布尔值，表示某个键是否在当前Map对象中。
     - **delete(key)**：该方法删除某个键，返回true，如果删除失败，返回false。
     - **clear()**：map.clear()清除所有成员，没有返回值。
     - **keys()**：返回键名的遍历器。
     - **values()**：返回键值的遍历器。
     - **entries()**：返回所有成员的遍历器。
     - **forEach()**：遍历Map的所有成员。

   

### 20.WeakMap

WeakMap 对象也是一组键值对的集合，其中的键是弱引用的。**其键必须是对象**，原始数据类型不能作为key值，而值可以是任意的。

他也没有遍历器，他只有`set(key) get(key) has(key) delete(key)`这四种方法。

```js
        let obj = {name:"zs"}
        const map2 = new WeakMap([[obj,"Pepole"]])
        obj = null//解除了引用
        console.log(map2);// key会消失，因为obj没有引用他了，所以就被垃圾回收机制处理了。
```





### 21.类数组对象

说白了就是一个对象

```js
const arrayLike = {
  0: 'first element',
  1: 'second element',
  2: 'third element',
  length: 3
};
```

怎么把这个对象变成数组

```js
//说白就是把this指向了arryLike，然后这些方法刚好需要下标和长度，arrayLike刚好满足了条件，克隆了一个数组出来了

Array.prototype.slice.call(arrayLike);
Array.prototype.splice.call(arrayLike, 0);
Array.prototype.concat.apply([], arrayLike);
Array.from(arrayLike);
```



### 22. ES6模块与CommonJS模块有什么区别？

- ES6 模块
  - **语法**：使用 `import` 和 `export`。
  - **加载方式**：编译时确定依赖关系，异步加载。
  - **严格模式**：默认严格模式，顶层 `this` 是 `undefined`。
  - **用途**：现代前端开发，支持现代浏览器和工具链。
- CommonJS 模块
  - **语法**：使用 `require` 和 `module.exports`。
  - **加载方式**：运行时确定依赖关系，同步加载。
  - **严格模式**：默认非严格模式（可以手动启用），顶层 `this` 是 `module.exports`。
  - **用途**：主要用于 Node.js 环境。



### 23.for...of  for...in  forEach  map的区别

- for...of

  用来获取数组的值，用在一般对象上会报错（没有迭代器）。

- for...in

  用来获取数组或者对象的key。

- forEach

  用于数组，操作数组中的元素，会改变原数组。

- map

  用于数组，操作数组中的元素，不会改变原数组，返回一个新数组。



### 24.Set对象

`Set` 是一种集合数据结构，它允许你存储任何类型的唯一值，无论是原始值还是对象引用。

有一些常用的方法，如 `add`、`delete`、`has` 和 `clear`。和`Map`挺像的。

```js
const mySet = new Set();
mySet.add('随便')
mySet.add('加一点')
console.log(mySet);// Set { '随便', '加一点' }
```

同理WeakSet和WeakMap差不多，都是弱引用，就不过多说了。



### 25.for of怎么样才能用于对象（iterator）

因为对象没有iterator，数组等能够遍历就是因为有iterator。

函数中返回一个next方法，next方法返回一个value和done。

```js
var obj = {
    a: 1,
    b: 2,
    c: 3
};

obj[Symbol.iterator] = function () {
    var keys = Object.keys(this)
    var count = 0
    return {
        next() {
            if (count < keys.length) {
                return { value: obj[keys[count++]], done: false }
            } else {
                return { value: undefined, done: true }
            }
        }
    }
}

for (const value of obj) {
    console.log(value);
}
```



### 26. Ajax、Axios、Fetch的区别

- Ajax

  是指一种技术，**不重新加载整个网页但做到了数据交换**。Axios和Fetch是实现这种技术的方式。

- Fetch

  浏览器内置的方法，用于实现Ajax，基于 Promise但不是对XMLHttpRequest的封装，语法简洁，但不支持进度事件。但是没有请求拦截器和响应拦截器，还要自己处理JSON，也不会抛出网络错误。

- Axios

  是一种第三方库，用于实现Ajax。基于 Promise对XMLHttpRequest的封装。



### 27.闭包

**闭包是指有权访问另一个函数作用域中变量的函数**

```js
function fn1() {
    const a = 'I am outside!';

    function fn2() {
        console.log(a);
    }
    return fn2;
}

const myClosure = fn1();
myClosure(); // 输出: I am outside!
```

运用就是防抖节流

```js
//防抖函数

function debounce(func, wait) {
  let timeout;

  return function(...args) {
    const context = this;

    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(context, args), wait);
  };
}
```

节流

```js
function throttle(func, wait) {
  let lastTime = 0;

  return function(...args) {
    const now = Date.now();
    if (now - lastTime >= wait) {
      lastTime = now;
      func.apply(this, args);
    }
  };
}
```



### 28.对执行上下文的理解

执行上下文（Execution Context）是 **JavaScript 代码在运行时评估和执行的环境**。每当函数被调用时，JavaScript 引擎会创建一个新的执行上下文。

**执行上下文的类型**

1. **全局执行上下文**：这是默认的、最基础的执行上下文。任何不在函数内部的代码都在全局执行上下文中执行。
2. **函数执行上下文**：每当一个函数被调用时，都会为该函数创建一个新的执行上下文。
3. **Eval 执行上下文**：代码在 `eval` 函数中执行时，会有其自己的执行上下文。（eval函数是运行代码的）



**执行上下文的生命周期主要分为三个阶段：**

1. 创建阶段：
   - **变量对象（Variable Object, VO）**：创建变量对象，包含函数的参数、内部变量和函数声明。
   - **作用域链（Scope Chain）**：创建作用域链，以便变量和函数能在当前上下文中被访问。
   - **this 绑定**：确定 this 的值。
2. 执行阶段：
   - **变量赋值**：执行代码，变量赋值和函数引用。
3. 销毁阶段：
   - 执行上下文被销毁，内存被释放。



### 29.Promise、Async/Await 的区别

- **Promise**

  Promise本身是**同步的立即执行函数**，但是Promise的回调（通过 `.then()` 和 `.catch()` 添加的）是异步的。

- **async/await**

  async 函数返回一个 Promise 对象，当函数执行的时候，一旦遇到 await 就会先返回，等到触发的异步操作完成，再执行函数体内后面的语句。可以理解为，是让出了线程，跳出了 async 函数体。



### 30.Promise的理解

Promise 对象是**异步编程的一种解决方案**。Promise 是一个**构造函数**，接收一个**函数作为参数**，返回一个 **Promise 实例**。一个 Promise 实例有三种状态，分别是**pending**、**resolved** 和 **rejected**，分别代表了进行中、已成功和已失败。**实例的状态只能由 pending 转变 resolved 或者rejected 状态**，并且状态一经改变，就凝固了，无法再被改变了。

#### 30-1.基本用法

```js
const promise = new Promise(function(resolve, reject) {
  // ... some code
  if (/* 异步操作成功 */){
    resolve(value);
  } else {
    reject(error);
  }
});
```

#### 30-2.Promise方法

- then()

  ```js
  promise.then(function(value) {
    // success
  }, function(error) {
    // failure
  });
  ```

- catch()

  romise对象除了有then方法，还有一个catch方法，该方法相当于`then`方法的第二个参数，指向`reject`的回调函数。不过`catch`方法还有一个作用，就是在执行`resolve`回调函数时，如果出现错误，抛出异常，不会停止运行，而是进入`catch`方法中。

  ```js
  p.then((data) => {
       console.log('resolved',data);
  },(err) => {
       console.log('rejected',err);
       }
  ); 
  p.then((data) => {
      console.log('resolved',data);
  }).catch((err) => {
      console.log('rejected',err);
  });
  ```

- all()

  `all`方法可以完成并行任务， 它接收一个数组，数组的每一项都是一个`promise`对象。当数组中所有的`promise`的状态都达到`resolved`的时候，`all`方法的状态就会变成`resolved`，如果有一个状态变成了`rejected`，那么`all`方法的状态就会变成`rejected`。

  ```js
  javascript
  let promise1 = new Promise((resolve,reject)=>{
  	setTimeout(()=>{
         resolve(1);
  	},2000)
  });
  let promise2 = new Promise((resolve,reject)=>{
  	setTimeout(()=>{
         resolve(2);
  	},1000)
  });
  let promise3 = new Promise((resolve,reject)=>{
  	setTimeout(()=>{
         resolve(3);
  	},3000)
  });
  Promise.all([promise1,promise2,promise3]).then(res=>{
      console.log(res);
      //结果为：[1,2,3] 
  })
  ```

- race()

  `race`方法和`all`一样，接受的参数是一个每项都是`promise`的数组，但是与`all`不同的是，当最先执行完的事件执行完之后，就直接返回该`promise`对象的值。如果第一个`promise`对象状态变成`resolved`，那自身的状态变成了`resolved`；反之第一个`promise`变成`rejected`，那自身状态就会变成`rejected`。

  ```js
  let promise1 = new Promise((resolve,reject)=>{
  	setTimeout(()=>{
         reject(1);
  	},2000)
  });
  let promise2 = new Promise((resolve,reject)=>{
  	setTimeout(()=>{
         resolve(2);
  	},1000)
  });
  let promise3 = new Promise((resolve,reject)=>{
  	setTimeout(()=>{
         resolve(3);
  	},3000)
  });
  Promise.race([promise1,promise2,promise3]).then(res=>{
  	console.log(res);
  	//结果：2
  },rej=>{
      console.log(rej)};
  )
  ```

- fianlly

  `finally`方法用于指定不管 Promise 对象最后状态如何，都会执行的操作。该方法是 ES2018 引入标准的。

  ```js
  promise
  .then(result => {···})
  .catch(error => {···})
  .finally(() => {···});
  ```



### 31.面向对象

面向对象编程是一种强大且灵活的编程范式，它通过将数据和操作数据的方法封装在对象中，提供了一种自然且直观的方式来组织代码和解决问题。

#### 31-1.对象的创建方法

1. 直接写，网上说那么多我感觉都是废话。

   ```js
   //
   const obj1 = {}
   obj1.name = 'zs'
   //
   const obj2 = {name:'zs'}
   ```

2. `new Ｏbject()`

   ```js
   const obj3 = new Object()
   ```

   以上这两种方式我都觉的傻了吧唧的，干嘛分这么细。

   不用重复制造对象的情况下是可以的，如果需要批量造就不太方便。

   

3. 使用工厂模式创建对象

   口述一下就是定义一个函数接受参数，函数里面创造一个对象，并把参数传递进去当做属性。

   ```js
   <script>
           'use strict';
   
           // 使用工厂模式创建对象
           // 定义一个工厂方法
           function createObject(name){
               var o = new Object();
               o.name = name;
               o.sayName = function(){
                   alert(this.name);
               };
               return o;
           }
   
           var o1 = createObject('zhang');
           var o2 = createObject('li');
   
           //缺点：调用的还是不同的方法
           //优点：解决了前面的代码重复的问题
           alert(o1.sayName===o2.sayName);//false
   
       </script>
   
   ```

4. 用构造函数

   这他妈真的废话

5. 通过原型模式创建对象

   写一个构造函数，在构造函数的原型上写一些属性和方法，这样的话这个构造函数new出来的对象都有相同的属性和方法了。

   ```js
     <script>
           'use strict';
   
           /*
            *  原型模式创建对象
            */
           function Animal() { }
   
           Animal.prototype.name = 'animal';
           Animal.prototype.sayName = function () { alert(this.name); };
   
           var a1 = new Animal();
           var a2 = new Animal();
   
           a1.sayName();
   
           alert(a1.sayName === a2.sayName);//true
           alert(Animal.prototype.constructor);//function Animal(){}
           alert(Animal.prototype.constructor==Animal);//true
       </script>
   
   ```

6. 原型+构造函数

   在构造函数中放私有的属性，在原型上放公共的方法。

   ```js
   //混合创建 构造函数（可变）   原型（固定，公共，共享的）
     			function Student(name,age)
   			{
   				this.name = name;
   				this.age = age;
   				this.func = function()
   				{
   					console.log("敲代码")
   				}
   			}
   			Student.prototype.hobby = "学习";
   			Student.prototype.skill = function()
   			{
   				console.log("学习");
   			};
   			
   			var stu1 = new Student("张三",21);
   			
   			console.log(stu1);
   
   
   //特点：实例化对象有自己的一些属性和方法，Student的公共属性和方法放置在prototype中
   
   ```

7. 寄生模式

   也是废话，和工厂模式差不多的东西。

#### 31-2.实现对象继承的方式

这真的好多废话，无非是几种

1. 原型链继承

   就是把子对象的原型指向父对象的实例

   ```js
   function Parent() {
       this.name = 'Parent';
   }
   
   Parent.prototype.sayName = function() {
       console.log(this.name);
   };
   
   function Child() {
       this.age = 18;
   }
   
   Child.prototype = new Parent();
   
   const child = new Child();
   child.sayName();  // 输出: Parent
   console.log(child.age);  // 输出: 18
   ```

2. 借用构造函数

   把子构造函数中用call调用父构造函数。

   ```js
   function Parent(name) {
       this.name = name;
   }
   
   function Child(name, age) {
       Parent.call(this, name);
       this.age = age;
   }
   
   const child = new Child('John', 18);
   console.log(child.name);  // 输出: John
   console.log(child.age);  // 输出: 18
   ```

3. 使用class

   ```js
   class Parent {
       constructor(name) {
           this.name = name;
       }
   
       sayName() {
           console.log(this.name);
       }
   }
   
   class Child extends Parent {
       constructor(name, age) {
           super(name);
           this.age = age;
       }
   }
   
   const child = new Child('John', 18);
   child.sayName();  // 输出: John
   console.log(child.age);  // 输出: 18
   ```





## Vue

### 1.Vue的基本原理

1. 当一个Vue实例创建时，Vue会遍历data中的属性，用 Object.defineProperty（vue3.0使用proxy ）将它们转为 getter/setter，并且在内部追踪相关依赖，在属性被访问和修改时通知变化。
2. 每个组件实例都有相应的 watcher 程序实例，它会在组件渲染的过程中把属性记录为依赖，之后当依赖项的setter被调用时，会通知watcher重新计算，从而致使它关联的组件得以更新。



### 2.双向数据绑定的原理

1. **数据劫持（Data Hijacking）**

   Vue 使用 `Object.defineProperty()` 方法对数据对象的属性进行拦截和劫持。这样，当数据发生变化时，可以通知依赖这些数据的视图进行更新。

   ```js
   const data = { message: 'Hello, Vue!' };
   
   Object.keys(data).forEach(key => {
     let value = data[key];
     Object.defineProperty(data, key, {
       get() {
         console.log(`获取属性 ${key}`);
         return value;
       },
       set(newValue) {
         console.log(`设置属性 ${key} 为 ${newValue}`);
         value = newValue;
         // 通知依赖更新
       }
     });
   });
   ```

2. **发布-订阅模式（Publish-Subscribe Pattern）**

   在Vue中，每个响应式属性都有一个依赖（`Dep`）对象，存储所有依赖于该属性的订阅者（即观察者，`Watcher`）。当属性变化时，`Dep`会通知所有订阅者进行更新。

   **依赖收集（Dependency Collection）**

   当Vue实例化时，`Watcher`会读取数据属性，并将自己添加到该属性的依赖列表中。

   ```js
   class Dep {
     constructor() {
       this.subscribers = [];
     }
   
     addSub(sub) {
       this.subscribers.push(sub);
     }
   
     notify() {
       this.subscribers.forEach(sub => {
         sub.update();
       });
     }
   }
   
   class Watcher {
     constructor(obj, key, callback) {
       this.obj = obj;
       this.key = key;
       this.callback = callback;
       this.value = this.get();
     }
   
     get() {
       Dep.target = this;
       const value = this.obj[this.key];
       Dep.target = null;
       return value;
     }
   
     update() {
       const value = this.obj[this.key];
       this.callback(value);
     }
   }
   
   const data = { message: 'Hello, Vue!' };
   const dep = new Dep();
   
   Object.keys(data).forEach(key => {
     let value = data[key];
     Object.defineProperty(data, key, {
       get() {
         if (Dep.target) {
           dep.addSub(Dep.target);
         }
         return value;
       },
       set(newValue) {
         value = newValue;
         dep.notify();
       }
     });
   });
   
   // 使用观察者
   new Watcher(data, 'message', (newVal) => {
     console.log(`视图更新: ${newVal}`);
   });
   
   data.message = 'Hello, World!';  // 输出: 视图更新: Hello, World!
   ```

3. **模版编译和更新**

   Vue 的模版编译器会将模版编译成渲染函数，渲染函数会读取响应式数据并生成虚拟DOM。当数据变化时，`Watcher`会触发视图更新，新的虚拟DOM会和旧的虚拟DOM进行比较（diff算法），找到最小的差异，并只更新那些实际变化的部分。

4. **双向数据绑定**

   - **绑定输入事件**：监听表单元素的 `input` 事件，当用户输入时，更新数据模型。
   - **绑定视图更新**：当数据模型变化时，更新表单元素的值。

总结：首先数据劫持，用`Object.defineProperty()`给每个属性加上getter和setter。有一个watcher类，watcher在实例化的时候就会获取一次数据的值从而触getter，getter会把watcher添加进依赖Dep。Dep是用来管理watcher的，他有把watcher添加进管理列表`subscribers`的方法`addSub()`和通知方法`notify()`。当数据更新的时候，触发响应式数据的setter，就会调用Dep中的`notify()`，会通知`subscribers`中所有的watcher调用他们的`update()`方法进行更新。



### 3.使用 Object.defineProperty() 来进行数据劫持有什么缺点？

在对一些属性进行操作时，使用这种方法无法拦截，比如通过下标方式修改数组数据或者给对象新增属性，这都不能触发组件的重新渲染，因为 Object.defineProperty 不能拦截到这些操作。

在 Vue3.0 中已经不使用这种方式了，而是通过使用 Proxy 对对象进行代理，从而实现数据劫持。唯一的缺点是兼容性的问题，因为 Proxy 是 ES6 的语法。



### 4.computed和watch

- computed 计算属性 : 依赖其它属性值，并且 computed 的值有缓存，只有它依赖的属性值发生改变，下一次获取 computed 的值时才会重新计算 computed 的值。 
- watch 侦听器 : 更多的是**观察**的作用，**无缓存性**，类似于某些数据的监听回调，每当监听的数据变化时都会执行回调进行后续操作。 



### 5.slot是什么？有什么作用？原理是什么？

slot又名插槽，是**Vue的内容分发机制**，组件内部的模板引擎使用slot元素作为承载分发内容的出口。

- 默认插槽：又名匿名插槽，当slot没有指定name属性值的时候一个默认显示插槽，一个组件内只有有一个匿名插槽。
- 具名插槽：带有具体名字的插槽，也就是带有name属性的slot，一个组件可以出现多个具名插槽。
- 作用域插槽：默认插槽、具名插槽的一个变体，可以是匿名插槽，也可以是具名插槽，该插槽的不同点是在子组件渲染作用域插槽时，可以将子组件内部的数据传递给父组件，让父组件根据子组件的传递过来的数据决定如何渲染该插槽。

实现原理：当子组件vm实例化时，获取到父组件传入的slot标签的内容，存放在`vm.$slot`中，默认插槽为`vm.$slot.default`，具名插槽为`vm.$slot.xxx`，xxx 为插槽名，当组件执行渲染函数时候，遇到slot标签，使用`$slot`中的内容进行替换，此时可以为插槽传递数据，若存在数据，则可称该插槽为作用域插槽



### 6.如何保存页面的当前的状态

- 组件会被卸载

  1. 将状态存储在LocalStorage / SessionStorage
  2. 各种传值

- 组件不会被卸载

  直接把页面写成一个组件，控制他隐藏。

- `keep-alive`

  用`<keep-alive>`包裹，这个时候组件就不会执行一系列钩子函数，只会执行**activated**和**deactivated**

  ```html
  //组件中
  <keep-alive>
  	<router-view v-if="$route.meta.keepAlive"></router-view>
  </kepp-alive>
  ```

  ```js
  //router.js
  {
    path: '/',
    name: 'xxx',
    component: ()=>import('../src/views/xxx.vue'),
    meta:{
      keepAlive: true // 需要被缓存
    }
  },
  ```



### 7.常见的事件修饰符及其作用

- `.stop`：等同于 JavaScript 中的 `event.stopPropagation()` ，防止事件冒泡；
- `.prevent` ：等同于 JavaScript 中的 `event.preventDefault()` ，防止执行预设的行为（如果事件可取消，则取消该事件，而不停止事件的进一步传播）；
- `.capture` ：与事件冒泡的方向相反，事件捕获由外到内；
- `.self` ：只会触发自己范围内的事件，不包含子元素；
- `.once` ：只会触发一次。



### 8.v-model 是如何实现的，语法糖实际是什么？

就是语法糖，省略了一些代码，实际上就是绑定了一个事件，传递了一个prop。

- 用在表单上

  ```html
  <input v-model="sth" />
  //  等同于
  <input 
      v-bind:value="message" 
      v-on:input="message=$event.target.value"
  >
  //$event 指代当前触发的事件对象;
  //$event.target 指代当前触发的事件对象的dom;
  //$event.target.value 就是当前dom的value值;
  //在@input方法中，value => sth;
  //在:value中,sth => value;
  ```

- 用在自定义组件上

  ```js
  // 父组件
  <aa-input v-model="aa"></aa-input>
  // 等价于
  <aa-input v-bind:value="aa" v-on:input="aa=$event.target.value"></aa-input>
  ```

  在自定义组件中Vue2和Vue3有些许的不同，Vue2中`v-model`在同一个组件上只能用一次，想要用多次就用`.sync`。

  ```html
  <!-- Test.vue -->
  <CustomInput :firstName.sync="obj.firstName" :lastName.sync="obj.lastName"></CustomInput>
  
  <!-- CustomInput.vue -->
  <template>
    <div>
      <div><span>{{firstName}}</span><span @click="changeX">更改姓</span></div>
      <div><span>{{lastName}}</span><span @click="changeM">更改名</span></div>
    </div>
   </template>
  <script>
  export default {
    props: {
      firstName: String,
      lastName: String
    },
    methods: {
      changeX () {
        this.$emit('update:firstName', 'liu')
      },
      changeM () {
        this.$emit('update:lastName', 'yz')
      }
    }
  }
  </script>
  
  ```

  Vue3中可以用多次`v-model`，但是要定义一下名称

  ```html
    <!-- Test.vue -->
    <MyComponent
      v-model:first-name="first"
      v-model:last-name="last"
    />
    
    <!-- MyComponent.vue -->
    defineProps({
      firstName: String,
      lastName: String
    })
    
    defineEmits(['update:firstName', 'update:lastName'])
    </script>
    
    <template>
      <input
        type="text"
        :value="firstName"
        @input="$emit('update:firstName', $event.target.value)"
      />
      <input
        type="text"
        :value="lastName"
        @input="$emit('update:lastName', $event.target.value)"
      />
    </template>
  ```

  



### 9.data为什么是一个函数而不是对象

Vue组件可能存在多个实例，如果使用对象形式定义data，则会导致它们共用一个data对象，那么状态变更将会影响所有组件实例。



### 10.对keep-alive的理解，它是如何实现的，具体缓存的是什么？

把组件的实例添加到缓存里面，并且缓存它的key。当组件切换回来的时候会在cache对象中找到对应的实例，重新激活。



### 11.$nextTick 原理及作用

在 Vue 中，数据的变化会触发 DOM 更新，但这种更新是异步执行的，以便在同一个事件循环中多次数据修改只会触发一次 DOM 更新。`$nextTick` 方法允许你在 DOM 更新完成后执行代码，这对需要依赖最新 DOM 状态的操作非常有用。



### 12.Vue 中给 data 中的对象属性添加一个新的属性时会发生什么？如何解决？

视图不会有变化，除非用了api `$set()`

```html
<template> 
   <div>
      <ul>
         <li v-for="value in obj" :key="value"> {{value}} </li> 
      </ul> 
      <button @click="addObjB">添加 obj.b</button> 
   </div>
</template>

<script>
    export default { 
       data () { 
          return { 
              obj: { 
                  a: 'obj.a' 
              } 
          } 
       },
       methods: { 
          addObjB () { 
             this.$set(this.obj, 'b', 'obj.b')
          } 
      }
   }
</script>
```



### 13.Vue中封装的数组方法有哪些，其如何实现页面更新

`push(),pop(),shift(),unshift(),splice(),sort(),reverse()`

1. **创建 `arrayMethods` 对象**：首先，创建一个对象 `arrayMethods`，它继承自 `Array.prototype`，并对数组的变更方法进行重写。
2. **重写数组方法**：对每个需要重写的方法（如 `push`、`pop` 等），使用 `Object.defineProperty` 定义新的方法。在新的方法中，首先调用原始的数组方法，然后进行依赖通知。
3. **依赖通知**：重写的方法在执行原始操作后，会调用观察者的 `dep.notify()` 方法，通知所有依赖该数组的观察者，从而触发视图更新。
4. **观察新插入的元素**：对于 `push`、`unshift` 和 `splice` 方法，会对新插入的元素进行观察，以确保这些新元素也是响应式的。



### 14.Vue template 到 render 的过程

1. **模板解析和编译**
   - **模板解析（Parsing）**：将模板字符串解析成抽象语法树（AST）。
   - **优化（Optimization）**：标记静态节点和静态根节点，静态节点生成的DOM不会变化，以提升性能。
   - **代码生成（Code Generation）**：将优化后的 AST 转换成**渲染函数的代码字符串**。
2. **渲染函数执行和虚拟 DOM 生成**
   - 渲染函数在**组件实例的上下文中执行**，返回一个虚拟 DOM 树（VNode Tree）。
3. **虚拟 DOM 渲染成真实 DOM**
   - **初始渲染**：将虚拟 DOM 树转换为真实 DOM 元素，并插入到页面中。
   - **更新渲染**：在数据更新时，生成新的虚拟 DOM 树，与旧的虚拟 DOM 树进行比较（diff 算法），找出需要更新的部分，并进行最小量的 DOM 操作以更新视图。





### 15.Vue data 中某一个属性的值发生改变后，视图会立即同步执行重新渲染吗？

不会的，DOM的更新是异步的，会把所有的DOM更新事件放在一个队列里面，一起更新。



### 16.简述 mixin、extends 的覆盖逻辑

1. **生命周期钩子**：生命周期钩子（如 `created`、`mounted` 等）会合并成一个数组，所有的钩子函数会按顺序执行。先执行 `extends` 中的钩子函数，再执行 `mixin` 中的钩子函数，最后执行组件自身的钩子函数。
2. **数据（data）**：数据选项会进行递归合并。如果存在同名的属性，组件自身的数据属性会覆盖 `extends` 和 `mixin` 中的数据属性。注意，数据属性在合并时是浅合并。
3. **方法（methods）**：方法选项会合并成一个对象。如果存在同名的方法，组件自身的方法会覆盖 `extends` 和 `mixin` 中的方法。
4. **计算属性（computed）**：计算属性的合并逻辑与方法类似，同名的计算属性会被覆盖。
5. **其他选项**：其他选项（如 `components`、`directives` 等）会进行递归合并，组件自身的选项会优先覆盖 `extends` 和 `mixin` 中的选项。



总结就是，对于生命周期不同的钩子会按顺序执行，同一个钩子会先extends，再mixin，最后才是组件。对于其他的，同名的情况下组件自身的会覆盖mixin和extends的。



### 17.自定义指令

例如实现一个按钮防抖

```js
import Vue from 'vue';

Vue.directive('debounce', {
  bind(el, binding) {
    if (typeof binding.value !== 'function') {
      console.warn(`Expect a function, got ${typeof binding.value}`);
      return;
    }
    // 使用防抖函数包装传入的函数
    const debouncedFn = debounce(binding.value, binding.arg || 300);
    // 将防抖函数存储在元素的自定义属性中，以便在 unbind 钩子中可以访问
    el.__debouncedFn__ = debouncedFn;
    // 添加事件监听器
    el.addEventListener('click', debouncedFn);
  },
  unbind(el) {
    // 移除事件监听器
    el.removeEventListener('click', el.__debouncedFn__);
    // 删除自定义属性
    delete el.__debouncedFn__;
  }
});
```

- 全局注册

  ```Vue
  //写在main.js中
  
  Vue.directive('focus', {
    // 当绑定元素插入到 DOM 中时
    inserted(el) {
      el.focus();
    }
  });
  ```

- 局部注册

  ```Vue
  //写在组件内
  
  const MyComponent = {
    directives: {
      focus: {
        inserted(el) {
          el.focus();
        }
      }
    }
  };
  ```

自定义指令的生命周期：

1. **bind**: 只调用一次，指令第一次绑定到元素时调用。这是进行一次性初始化的好地方。
2. **inserted**: 被绑定元素插入父节点时调用（仅保证父节点存在，但不一定已被插入文档中）。
3. **update**: 所在组件的 VNode 更新时调用，但是可能发生在其子 VNode 更新之前。
4. **componentUpdated**: 指令所在组件的 VNode 及其子 VNode 全部更新后调用。
5. **unbind**: 只调用一次，指令与元素解绑时调用。



### 18.assets和static的区别

assets中的东西会打包，而static不会，所以已经第三方的资源文件可以放在static中，因为这些东西已经压缩处理过了不需要再处理一次。



### 19.Vue的性能优化有哪些

- 编码阶段
  - 尽量减少data中的数据，data中的数据都会增加getter和setter，会收集对应的watcher
  - v-if和v-for不能连用
  - 如果需要使用v-for给每项元素绑定事件时使用事件代理
  - SPA 页面采用keep-alive缓存组件
  - 在更多的情况下，使用v-if替代v-show
  - key保证唯一
  - 使用路由懒加载、异步组件
  - 防抖、节流
  - 第三方模块按需导入
  - 长列表滚动到可视区域动态加载
  - 图片懒加载
- SEO优化
  - 预渲染
  - 服务端渲染
- 打包优化
  - 压缩代码
  - Tree Shaking/Scope Hoisting
  - 使用cdn加载第三方模块
  - 多线程打包happypack
  - splitChunks抽离公共文件
  - sourceMap优化
- 用户体验
  - 骨架屏
  - 还可以使用缓存(客户端缓存、服务端缓存)优化、服务端开启gzip压缩等。



### 20.v-if和v-for哪个优先级更高？如果同时出现，应如何优化？

Vue2，Vue3两边不一样，但是总而言之不要一起用。如果需要先做判断再v-for，那就可以使用computed计算过后再v-for。



### 21.说一下Vue的生命周期

1. **beforeCreate（创建前）**：数据观测和初始化事件还未开始，此时 data 的响应式追踪、event/watcher 都还没有被设置，也就是说不能访问到data、computed、watch、methods上的方法和数据。
2. **created（创建后）** ：实例创建完成，实例上配置的 options 包括 data、computed、watch、methods 等都配置完成，但是此时渲染得节点还未挂载到 DOM，所以不能访问到 `$el` 属性。
3. **beforeMount（挂载前）**：在挂载开始之前被调用，相关的render函数首次被调用。实例已完成以下的配置：编译模板，把data里面的数据和模板生成html。此时还没有挂载html到页面上。
4. **mounted（挂载后）**：在el被新创建的 vm.$el 替换，并挂载到实例上去之后调用。实例已完成以下的配置：用上面编译好的html内容替换el属性指向的DOM对象。完成模板中的html渲染到html 页面中。此过程中进行ajax交互。
5. **beforeUpdate（更新前）**：响应式数据更新时调用，此时虽然响应式数据更新了，但是对应的真实 DOM 还没有被渲染。
6. **updated（更新后）** ：在由于数据更改导致的虚拟DOM重新渲染和打补丁之后调用。此时 DOM 已经根据响应式数据的变化更新了。调用时，组件 DOM已经更新，所以可以执行依赖于DOM的操作。然而在大多数情况下，应该避免在此期间更改状态，因为这可能会导致更新无限循环。该钩子在服务器端渲染期间不被调用。
7. **beforeDestroy（销毁前）**：实例销毁之前调用。这一步，实例仍然完全可用，`this` 仍能获取到实例。
8. **destroyed（销毁后）**：实例销毁后调用，调用后，Vue 实例指示的所有东西都会解绑定，所有的事件监听器会被移除，所有的子实例也会被销毁。该钩子在服务端渲染期间不被调用。
9. **特殊**：actived和deactived，是使用了`<keeep-alive>`包裹的组件独有的，分别对应消失和隐藏。



### 22.Vue 子组件和父组件执行顺序

**加载渲染过程：**

1. 父组件 beforeCreate
2. 父组件 created
3. 父组件 beforeMount
4. 子组件 beforeCreate
5. 子组件 created
6. 子组件 beforeMount
7. 子组件 mounted
8. 父组件 mounted

**更新过程：**

1. 父组件 beforeUpdate
2. 子组件 beforeUpdate
3. 子组件 updated
4. 父组件 updated

**销毁过程：**

1. 父组件 beforeDestroy
2. 子组件 beforeDestroy
3. 子组件 destroyed
4. 父组件 destoryed



### 23.组件通信

- 父传子

  在父组件中用`v-bind`传递数据，子组件用props接受。

- 字传父

  父组件中写一个方法用`v-on`绑定一个事件在子组件上，子组件用`$emit()`触发事件，数据以函数入参的方式传给父组件。

- 兄弟组件

  用EventBus全局事件总线传值。

- 祖先传后代

  1. 用provide / inject

     大致就是在祖先中写provide提供数据，后代用inject接受数据，但是不好用我感觉，还不如用eventBus。

  2. pinia / vuex

- 其他冷门的方法

  1. ref / $ref

     在子组件上标记ref，然后获取子组件实例，使用子组件的方法。

  2. $parent / $children

     已经不推荐用了，别用。



### 24.Vue-Router 的懒加载如何实现

正常写法

```js
import List from '@/components/list.vue'
const router = new VueRouter({
  routes: [
    { path: '/list', component: List }
  ]
})
```

1. 用箭头函数+import

   ```js
   const List = () => import('@/components/list.vue')
   const router = new VueRouter({
     routes: [
       { path: '/list', component: List }
     ]
   })
   ```

2. 使用箭头函数+require

   ```js
   const router = new Router({
     routes: [
      {
        path: '/list',
        component: resolve => require(['@/components/list'], resolve)
      }
     ]
   })
   ```

3. 使用webpack的require.ensure技术

   ```js
   // r就是resolve
   const List = r => require.ensure([], () => r(require('@/components/list')), 'list');
   // 路由也是正常的写法  这种是官方推荐的写的 按模块划分懒加载 
   const router = new Router({
     routes: [
     {
       path: '/list',
       component: List,
       name: 'list'
     }
    ]
   }))
   ```



### 25.hash路由和history路由

一个是修改#后面的hash值进行路由跳转，一个是修改.com/后面的路径，history路由要后台支持，比如修改NGINX的配置，禁止服务器自动匹配资源，将请求交给Vue来处理。

```
location / {
    root   html;
    try_files $uri /index.html;
}
```



### 26.如何定义动态路由？如何获取传过来的动态参数？

1. **param方式**
   - 配置路由格式：`/router/:id`
   - 传递的方式：在path后面跟上对应的值
   - 传递后形成的路径：`/router/123`
   - 通过 `$route.params.id` 获取传递的值
2. **query方式**
   - 配置路由格式：`/router`，也就是普通配置
   - 传递的方式：对象中使用query的key作为传递方式
   - 传递后形成的路径：`/route?id=123`
   - 通过$route.query 获取传递的值



### 27.Vue-router 路由钩子在生命周期的体现

- 全局钩子

  - router.beforeEach 全局前置守卫 进入路由之前
  - beforeResolve 全局解析守卫
  - router.afterEach 全局后置钩子 进入路由之后

  ```js
  router.beforeEach((to, from) => {  
     ...
  });
  
  router.afterEach((to, from) => {  
     ...
  });
  ```

  

- 组件内钩子

  - beforeRouteUpdate

    组件被复用但是地址有改变，比如说传参变了。

  - beforeRouteEnter

    ```js
    beforeRouteEnter(to, from, next) {      
        next(target => {        
            if (from.path == '/classProcess') {          
                target.isFromProcess = true        
            }      
        })    
    }
    ```

  - beforeRouteLeave 同上

- 单个路由钩子

  在路由表里面写的

  ```js
  export default [    
      {        
          path: '/',        
          name: 'login',        
          component: login,        
          beforeEnter: (to, from, next) => {          
              console.log('即将进入登录页面')          
              next()        
          }    
      }
  ]
  ```

假如说从A页面到B页面完整的顺序

beforeRouteLeave  beforeEach  beforeEnter  beforeRouteEnter  beforeResolve  afterEach 然后组件生命周期



### 28.params和query的区别

有两种方式写路由跳转，一种叫编程式导航，还有种叫声明式导航。

第一种params会以路径的形式在url中显示参数，第二种使用编程式导航写params，但是这种方式刷新会丢失参数，导致页面显示有问题。query传参参数会以查询参数的形式在url中显示参数。



### 29.Vuex

Vuex 实现了一个单向数据流，在全局拥有一个 State 存放数据，当组件要更改 State 中的数据时，必须通过 Mutation 提交修改信息， Mutation 同时提供了订阅者模式供外部插件调用获取 State 数据的更新。而当所有异步操作(常见于调用后端接口异步获取更新数据)或批量的同步操作需要走 Action ，但 Action 也是无法直接修改 State 的，还是需要通过Mutation 来修改State的数据。最后，根据 State 的变化，渲染到视图上。

1. **State**: Vuex 的状态存储是响应式的，当 `State` 中的数据变化时，依赖这些数据的组件会自动更新。
2. **Getters**: 用于派生 `State`，类似于计算属性。
3. **Mutations**: 是同步事务，用于更改 `State`。通过提交 `Mutation`，可以确保 `State` 的变化是可追踪的。
4. **Actions**: 可以包含异步操作，通过分发 `Action` 来提交 `Mutation`，使得 `State` 的变化是可预测的。



### 30.Vue2和Vu3的区别

Vue2使用Object.defineProperty，Vue3使用proxy，Vue3有setup模式，Vue2是选项是api（options api），Vue3是组合式api（composition api）。巴拉巴拉的。Vue2太过依赖于this。



### 31. DIFF算法的原理

**主要流程**：

1. **初步对比**：

   - 从根节点开始，递归地比较新旧虚拟 DOM 树的每个节点。
   - 如果节点类型不同，直接替换整个节点。
   - 如果节点类型相同，则继续比较节点的属性和子节点。

2. **更新属性**：

   - 对比新旧节点的属性，找出不同并进行更新。
   - 新增或删除属性。
   - 更新已有属性的值。

3. **处理子节点**：

   - 使用 Keyed Diff 算法，通过节点的 `key` 属性唯一标识每个节点，从而提高比较效率。

     主要是建立了一个旧子节点的`key-index`映射表，方便快速判断子节点是否存在，定位子节点。（oldKeyToIndex列表，输入新子节点的key就可判断了。）

   - 双端比较用于进一步优化子节点的更新，减少节点的移动次数。

   - 具体来说，双端比较通过从头和尾同时进行对比，尽可能减少需要移动的节点数量。

     假如说就叫旧子节点list，新子节点list，还有对应的头尾指针；后面的判断如果是true就调用更新函数；先比较旧头部节点和新头部节点的key，再比较旧尾节点和新尾节点的key，再旧头和新尾，再旧尾和新头；还没有就直接查找，找不到就立即插入新指针的位置，找到了就根据key获取旧元素的index，插入当前的位置。



### 32.通过路由传递props（少见）

通过配置路由时设定props

```js
const routes = [
  {
    path: '...',
    name: '...',
    component: ...,
    props: true //就是这里
  }
];
```

有三种模式：

- 布尔值`true`

  会将params作为props传给组件，组件可以直接接受这个props，props的key就是占位符，比如`/destination/:user`，那组件接受props就是user。

- 对象

  只能写死，把这个对象传给组件

  ```js
  const routes = [
    {
      path: '/destination',
      name: 'destination',
      component: DestinationComponent,
      props: { user: 'JohnDoe' }
    }
  ];
  
  //组件接受的props就是user
  ```

- 函数

  这种方法比较灵活，能同时传query形式的参数也能传递params，也最推荐。

  ```js
  const routes = [
    {
      path: '/destination/:user',
      name: 'destination',
      component: DestinationComponent,
      props: route => ({ user: route.params.user, isAdmin: route.query.admin === 'true' })
    }
  ];
  ```



## 小程序

### 1.小程序组件通信

1. 父传子通过属性传值，子组件用properties接收。
2. 子传父通过父对子组件绑定一个事件，子组件用`this.triggerEvent("事件名",值)`以入参的方式传回父。
3. 父组件用this.selectComponent获取子组件实例，可以获取子组件的数据，使用子组件的方法。
4. 全局传值，相当于事件总线把，在app.js中定义globalData，然后在任意组件就可以读值和设置值。
5. url传值，只能传字符串，`wx.navigateTo()`带上query参数，页面在onLoad(options)中options可以获取参数。
6. 页面之间要传递复杂的数据的话，`wx.navigateTo()`中配置events事件以及成功的success回调，目标页面就能通过getOpenerEventChannel获取。
7. 本地存储数据，`wx.setStorageSync`和 `wx.getStorageSync`。



### 2.小程序setData

用来修改state中的数据，修改是同步的，但是页面渲染是异步的。



### 3.页面下拉刷新与上拉加载

可以在全局 config 中的 window 配置中设置 enablePullDownRefresh 属性，当然建议 enablePullDownRefresh 属性是在页面级配置中设置， 在 Page 中定义 onPullDownRefresh 事件函数
到达下拉刷新条件后，该事件函数执行，发起请求方法，下拉刷新请求返回后，调用 wx.stopPullDownRefresh 停止下拉刷新。
至于上拉加载则可以利用 onReachBottom 事件函数来确认后续的功能操作，一般它与 onReachBottomDistance 进行配合处理，确认距离底部的距离，而它的单位是px



### 4.bindtap和catchtap的区别是什么

- 相同点：首先他们都是作为点击事件函数，就是点击时触发。在这个作用上他们是一样的，可以不做区分。
- 不同点：他们的不同点主要是bindtap是不会阻止冒泡事件的，catchtap是阻值冒泡的。



### 5.小程序有哪些导航API，它们各自的应用场景与差异区别是什么

wx.navigateTo()：保留当前页面，跳转到应用内的某个页面，但是不能跳到 tabbar 页面
wx.redirectTo()：关闭当前页面，跳转到应用内的某个页面，但是不允许跳转到 tabbar 页面
wx.switchTab()：跳转到 tabBar 页面，并关闭其他所有非 tabBar 页面
wx.navigateBack()：关闭当前页面，返回上一页面或多级页面。可通过 getCurrentPages() 获取当前的页面栈，决定需要返回几层
wx.reLaunch()：关闭所有页面，打开到应用内的某个页面



### 6.小程序中如何使用第三方npm模块进行功能开发

- npm init项目的初始化操作
- npm install lodash --save等模块安装操作
- 微信开发者工具->详情->本地设置->使用npm模块
- 微信开发者工具->工具->构建npm

在设置里面使用npm模块，在工具里面构建npm



### 7.小程序的定位在开发环境的设置

- 使用定位操作需要授权处理，需在app.json中设置permission节点信息，将useLocation授权添加上。
- 开发环境使用定位需要在调试器中开启，在**Sensor(传感器)**中将Geolocation的enable设置为开启状态



### 8.小程序的地图应用可以使用什么方式处理

wx.getLocation获取位置的经纬度等信息，再使用wx.openLocation打开微信内置地图查看位置，但是能看到的东西很少，只有经纬度。

更详细的需要用第三方的API。



### 9.小程序如何实现分享功能

- 在页面中如果不设置 onShareAppMessage 分享的事件回调函数，那么小程序右上角三个点的操作中不包含分享功能

- 通过**button按钮的open-type属性设置为share**则将调用页面中的 onShareAppMessage 事件，可以通过事件的 res中的 from 内容来判断是按钮button的分享处理还是右上角三个点menu的页面分享操作

  



### 10.小程序是否支持双向数据绑定

- 但仅限于简易双向数据绑定，绑定的对象只能是一个单一字段的绑定，不支持对象等形式的数据路径设置操作

- 在自定义组件中也可以实现传递双向绑定操作

- 它的基本语法操作是

  ```html
  <input model:value="{{value}}" />
  ```



### 11.授权验证登录怎么做，用户退出后下次进入还需要再次授权吗

- wx.login获取到一个code，拿这code去请求后台得到openId, sessionKey, unionId。
- 调wx.getUserInfo获取用户信息内容
- 一次性授权：每次授权都需要与后台进行权限认证操作
- 永久授权：调取授权登录接口并把获取到的用户公开信息存入数据库



### 12.授权验证是怎么做的

- 按钮触发的，open-type指定为getUserInfo类型，可以从bindgetuserinfo回调中获取到用户信息
- 授权验证操作只执行一次，不会二次执行
- 授权以后可以通过wx.getUserInfo获取基础的用户信息



### 13.微信小程序之用户授权

用户授权包括很多内容：用户信息、地理位置、后台定位、录音功能、保存到相册、摄像头等

授权操作主要分两种不同的情况

- 弹出授权框用户点击允许，授权信息会直接记录，后续不再确认授权操作

- 弹出授权框用户点击拒绝，授权信息会直接记录，但用户还想再次操作对应功能，需要弹窗再次授权

  1. 查看所拥有权限
  2. wx.authorize 发起请求用户授权，利用 wx.showModal 弹窗授权确认
  3. wx.showModal 确认后利用 wx.openSetting 打开授权设置
  4. 确认授权设置打开授权信息

  



### 14.使用webview直接加载要注意哪些事项？

- 个人类型的小程序暂不支持使用
- H5地址需要在小程序后台添加H5域名白名单，如果webview里面还有跳转到其他的H5页面，也是需要添加域名白名单的
- 在网页内可通过window.__wxjs_environment变量判断是否在小程序环境
- webview内可以通过桥接方式进行监听，监听事件onPageStateChange可以确认小程序是否在前台
- 每个页面只能有一个 web-view，web-view 会自动铺满整个页面，并覆盖其他组件
- 避免在链接中带有中文字符，在 iOS 中会有打开白屏的问题，建议加一下 encodeURIComponent
- web-view 网页与小程序之间不支持除 JSSDK 提供的接口之外的通信



### 15.webview中的页面怎么跳转回小程序

`wx.miniProgram.navigateTo()`



### 16.怎么获取手机号

个人不行，要完成认证的小程序，先去微信平台认证。

1. 利用wx.login获取登录凭证code，通过code与开发者服务器交互获取加密后的openId，并将openId与session_key进行服务器数据库信息存储
2. 对openId进行加密传递回小程序端
3. 利用button进行open-type的类型设置，值为getPhoneNumber，并且需要进行bindgetphonenumber事件绑定
4. 绑定回调getPhoneNumber中可以找到手机加密数据
5. 将加密的openId、encryptedData、iv等数据发送至服务器端
6. 服务器端解密
7. 可以将解密信息等内容进行返回小程序端处理



### 17.生命周期

**应用级别的**

1. onLaunch 小程序初始化
2. onShow 小程序启动
3. onHide 小程序切后台

**页面级别的**

1. onLoad 页面加载
2. onShow 页面显示
3. onReady 页面渲染完成
4. onHide 页面隐藏
5. onUnload 页面卸载

**组件级别的**

1. created 组件实例创建
2. attached 组件被添加到页面节点树种
3. ready 组件初次渲染完成
4. moved 组件被移动到新的节点
5. detached 组件被页面节点树种移除





## React

### 1.React中的事件机制

JSX 上写的事件并**没有绑定在对应的真实 DOM 上**，而是通过事件代理的方式，将所有的事件都统一绑定在了组件树的根上。这样的方式不仅**减少了内存消耗，还能在组件挂载销毁时统一订阅和移除事件**。



### 2.React 高阶组件、Render props、hooks 有什么区别，为什么要不断迭代

- HOC

  简单来说就是一个函数接受一个组件，这个函数中又定义了一个组件，在这个新定义的组件中可以写一些属性方法等公共代码，然后把这些属性方法传给接受的组件，最后return新定义的组件。

  ```jsx
  // hoc的定义
  function withSubscription(WrappedComponent, selectData) {
    return class extends React.Component {
      constructor(props) {
        super(props);
        this.state = {
          data: selectData(DataSource, props)
        };
      }
      // 一些通用的逻辑处理
      render() {
        // ... 并使用新数据渲染被包装的组件!
        return <WrappedComponent data={this.state.data} {...this.props} />;
      }
    };
  
  // 使用
  const BlogPostWithSubscription = withSubscription(BlogPost,
    (DataSource, props) => DataSource.getBlogPost(props.id));
  ```

- Render props

  父组件向Render props组件传递了一个render函数，这个render函数定义了渲染内容；Render props组件通过this.props.render获取函数然后写入参数。

  ```jsx
  // DataProvider组件内部的渲染逻辑如下
  class DataProvider extends React.Components {
       state = {
      name: 'Tom'
    }
  
      render() {
      return (
          <div>
            <p>共享数据组件自己内部的渲染逻辑</p>
            { this.props.render(this.state) }
        </div>
      );
    }
  }
  
  // 调用方式
  <DataProvider render={data => (
    <h1>Hello {data.name}</h1>
  )}/>
  
  ```

- Hooks

  可以在里面用其他的hook，直接return出数据，使用的时候useXxxx就行了，非常方便。



### 3.对React-Fiber的理解，它解决了什么问题？

1. **可中断的渲染**

   以前react更新过程是同步的，一旦开始就会进行到底，这可能导致主线程被占据，页面卡顿做不了其他的事情。现在react把更新过程拆分成多个小任务，这样渲染的过程就能被其他优先级更高的任务插队，从而更好的响应用户交互。

2. **优先级管理**

   比如用户输入，图表更新，在浏览器原生的任务调度机制下，用户的输入可能会被图表更新所堵塞，但是在Fiber的操作下，用户的输入是优先于图表更新的。 React Fiber 如何在任务调度方面比浏览器提供更细粒度的控制。

3. **并发渲染**

   在传统架构中，React 是单线程的，无法充分利用多核 CPU 的优势。Fiber 使得 React 能够更好地利用现代多核处理器，提高渲染性能。



### 4.React.PureComponent

在函数组件里面就是`React.memo`，react会自动浅比较一下传入props，变化了就更新组件。



### 5.类组件中的生命周期

- **挂载阶段**

  1. **constructor**

     用于初始化 state 和绑定方法。

     ```jsx
     constructor(props) {
      super(props);
      this.state = { count: 0 };
     }
     ```

  2. **static getDerivedStateFromProps**

     根据 props 更新 state。是一个静态方法。返回值会合并到state中

     ```jsx
     static getDerivedStateFromProps(nextProps, prevState) {
      if (nextProps.someValue !== prevState.someValue) {
        return { someValue: nextProps.someValue };
      }
      return null;
     }
     ```

  3. **render**

     返回要渲染的元素。

     ```jsx
     render() {
      return <div>{this.state.count}</div>;
     }
     ```

  4. **componentDidMount**

     组件挂载后调用，可以进行 DOM 操作或数据请求。

     ```jsx
     componentDidMount() {
      // 进行数据请求或订阅操作
     }
     ```

- 更新阶段

  1. **getDerivedStateFromProps**

     在每次组件更新时调用（见上）。

  2. **shouldComponentUpdate**

     决定组件是否应该重新渲染。返回 `true` 或 `false`。

     ```jsx
     shouldComponentUpdate(nextProps, nextState) {
      return nextState.count !== this.state.count;
     }
     ```

  3. **render**

     重新渲染

  4. **getSnapshotBeforeUpdate**

     在更新前获取一些信息（例如，DOM 状态）。

     ```jsx
     getSnapshotBeforeUpdate(prevProps, prevState) {
      if (prevProps.someValue !== this.props.someValue) {
        return { scrollPosition: window.scrollY };
      }
      return null;
     }
     ```

  5. **componentDidUpdate**

     组件更新后调用，可以进行 DOM 操作或数据请求。

     ```jsx
     componentDidUpdate(prevProps, prevState, snapshot) {
      if (snapshot !== null) {
        window.scrollTo(0, snapshot.scrollPosition);
      }
     }
     ```

- **卸载阶段**

  **componentWillUnmount**

  ```jsx
  componentWillUnmount() {
   // 进行清理工作，如取消订阅
  }
  ```

  

### 6.哪些方法会触发 React 重新渲染？重新渲染会做些什么?

1. **State 变化**：
   - 当组件的 state 发生变化时，会触发重新渲染。
   - 使用 `this.setState` 方法更新 state 会导致重新渲染。
2. **Props 变化**：
   - 当父组件传递给子组件的 props 发生变化时，子组件会重新渲染。
   - 这也是为什么组件应该是纯函数的一个原因，即它们的输出应该完全由输入（props 和 state）决定。
3. **强制更新**：
   - 使用 `this.forceUpdate` 方法可以强制组件重新渲染。通常不推荐使用这个方法，因为它绕过了 React 的优化机制。
4. **Context 变化**：
   - 当使用 React Context 时，如果 Context 的值发生变化，所有使用该 Context 的组件都会重新渲染。
5. **父组件变化**：
   - 父组件的渲染会带着子组件一起重新渲染一遍。



重新渲染就会用diff算法来对新旧VNode进行比对。





### 7.React如何判断什么时候重新渲染组件？

写了componentShouldUpdate就根据返回值来判断，true就重新渲染，false就放弃这次渲染。



### 8.无状态组件

就是没有自己的状态，就负责展示，可以传递props给它展示。



### 9.如何获取DOM元素

1. 在类组件中使用 `ref`

   在类组件中，你可以通过创建一个 `ref` 并将其附加到一个 DOM 元素上来获取对该元素的引用。

   ```jsx
   import React, { Component } from 'react';
   
   class MyComponent extends Component {
     constructor(props) {
       super(props);
       // 创建一个 ref
       this.myRef = React.createRef();
     }
   
     componentDidMount() {
       // 访问 DOM 元素
       console.log(this.myRef.current);
     }
   
     render() {
       return <div ref={this.myRef}>Hello, World!</div>;
     }
   }
   
   export default MyComponent;
   ```

   

### 10.React中可以在render访问refs吗？为什么？

不能，要在render之后。



### 11.对React的插槽(Portals)的理解，如何使用，有哪些使用场景

Portal 提供了一种将子节点渲染到存在于父组件以外的 DOM 节点的优秀的方案。

React 提供了 `ReactDOM.createPortal` 方法来创建一个 Portal。这个方法接收两个参数：

1. 子组件（或元素）
2. DOM 节点

```jsx
import React from 'react';
import ReactDOM from 'react-dom';

class Modal extends React.Component {
  render() {
    return ReactDOM.createPortal(
      <div className="modal">
        {this.props.children}
      </div>,
      document.getElementById('modal-root')
    );
  }
}

// 在你的 HTML 文件中，需要有一个 id 为 'modal-root' 的元素，就是入口文件
// <div id="modal-root"></div>

class App extends React.Component {
  render() {
    return (
      <div className="app">
        <h1>My App</h1>
        <Modal>
          <p>This is a modal!</p>
        </Modal>
      </div>
    );
  }
}

export default App;
```

应用：弹窗类用的最多。





### 12.在React中如何避免不必要的render？

1. shouldComponentUpdate
2. PureComponent
3. React.memo



### 13.对 React context 的理解

用来组件通信的

```jsx
import React from 'react';

// 创建一个 Context 对象，并设置默认值
const ThemeContext = React.createContext('light');

export default ThemeContext;
```

```jsx
 //父组件
 <ThemeContext.Provider value={this.state.theme}>
        <div>
          <button onClick={this.toggleTheme}>Toggle Theme</button>
          <ThemedComponent />
        </div>
</ThemeContext.Provider>
```

```jsx
//子组件
  <ThemeContext.Consumer>
    {theme => (
      <div style={{ background: theme === 'light' ? '#fff' : '#333', color: theme === 'light' ? '#000' : '#fff' }}>
        <h2>Themed Component</h2>
        <p>The current theme is {theme}</p>
      </div>
    )}
  </ThemeContext.Consumer>
```



### 14.React中什么是受控组件和非控组件

指那些表单数据由React组件状态state控制的表单元素，表单元素的值和组件的状态同步。



### 15.React中refs的作用是什么？有哪些应用场景？

直接获取DOM元素或者React组件实例，但是**函数组件没有实例**，直接获取的话会报错，所以要用到forwardRef 

```jsx
const A = forwardRef((props,ref)=>{
    //接收两个参数
   	//	props表示传参
    //	转发ref给其他能获取到实例的元素
    return  <input ref={ref} type="text" />
})
```

```jsx
import React, { useRef, useEffect, forwardRef } from 'react';

// 定义一个函数组件并使用 React.forwardRef 转发 ref
const FunctionComponent = forwardRef((props, ref) => (
  <input ref={ref} type="text" />
));
//------------------------------------------------------------------
const ParentComponent = () => {
  const inputRef = useRef(null);

  useEffect(() => {
    // 组件挂载后，让输入框自动获得焦点
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  return <FunctionComponent ref={inputRef} />;
};

export default ParentComponent;
```



### 16.React中除了在构造函数中绑定this，还有别的方式吗？

一起列举出来

1. 在构造函数中绑定 `this`

   ```jsx
   class MyComponent extends React.Component {
     constructor(props) {
       super(props);
       this.state = { count: 0 };
       this.handleClick = this.handleClick.bind(this);
     }
   
     handleClick() {
       this.setState({ count: this.state.count + 1 });
     }
   
     render() {
       return <button onClick={this.handleClick}>Click me</button>;
     }
   }
   ```

2. 使用箭头函数定义类方法（类字段语法）

   ```jsx
   class MyComponent extends React.Component {
     state = { count: 0 };
   
     handleClick = () => {
       this.setState({ count: this.state.count + 1 });
     };
   
     render() {
       return <button onClick={this.handleClick}>Click me</button>;
     }
   }
   ```

3. 在jsx中使用箭头函数

   ```jsx
   class MyComponent extends React.Component {
     state = { count: 0 };
   
     handleClick() {
       this.setState({ count: this.state.count + 1 });
     }
   
     render() {
       return <button onClick={()=>this.handleClick()}>Click me</button>;
     }
   }
   ```

4. 在jsx中用bind，`this.handleClick.bind(this);`



### 17.React组件的构造函数有什么作用？它是必须的吗？

**构造函数的主要作用**：初始化状态和绑定事件处理器中的 `this`。

所以如果props不涉及初始化，又不需要处理this的问题的话，那就可以不用构造函数。

```js
class LikeButton extends React.Component {
  constructor() {
    super();
    this.state = {
      liked: false
    };
    this.handleClick = this.handleClick.bind(this);
  }
  handleClick() {
    this.setState({liked: !this.state.liked});
  }
  render() {
    const text = this.state.liked ? 'liked' : 'haven\'t liked';
    return (
      <div onClick={this.handleClick}>
        You {text} this. Click to toggle.
      </div>
    );
  }
}
ReactDOM.render(
  <LikeButton />,
  document.getElementById('example')
);
```



### 18.setState的用法和原理

推荐使用函数式的，可以获取到正确的状态。

```jsx
this.setState((prevState, props) => ({
 ...
}),callback);
              
//第二个参数是回调函数，state完成更新后执行
```

用`useState()`也是的，如果依赖旧状态，也建议写函数式的

```
import React, { useState } from 'react';

function Counter() {
  // 声明一个叫做 "count" 的状态变量，并赋初始值为 0
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount((prevCount )=>prevCount +1)}>
        Click me
      </button>
    </div>
  );
}
```



1. **状态更新请求**：
   当 `setState` 被调用时，React 接收到一个状态更新请求，这个请求可以是一个对象或者一个函数。
2. **合并状态**：
   React 将新的状态与当前状态合并（浅合并），但不会立即更新 `this.state`。相反，React 会将状态更新放入一个队列中，稍后处理。
3. **批量更新**：
   为了提高性能，React 会批量处理多个 `setState` 调用。在事件处理、生命周期方法或合成事件中，状态更新不会立即生效，而是会被暂存并在稍后的一个批处理中一起处理。但是如果在一些原生事件中，`setState`可能是同步的，因为合成事件不会处理。
4. **重新渲染**：
   批处理完成后，React 会重新计算组件的状态和属性，并触发组件的重新渲染。React 会调用 `render` 方法生成新的虚拟 DOM，然后通过与旧的虚拟 DOM 进行对比（diffing），找到需要更新的部分，并进行实际的 DOM 更新。



### 19.React中defaultProps

在 React 16.3 及更高版本中，推荐使用 `defaultProps` 静态属性来定义默认属性值：

- 类组件

  ```jsx
  class MyComponent extends React.Component {
    static defaultProps = {
      name: 'Default Name'
    };
  
    render() {
      return <div>{this.props.name}</div>;
    }
  }
  
  // 使用 defaultProps 的效果与 getDefaultProps 相同
  <MyComponent /> // 渲染结果：<div>Default Name</div>
  ```

- 函数组件

  直接使用默认入参就行了



### 20.React中的setState和replaceState的区别是什么？

replaceState已经被废弃了，不了解。



### 21.React性能优化在哪个生命周期？它优化的原理是什么？

shouldComponentUpdate(nextProps,nextState)，可以决定组件是否更新。



### 22.state和 props 触发更新的生命周期分别有什么区别？

`getDerivedStateFromProps`仅在 `props` 变化时调用。



### 23.React-Router的实现原理是什么？

客户端路由实现的思想：

- 基于 hash 的路由：通过监听`hashchange`事件，感知 hash 的变化

- - 改变 hash 可以直接通过 location.hash=xxx

- 基于 H5 history 路由：

- - 改变 url 可以通过 history.pushState 和 resplaceState 等，会将URL压入堆栈，同时能够应用 `history.go()` 等 API
  - 监听 url 的变化可以通过自定义事件触发实现



### 24.React-Router怎么设置重定向？

使用 `<Navigate>` 组件



### 25.React-Router如何获取URL的参数？

1. **路径参数**

   ```jsx
        // 定义路由
        <Route path="/user/:id" component={UserComponent} />
   
        // 获取参数
        const { id } = useParams();
   ```

2. **查询参数**

   ```jsx
        // 定义路由
        <Route path="/search" component={SearchComponent} />
   
        // 获取查询参数
        const [searchParams] = useSearchParams();
        const query = searchParams.get('query');
   ```

3. **state参数**

   ```jsx
   const navigate = useNavigate(); 
   navigate('/user', { state: { id: 123, name: 'John Doe' } }); // 导航并通过 state 传递参数
   
   ---------------------------
       
   const location = useLocation();
   const userState = location.state; // 获取通过 state 传递的参数
   ```

4. **其他的钩子**

   ```jsx
   import React from 'react';
   import { useMatch } from 'react-router-dom';
   
   const About = () => {
     const match = useMatch('/about');
   
     return (
       <div>
         <h1>About Page</h1>
         {match && <p>This is the About page</p>}
       </div>
     );
   };
   
   export default About;
   ```

   

### 26.useLayoutEffect

用法和useEffect一样，普通的useEffect会再浏览器完成**绘制**之后执行，但是useLayoutEffect会**在DOM变更后就执行（浏览器绘制之前）**，这有什么卵用呢？

比如说要写一个tooltip，当上方的空间不够了，那就应该尝试出现在下方，所以要在浏览器完成绘制之前也就是DOM一旦变更就可以去测量上方的空间够不够了，上方空间不够用立马就更改他的位置，让浏览器再次渲染一遍。



### 27.React 数据持久化有什么实践吗？

**redux-persist**



### 28.Redux原理

在React中，组件通过connect连接到 Redux ，如果要访问 Redux，需要dispatch一个包含 type和负载(payload) 的 Action。Action 中的 payload 是可选的，Action 将其转发给 Reducer。

当Reducer收到Action时，通过 switch…case 语法比较 Action 中type。 匹配时，更新对应的内容返回新的 state。

当Redux状态更改时，连接到Redux的组件将接收新的状态作为props。当组件接收到这些props时，它将进入更新阶段并重新渲染 UI。

```jsx
import React from 'react';
import { connect } from 'react-redux';
import { increment, decrement } from './actions';

function App({ count, increment, decrement }) {
  return (
    <div>
      <button onClick={increment}> + </button>
      <p>{count}</p>
      <button onClick={decrement}> - </button>
    </div>
  )
}

//把store中的数据映射到组件的props中
const mapStateToProps = state => {
  return {
    count: state.count,
  }
}

//把actions映射到组件的props中
const mapDispatchToProps = {
  increment,
  decrement,
}

// 使用 connect 函数连接组件和 Redux store
export default connect(mapStateToProps, mapDispatchToProps)(App)

```



### 29.reducer

`reducer` 函数接收当前状态 `state` 和一个动作 `action`，然后根据 `action.type` 返回新的状态。

函数组件中使用useReducer

```jsx
import React, { useReducer } from 'react';

const initialState = { count: 0 };

function reducer(state, action) {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + 1 };
    case 'DECREMENT':
      return { count: state.count - 1 };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'INCREMENT' })}>Increment</button>
      <button onClick={() => dispatch({ type: 'DECREMENT' })}>Decrement</button>
    </div>
  );
}

export default Counter;
```



### 30.useTransition

**延迟的更新**：使用 `useTransition` 标记的状态更新会被延迟，直到所有高优先级的更新完成。

**可中断的更新**：过渡更新可以被高优先级的更新中断，以保持应用的响应性。

**指示过渡状态**：可以获取过渡是否进行中的状态，以便在 UI 中展示加载指示器等。

```jsx
import React, { useState, useTransition } from 'react';

function App() {
  const [isPending, startTransition] = useTransition();
  const [count, setCount] = useState(0);

  const handleClick = () => {
    startTransition(() => {
      setCount(count + 1);
    });
  };

  return (
    <div>
      <button onClick={handleClick}>Increment</button>
      {isPending ? <p>Loading...</p> : <p>Count: {count}</p>}
    </div>
  );
}

export default App;
```



### 31.useDeferredValue

创造一个延迟更新的值，第一次返回旧值，当其他优先级高的任务执行完了再创造一个新值。



### 32.React.lazy()和Suspense

用于路由懒加载

```jsx
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { Suspense, lazy } from 'react';
const Home = lazy(() => import('./routes/Home'))
const count = lazy(() => import('./routes/count'))
 

export default class App extends Component {
  render() {
    return (
      <div>
          <Router>
            <Suspense fallback={<h1>Loading...</h1>}>
              <Switch>
                <Route exact path="/" component={Home}/>
                <Route path="/count" component={count}/>
                ...
              </Switch>
            </Suspense>
          </Router>
      </div>
    )
  }
}
```



### 33.JSX是怎么变成真实的DOM的

**JSX 解析和编译**：JSX 通过 Babel 编译成 `React.createElement` 调用。

**创建虚拟 DOM**：`React.createElement` 创建虚拟 DOM 对象。

**构建虚拟 DOM 树**：React 通过虚拟 DOM 对象构建虚拟 DOM 树。

**比较和更新虚拟 DOM 树**：React 比较新旧虚拟 DOM 树，找出差异。

**更新真实 DOM**：React 将差异转换为实际的 DOM 操作，更新真实 DOM。

**渲染真实 DOM**：React 将虚拟 DOM 树中的元素渲染成真实的 DOM 元素，并插入页面。



### 34.为什么 Hooks 不能在条件判断中使用？

React **依赖 Hook 调用顺序来正确关联状态和副作用**。



### 35.如何通过 DOM 元素找到对应的 Fiber 对象

具体来说，React 在内部创建 DOM 元素时，会在 DOM 元素上附加一个 `__reactFiber$` 前缀的属性，该属性的值是 `fiber` 对象。



### 36.React源码

#### 36-1.JSX转换成ReactElement的过程

调用了createElement方法

```js
/**
* 创建React Element
* type  元素类型
* config  配置属性
* children  子元素
* type  元素类型
*	1.分离props属性和特殊属性
*	2.将子元素挂在到props.children中
*	3.为props属性赋默认值
*	4.创建并返回ReactElement
*/
function createElement(type,config,children){
    ...
}
```

如何判断一个参数是ReactElement？

看对象的$$typeof属性

```
object.$$typeof === REACT_ELEMENT_TYPE
```



#### 36-2.React架构

- **Scheduler**(调度层)：调度任务的优先级，高优先级的先进入协调器。
- **Reconciler**(协调层)：构建Fiber数据结构，对比Fiber对象找出差异，记录Fiber对象要进行的DOM操作。
- **Renderer**(渲染层)：将变化的部分渲染到页面上。

调度层和协调层的工作是在内存当中进行的，渲染层设定的就是不可以打断的，所以不会出现DOM渲染不完整的问题。



#### 36-3. Fiber数据结构

```js
type Fiber= {
    /************DOM实例相关************/
    
    //表示Fiber节点的类型 用于协调和渲染的时候做判断的
	tag:WorkTag,
    
    //React元素的类型 DOM元素就是字符串("div","span") React元素就是组件的构造函数或者类
    type:any,
    
    //与Fiber节点关联的实例对象，对于DOM元素来说是实际的DOM节点，对于类组件来说是组件实例
    stateNode: any,
    
    /************构建Fiber树相关的************/
    
    //父Fiber节点，表示树结构中的父节点
  	return: Fiber | null,

  	//子Fiber节点，表示树结构中的第一个子节点。
  	child: Fiber | null,

  	//兄弟Fiber节点，表示树结构中当前节点的下一个兄弟节点。
  	sibling: Fiber | null,
    
    //有了这些数据，无论出于Fiber树种哪个位置，都能快速的找到父级 子级 兄弟级节点了
    
    //指的是 workInProgress Fiber节点
    alternate: Fiber | null,
    
    /************状态数据相关的************/
    
    //将用于渲染的新属性
    pendingProps: any,

  	//上一次渲染时使用的属性
  	memoizedProps: any,

  	//上一次渲染时使用的状态
 	 memoizedState: any,
    
     /************副作用相关************/
    
    //该Fiber对应的组件所产生的状态更新都会放在这个队列里
    updateQueue:updateQueue<any> | null,
    
    //用来记录当前Fiber要执行的DOM操作，比如说当前对应的DOM节点要做插入 删除等操作
    effectTag:sudeEffectTag,
    
    //指向当前Fiber节点的第一个副作用Fiber节点。
    firstEffect:Fiber | null,
    
    //指向当前Fiber节点的下一个副作用Fiber节点。
    nextEffect:Fiber | null,
    
    //指向当前Fiber节点的最后一个副作用Fiber节点。
    lastEffect:Fiber | null,
    
    //通过设置不同的expirationTime，React可以控制各个更新任务的执行顺序，确保用户交互等高优先级任务能及时响应。
    expirationTime:ExpirationTime,
    
    //表示当前Fiber节点的渲染模式  并发渲染，同步渲染，不使用特定的渲染模式等等
    mode:TypeOfMode,  
}
```



#### 36-4.双缓存技术

React最多同时存在两颗Fiber树，屏幕中看到的讲座current Fiber树，当发生更新的时候，React会在内存里面重新构建一颗workInProgress Fiber树。当workInProgress Fiber树构建好了直接替换current Fiber树，更新就更流畅了。



#### 36-5.FiberRoot和RootFiber

- FiberRoot

  是React应用的顶层结构，包含了整个应用的渲染状态和调度信息。它主要负责管理整个应用的渲染和更新过程。

- RootFiber

  是整个React应用的顶层Fiber节点，是`FiberRoot`的一个属性。`rootFiber`表示当前渲染的Fiber树的根节点，是从这个节点开始递归遍历整个Fiber树。



#### 36-6.整个过程

1. `render`方法的调用其实是return`legacyRenderSubtreeIntoContainer`的结果。
2. `legacyRenderSubtreeIntoContainer`是为`container`（`<div id = 'app'>`）创建或者获取`FiberRoot`，然后开始下一步调用`updateContainer`。
3. 更新过程就是调用了`updateContainer`，`updateContainer`会创建任务（初始化渲染或者更新渲染）放在任务队列里面，等待浏览器空闲执行。
4. 任务执行调用`scheduleUpdateOnFiber`，这会进入渲染阶段，渲染阶段包括了协调和提交两个子阶段。
5. 在协调阶段会对比新旧Fiber树的差异，React会建立一个Effect List，用于在提交阶段执行所有的副作用。每个Fiber节点都会有一个effectTag，用于标记要执行的操作，例如更新、插入、删除等等。
6. 提交阶段又分了三个小阶段，Before Mutation、Mutation和Layout。
7. Before Mutation会处理DOM更新前要处理的副作用，例如`getSnapshotBeforeUpdate`。
8. Mutation就处理DOM节点的添加更新等。
9. Layout会执行所有需要再DOM变更之后处理的副作用例如 `componentDidMount` 和 `componentDidUpdate`。
10. DOM的更新。
11. 在所有的更新完成之后，React会执行需要清理的任务，例如 `useEffect` 中的回调函数。





## 项目优化

**框架中的项目都差不多**

- 编码阶段

  1. 使用路由懒加载、异步组件
  2. 第三方模块按需导入
  3. 图片懒加载
  4. 防抖和节流
  5. 减少响应式数据
  6. 减少组件的嵌套
  7. 虚拟列表

- 打包阶段

  1. SplitChunksPlugin分包
  2. Tree Shaking树摇
  3. TerserPlugin用于压缩JS文件
  4. css-minimizer-webpack-plugin压缩CSS文件
  5. hash生成唯一的文件名
  6. thread-loader使用多线程加载，提升构建速度。
  7. cache-loader缓存编译的结果
  8. happyPack使用多线程加载，提升构建速度。
  9. webpack-bundle-analyzer分析打包的结果
  10. SpeedMeasurePlugin Webpack 构建过程中的各个步骤所花费的时间。

- 用户体验

  1. 使用cdn加载第三方模块

  2. 利用缓存

     

