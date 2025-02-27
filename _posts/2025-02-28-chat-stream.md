---
title: 前端如何实现GPT的打字（streaming）效果
categories: [日常开发]
tags: [流式响应,ChatGPT效果,打字机效果]
---



## 1.获取Api Key

1. Api Key

   可以通过https://openrouter.ai获取，自行注册一个就可以免费试用了。这里我选的是**[Mistral 7B Instruct(free)](https://openrouter.ai/mistralai/mistral-7b-instruct:free)**，为了下面的步骤顺利进行，推荐和我使用一样的。

   ![](https://image.xukucha.cn/blog/20250225140838.png)

   然后就跳转到这个页面，再次点击创建按钮

![](https://image.xukucha.cn/blog/20250225140913.png)

如图输入就行

![](https://image.xukucha.cn/blog/20250225141027.png)

然后就获取到了key，注意自己保存下来

![](https://image.xukucha.cn/blog/20250225141135.png)

## 2.项目代码

搭建项目，我使用的是Next.js，根据个人习惯喜欢用什么框架就用什么框架。

传送门：[Nextjs](https://nextjs.org/docs/app/getting-started/installation)

```bash
# 执行创建Nextjs项目
npx create-next-app@latest
```

我选择了这些配置

![](https://image.xukucha.cn/blog/20250228002516.png)

**给出项目代码可以直接食用：**

```bash
app/
├── components/
│   ├── ApiKeyForm.tsx
│   ├── ChatInput.tsx
│   └── MessageList.tsx
├── types/
│   └── chat.ts
├── layout.tsx
└── page.tsx
```

```tsx
// app/components/ApiKeyForm.tsx

'use client';

import React, { useState } from 'react';
import { Key } from 'lucide-react';
import type { ApiKeyFormProps } from '../types/chat';

export default function ApiKeyForm({ onSubmit }: ApiKeyFormProps) {
    const [apiKey, setApiKey] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (apiKey.trim()) {
            onSubmit(apiKey.trim());
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
            <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-sm">
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="flex items-center justify-center mb-6">
                        <Key className="w-12 h-12 text-blue-500" />
                    </div>
                    <h2 className="text-2xl font-bold text-center text-gray-800">
                        输入 OpenRouter API Key
                    </h2>
                    <p className="text-center text-gray-600 mb-4">
                        请输入您的API Key以开始对话
                    </p>
                    <input
                        type="password"
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                        className="w-full p-3 border border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
                        placeholder="sk-or-v1-..."
                    />
                    <button
                        type="submit"
                        disabled={!apiKey.trim()}
                        className="w-full bg-blue-500 text-white p-3 rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                    >
                        确认
                    </button>
                </form>
            </div>
        </div>
    );
}
```

```tsx
// app/components/ChatInput.tsx

'use client';

import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';
import type { ChatInputProps } from '../types/chat';

export default function ChatInput({ onSend, isLoading }: ChatInputProps) {
    const [input, setInput] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        await onSend(input.trim());
        setInput('');
    };

    return (
        <div className="border-t bg-white p-4">
            <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="发送消息..."
                    className="w-full p-4 pr-12 rounded-lg border border-gray-200 focus:outline-none focus:border-blue-500"
                    disabled={isLoading}
                />
                <button
                    type="submit"
                    disabled={isLoading || !input.trim()}
                    className="absolute right-3 top-1/2 -translate-y-1/2 p-2 text-blue-500 hover:text-blue-600 disabled:text-gray-400 transition-colors"
                >
                    {isLoading ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                        <Send className="w-5 h-5" />
                    )}
                </button>
            </form>
        </div>
    );
}
```

```tsx

// app/components/MessageList.tsx

'use client';

import React, { useEffect, useRef } from 'react';
import { User, Bot } from 'lucide-react';
import type { MessageListProps } from '../types/chat';

export default function MessageList({ messages }: MessageListProps) {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    if (messages.length === 0) {
        return (
            <div className="flex-1 flex flex-col items-center justify-center text-gray-500">
                <Bot className="w-12 h-12 mb-4" />
                <p>开始一个新的对话</p>
            </div>
        );
    }

    return (
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map(message => (
                <div
                    key={message.id}
                    className={`flex items-start gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'
                        }`}
                >
                    {message.role === 'assistant' && (
                        <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center">
                            <Bot className="text-white w-5 h-5" />
                        </div>
                    )}
                    <div
                        className={`max-w-2xl rounded-lg p-4 ${message.role === 'user'
                            ? 'bg-blue-500 text-white'
                            : 'bg-white shadow-sm'
                            }`}
                    >
                        <div className="whitespace-pre-wrap">{message.content}</div>
                        {message.isStreaming && (
                            <span className="inline-block animate-pulse">▋</span>
                        )}
                    </div>
                    {message.role === 'user' && (
                        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                            <User className="text-gray-600 w-5 h-5" />
                        </div>
                    )}
                </div>
            ))}
            <div ref={messagesEndRef} />
        </div>
    );
}
```

```ts
// app/types/chat.ts

export type Message = {
    id: string;
    content: string;
    role: 'user' | 'assistant';
    isStreaming?: boolean;
};

export type ApiKeyFormProps = {
    onSubmit: (apiKey: string) => void;
};

export type ChatInputProps = {
    onSend: (message: string) => Promise<void>;
    isLoading: boolean;
};

export type MessageListProps = {
    messages: Message[];
};
```

```tsx
// app/layout.tsx

import { Inter } from 'next/font/google'
import './globals.css'

// 使用 Inter 字体
const inter = Inter({ subsets: ['latin'] })

// Root Layout
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

```tsx
// app/page.tsx

'use client';

import { useState } from 'react';
import ApiKeyForm from './components/ApiKeyForm';
import ChatInput from './components/ChatInput';
import MessageList from './components/MessageList';
import type { Message } from './types/chat';

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isKeySet, setIsKeySet] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleKeySubmit = (key: string) => {
    setApiKey(key);
    setIsKeySet(true);
  };

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model: 'mistralai/mistral-7b-instruct',
          messages: [...messages, userMessage].map(msg => ({
            role: msg.role,
            content: msg.content
          })),
          stream: true,
        }),
      });

      if (!response.ok) throw new Error('API request failed');

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      const messageId = Date.now().toString();

      // 初始化助手消息
      setMessages(prev => [...prev, {
        id: messageId,
        content: '',
        role: 'assistant',
        isStreaming: true
      }]);

      // 处理流式响应
      while (reader) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter(line => line.trim() !== '');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;

            try {
              const parsed = JSON.parse(data);
              const content = parsed.choices[0]?.delta?.content || '';

              setMessages(prev => prev.map(msg =>
                msg.id === messageId
                  ? { ...msg, content: msg.content + content }
                  : msg
              ));
            } catch (e) {
              console.error('Error parsing stream:', e);
            }
          }
        }
      }

      // 完成流式输出
      setMessages(prev => prev.map(msg =>
        msg.id === messageId
          ? { ...msg, isStreaming: false }
          : msg
      ));
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        content: '抱歉，发生了错误。请稍后重试。',
        role: 'assistant'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isKeySet) {
    return <ApiKeyForm onSubmit={handleKeySubmit} />;
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <MessageList messages={messages} />
      <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}
