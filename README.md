# 🤖 NeonBotChat

基于 QQ 官方 Bot API 的 WebUI 机器人接管面板，支持真人接管 Bot 进行群消息收发。

## ✨ 功能

### 消息收发
- **实时消息**：WebSocket 推送，秒级同步群消息
- **手动接管**：通过 WebUI 直接以 Bot 身份发送消息
- **乐观更新**：发送消息即时显示气泡，失败可点击重发
- **富媒体支持**：图片消息自动显示，点击查看大图
- **右键菜单**：复制（文字 / 图片）、转发、收藏、撤回、删除、多选

### 消息管理
- **消息历史**：本地 SQLite 持久化，自动刷新
- **撤回消息**：调用 QQ API 撤回已发送消息
- **删除消息**：本地删除单条或批量，不影响 QQ 端
- **多选模式**：右键进入多选，批量删除消息
- **清空记录**：支持清空单个群聊或全部聊天记录

### 会话管理
- **聊天列表**：自动识别群聊，支持搜索
- **备注名**：给群聊设置自定义备注名
- **添加群聊**：手动输入 group_openid 添加会话

### 用户识别
- **Bot 标识**：Bot 用户自动标注 🤖
- **@提及转昵称**：`<@OpenID>` 自动替换为 @昵称
- **用户头像**：消息旁显示发送者头像

### 收藏系统
- 右键收藏任意消息（文字 / 图片）
- 收藏列表侧边栏一键查看

### 个性化
- **自定义背景**：上传图片作为聊天背景
- **透明度调节**：背景透明度 5%~100% 可调
- **毛玻璃效果**：侧边栏、顶栏、输入栏、气泡均支持毛玻璃

### 系统状态
- 设置 → 状态：实时显示系统信息、CPU、内存、运行时长
- 每秒自动刷新，进度条平滑过渡动画

### 配置
- 端口可配置（`webui-port`）
- 外网访问开关（`enable-public`）

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Windows / Linux / macOS

### 安装

```bash
pip install qq-botpy aiohttp fastapi uvicorn psutil
```

### 配置

编辑 `config.yaml`：

```yaml
appid: "你的AppID"
secret: "你的AppSecret"
webui-port: 36336       # WebUI 端口，默认 8080
enable-public: false    # true 绑定 0.0.0.0 允许外网访问
```

### 启动

```bash
python init.py
```

浏览器打开 `http://127.0.0.1:36336`。

## 📁 项目结构

```
NeonBotChat/
├── init.py              # 主入口，启动 Bot + Web 服务
├── web_server.py        # FastAPI + WebSocket 后端
├── database.py          # SQLite 存储 + 消息去重
├── PatchMsg.py          # 补丁：群消息解析 + 附件提取
├── PatchActiveMsg.py    # 补丁：主动发送 / 撤回消息
├── PatchUserInfo.py     # 补丁：获取用户昵称 / 头像
├── config.yaml          # Bot 配置文件
└── templates/
    └── index.html       # WebUI 前端（零框架依赖）
```

## 🛠 技术栈

- **后端**：Python FastAPI + WebSocket
- **前端**：原生 HTML/CSS/JS（零框架依赖）
- **存储**：SQLite
- **Bot SDK**：qq-botpy 1.2.1

## ⌨ 快捷键

| 操作 | 快捷键 |
|------|--------|
| 发送消息 | Enter |
| 换行 | Shift + Enter |
| 右键菜单 | 右键消息气泡 |
| 关闭弹窗 | 点击遮罩层 / Esc |

## ⚠️ 注意事项

- `config.yaml` 中的 AppSecret 是敏感信息，请勿泄露或提交到公开仓库
- qq-botpy 官方 SDK 已长期未更新，本项目通过 Patch 模块补齐缺失功能
- 图片消息依赖 QQ 多媒体 CDN，链接可能有时效性
- 撤回消息需要消息 ID，仅支持通过 WebUI 发出的消息

## 📄 License

Copyright © 2026 Neon. All Rights Reserved.
