# 前端应用

基于 Next.js 14 的法学AI-Agent前端界面。

## 技术栈

- **Next.js 14** - React 框架
- **TypeScript** - 类型安全
- **TailwindCSS** - 样式框架
- **ShadcnUI** - UI 组件库
- **Lucide React** - 图标库

## 项目结构

```
frontend/
├── app/
│   ├── layout.tsx        # 根布局
│   ├── page.tsx          # 首页
│   └── globals.css       # 全局样式
├── components/
│   ├── ChatInterface.tsx # 聊天界面主组件
│   ├── MessageBubble.tsx # 消息气泡组件
│   ├── CitationPanel.tsx # 引用面板组件
│   └── ui/               # UI 组件
│       ├── button.tsx
│       ├── input.tsx
│       ├── card.tsx
│       └── badge.tsx
├── lib/
│   └── utils.ts          # 工具函数
└── package.json
```

## 核心功能

### 1. 聊天界面 (ChatInterface)
- 实时对话交互
- 消息历史管理
- 加载状态显示
- 引用点击交互

### 2. 消息气泡 (MessageBubble)
- 用户/助手消息区分
- 引用标记高亮
- 引用标签展示
- 点击查看详情

### 3. 引用面板 (CitationPanel)
- 显示法律条文详情
- 来源信息展示
- 原文内容查看
- 链接跳转

## 开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 启动生产服务器
npm start
```

## 配置

确保后端服务运行在 `http://localhost:8000`，或修改 `ChatInterface.tsx` 中的 API 地址。

## 特性

- ✅ 响应式设计
- ✅ 引用追踪和展示
- ✅ 流畅的用户体验
- ✅ TypeScript 类型安全