```

前端页面展示

![](https://image.xukucha.cn/blog/20250228003129.png)

![](https://image.xukucha.cn/blog/20250228003627.png)



## 3.流式传输

流式响应允许服务器以小块（chunks）的形式逐步发送数据，而不必等待整个响应准备完毕。

**工作流程**：

1. 客户端发送请求
2. 服务器接收请求并开始处理
3. 服务器处理出一部分数据后立即发送这部分数据
4. 客户端立即开始处理这部分数据
5. 服务器继续处理并发送更多数据块
6. 这个过程持续到全部数据传输完毕

在这个项目中，流式响应特别适合模拟打字的效果，具体细节在于：

1. **建立流式请求**：

   ```ts
   const response = await fetch(url, {
     // ...其他配置
     body: JSON.stringify({
       // ...其他参数
       stream: true,  // 启用流式响应
     }),
   });
   ```

2. **使用 Reader 接口处理流**：

   ```ts
   const reader = response.body?.getReader();
   const decoder = new TextDecoder();
   
   while (reader) {
     const { done, value } = await reader.read();
     if (done) break;
     
     const chunk = decoder.decode(value);
     // 处理收到的数据块
   }
   ```

3. **增量更新 UI**：

   ```ts
   setMessages(prev => prev.map(msg =>
     msg.id === messageId
       ? { ...msg, content: msg.content + newContent }
       : msg
   ));
   ```



## 4.分析处理流式响应代码

1. 发送用户消息

   ```ts
   // 这部分创建用户消息对象，添加到消息列表，并设置加载状态。
   
   const userMessage: Message = {
     id: Date.now().toString(),
     content,
     role: 'user'
   };
   
   setMessages(prev => [...prev, userMessage]);
   setIsLoading(true);
   ```

2. 发送API请求

   ```ts
   const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
     method: 'POST',
     headers: { ... },
     body: JSON.stringify({
       model: 'mistralai/mistral-7b-instruct',
       messages: [...messages, userMessage].map(msg => ({
         role: msg.role,
         content: msg.content
       })),
       stream: true, // 启用流式响应
     }),
   });
   ```

3. 准备读取流数据

   ```ts
   // getReader()：获取一个可以读取流的阅读器
   const reader = response.body?.getReader();
   // TextDecoder：用于将二进制数据转换为文本
   const decoder = new TextDecoder();
   // messageId：为AI回复创建一个唯一ID
   const messageId = Date.now().toString();
   ```

4. 创建空的AI回复消息

   ```ts
   // 这里创建一个空消息，稍后会逐步填充内容。
   
   setMessages(prev => [...prev, {
     id: messageId,
     content: '',  // 初始内容为空
     role: 'assistant',
     isStreaming: true  // 标记为正在流式接收
   }]);
   ```

5. 流式读取数据的核心循环

   ```ts
   while (reader) {
     const { done, value } = await reader.read();
     if (done) break;  // 如果读取完毕就退出循环
   
     const chunk = decoder.decode(value);  // 将二进制数据解码为文本
     const lines = chunk.split('\n').filter(line => line.trim() !== '');  // 按行分割
   ```

6. 解析每个数据块

   ```ts
   for (const line of lines) {
     if (line.startsWith('data: ')) {
       const data = line.slice(6);  // 移除"data: "前缀
       if (data === '[DONE]') continue;  // 特殊标记，表示流结束
   
       try {
         const parsed = JSON.parse(data);  // 解析JSON数据
         const content = parsed.choices[0]?.delta?.content || '';  // 提取新内容片段
   ```

   流式响应会发送多个"data:"开头的行，每行包含一个JSON。格式类似：

   ```json
   data: {"choices":[{"delta":{"content":"你"}}]}
   data: {"choices":[{"delta":{"content":"好"}}]}
   ```

   ![](https://image.xukucha.cn/blog/20250228012349.png)

7. 更新消息内容

   ```ts
   // 这里不是替换整个消息，而是逐步追加新内容，实现了内容"流入"的效果。
   
   setMessages(prev => prev.map(msg =>
     msg.id === messageId
       ? { ...msg, content: msg.content + content }  // 追加新内容到现有内容
       : msg
   ));
   ```

8. 完成流处理

   ```ts
   // 当全部内容接收完成后，移除流式状态标记（停止显示闪烁的光标）。
   
   setMessages(prev => prev.map(msg =>
     msg.id === messageId
       ? { ...msg, isStreaming: false }  // 标记流结束
       : msg
   ));
   ```

9. 错误处理

   ```ts
   catch (error) {
     console.error('Error:', error);
     setMessages(prev => [...prev, {
       id: Date.now().toString(),
       content: '抱歉，发生了错误。请稍后重试。',
       role: 'assistant'
     }]);
   }
   ```

   