---
name: OpenClaw快速开始
description: 从零开始安装配置OpenClaw，包括安装、onboard向导、pairing绑定等完整流程
---

# OpenClaw 快速开始

> 从零开始到第一条消息的完整指南

---

## 🚀 安装方式

### Linux / macOS

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Windows (PowerShell)

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

> ⚠️ **Windows强烈推荐使用WSL2**，原生Windows未经测试且兼容性较差

### 通过npm安装

```bash
npm install -g openclaw@latest
# 或
pnpm add -g openclaw@latest
```

---

## 📋 前置条件

| 依赖 | 要求 |
|:---|:---|
| Node.js | >= 22 |
| pnpm | 可选（从源码构建时推荐） |
| Brave Search API Key | 可选（用于web搜索） |

---

## 🧙 Onboard向导（推荐）

```bash
openclaw onboard --install-daemon
```

### 向导配置内容

1. **模式选择**：Local（本地） vs Remote（远程）
2. **认证方式**：
   - Anthropic API Key（推荐）
   - OpenAI Codex OAuth
   - Gemini API Key
   - 其他提供商
3. **工作区**：默认 `~/.openclaw/workspace`
4. **Gateway设置**：端口（默认18789）、绑定、认证
5. **渠道配置**：WhatsApp/Telegram/Discord等
6. **守护进程安装**：launchd(macOS) / systemd(Linux)
7. **Skills安装**：可选功能扩展

### 非交互式安装示例

```bash
# Anthropic
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --gateway-port 18789 \
  --install-daemon \
  --daemon-runtime node

# Gemini
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice gemini-api-key \
  --gemini-api-key "$GEMINI_API_KEY" \
  --gateway-port 18789
```

---

## 🔌 启动Gateway

### 检查服务状态

```bash
openclaw gateway status
```

### 手动启动（前台）

```bash
openclaw gateway --port 18789 --verbose
```

### Dashboard访问

- 本地：`http://127.0.0.1:18789/`
- 快捷命令：`openclaw dashboard`

---

## ✅ 快速验证

```bash
openclaw status           # 查看状态
openclaw health           # 健康检查
openclaw security audit --deep   # 安全审计
```

---

## 📱 连接聊天渠道

### WhatsApp（扫码登录）

```bash
openclaw channels login
```

在WhatsApp → 设置 → 已连接设备 中扫码

### Telegram / Discord

向导会提示输入Bot Token，或手动编辑配置文件

---

## 🔐 DM安全（Pairing）

默认情况下，陌生DM会收到一个验证码，需要批准后才会处理消息：

```bash
# 查看待批准列表
openclaw pairing list whatsapp
openclaw pairing list telegram
openclaw pairing list discord

# 批准某个验证码
openclaw pairing approve whatsapp XXXXXXXX
openclaw pairing approve telegram XXXXXXXX
openclaw pairing approve discord XXXXXXXX
```

---

## 🛠️ 从源码安装（开发者）

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build
pnpm build
openclaw onboard --install-daemon
```

---

## 📍 重要目录结构

| 路径 | 用途 |
|:---|:---|
| `~/.openclaw/openclaw.json` | 主配置文件 |
| `~/.openclaw/credentials/` | OAuth凭据 |
| `~/.openclaw/workspace/` | Agent工作区 |
| `~/.openclaw/agents/<id>/sessions/` | 会话数据 |
| `~/.openclaw/credentials/whatsapp/` | WhatsApp凭据 |

---

## ⚠️ 常见问题

| 问题 | 解决方案 |
|:---|:---|
| `no auth configured` | 运行 `openclaw onboard` 配置认证 |
| Bot不回复DM | 检查pairing状态，执行 `openclaw pairing approve` |
| WhatsApp/Telegram不工作 | 确保使用Node运行时（非Bun） |
| Gateway无法访问 | 检查端口18789是否开放 |

---

## 📚 相关文档

- 详细向导说明：`_raw/start/wizard.md`
- Pairing机制：`_raw/start/pairing.md`
- 完整安装选项：`_raw/install/`
