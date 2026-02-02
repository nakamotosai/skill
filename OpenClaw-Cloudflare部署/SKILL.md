---
description: 在 Cloudflare Workers 上部署 OpenClaw (MoltWorker) 的完整指南，包含环境配置、密钥设置、持久化存储、浏览器自动化集成及聊天平台接入。
---

# OpenClaw Cloudflare 部署指南

本 Skill 将指导你如何基于 [Cloudflare MoltWorker](https://github.com/cloudflare/moltworker) 项目，在 Cloudflare 平台上部署自托管的 OpenClaw (前身为 MoltBot) AI Agent。该项目利用 Cloudflare Sandboxes 在边缘运行安全的容器化环境。

> [!NOTE]
> 该部署需要 **Cloudflare Workers Paid Plan ($5/mo)** 以使用 Sandboxes 功能。

## 1. 准备工作

在开始之前，请确保你拥有：

- 一个 Cloudflare 账户并订阅了 Workers Paid Plan。
- 本地安装了 Node.js 和 npm。
- 一个 Anthropic API Key (或者使用 AI Gateway 支持的其他模型)。

## 2. 获取代码与安装依赖

首先克隆官方仓库并安装依赖：

```bash
git clone https://github.com/cloudflare/moltworker.git
cd moltworker
npm install
```

## 3. 基础配置与密钥设置

OpenClaw 需要通过 Cloudflare Secrets 存储敏感信息。

### 3.1 设置 AI 模型密钥

你可以直接设置 Anthropic Key，或者使用 Cloudflare AI Gateway (推荐)。

**方式 A: 直接使用 Anthropic Key**

```bash
npx wrangler secret put ANTHROPIC_API_KEY
# 提示时输入你的 sk-ant-... 密钥
```

**方式 B: 使用 Cloudflare AI Gateway (推荐)**

1. 在 Cloudflare Dashboard 创建 AI Gateway。
2. 添加 Provider (如 Anthropic)。
3. 获取 Gateway URL 和 API Key。

```bash
npx wrangler secret put AI_GATEWAY_API_KEY
npx wrangler secret put AI_GATEWAY_BASE_URL
# URL 格式: https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/anthropic
```

### 3.2 生成 Gateway Token

这是你为了连接和管理 Bot 所需的唯一凭证。

```bash
# 生成随机 Token
export MOLTBOT_GATEWAY_TOKEN=$(openssl rand -hex 32)
echo "Your Token: $MOLTBOT_GATEWAY_TOKEN"

# 写入 Secret
echo "$MOLTBOT_GATEWAY_TOKEN" | npx wrangler secret put MOLTBOT_GATEWAY_TOKEN
```

> [!IMPORTANT]
> 请务必保存好输出的 Token，后续访问管理后台 (`/_admin/`）和连接客户端时都会用到。

## 4. 配置安全访问 (Cloudflare Access)

为了安全地使用 Admin UI (`/_admin/`) 进行设备配对，必须配置 Cloudflare Access (Zero Trust)。

1. **部署一次以创建 Worker 实例**:

   ```bash
   npm run deploy
   ```

   *注意：此时访问 Admin UI 会失败，因为还未配置 Access。*

2. **开启 Access**:
   - 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/) -> Workers & Pages -> 选择 `moltbot-sandbox`。
   - Settings -> Domains & Routes -> 在 `workers.dev` 域名旁点击 `...` -> **Enable Cloudflare Access**。
   - 将你的邮箱添加到 Allow List。

3. **获取并在 Worker 中配置 Access 参数**:
   - 在 Access Application 设置中找到 **Application Audience (AUD) Tag**。
   - 在 Zero Trust Dashboard 设置中找到 **Team Domain** (例如 `myteam.cloudflareaccess.com`)。

   ```bash
   npx wrangler secret put CF_ACCESS_TEAM_DOMAIN
   # 输入: myteam.cloudflareaccess.com (不带 https)

   npx wrangler secret put CF_ACCESS_AUD
   # 输入: 你的 AUD Tag
   ```

## 5. 配置聊天平台集成 (可选)

OpenClaw 支持同时连接多个聊天平台。

### Telegram

获取 Bot Token (通过 @BotFather) 并设置：

```bash
npx wrangler secret put TELEGRAM_BOT_TOKEN
# 配合 TELEGRAM_DM_POLICY 使用 (默认: pairing)
```

### Discord

在 Discord Developer Portal 创建应用并获取 Bot Token：

```bash
npx wrangler secret put DISCORD_BOT_TOKEN
# 配合 DISCORD_DM_POLICY 使用 (默认: pairing)
```

### Slack

需要创建 Slack App 并获取 Bot Token (`xoxb-`) 和 App Token (`xapp-`)：

```bash
npx wrangler secret put SLACK_BOT_TOKEN
npx wrangler secret put SLACK_APP_TOKEN
```

配置完成后，记得运行 `npm run deploy` 重新部署。

## 6. 配置持久化存储 (R2) [推荐]

默认情况下 Sandboxes 容器重启后数据会丢失。配置 R2 可以保存对话历史、Session 和配对信息。

1. 在 Cloudflare Dashboard -> R2 中创建一个 Token，权限选择 **Object Read & Write**，作用域选择 `moltbot-data` bucket (部署时自动创建)。
2. 获取 Access Key ID 和 Secret Access Key。
3. 获取你的 Cloudflare Account ID。

```bash
npx wrangler secret put R2_ACCESS_KEY_ID
npx wrangler secret put R2_SECRET_ACCESS_KEY
npx wrangler secret put CF_ACCOUNT_ID
```

## 7. 配置浏览器自动化 (可选)

如果你希望 OpenClaw 具备联网浏览能力 (使用 Skill)，可启用 Browser Rendering。

1. **设置配置**:

    ```bash
    # 设置任意一个安全的共享密钥
    npx wrangler secret put CDP_SECRET

    # 设置 Worker 的 URL
    npx wrangler secret put WORKER_URL
    # 输入: https://moltbot-sandbox.<你的子域>.workers.dev
    ```

2. **内置 Browser Skill**:
   启用后，OpenClaw 会自动加载 `cloudflare-browser` skill。
   - 路径: `/root/clawd/skills/cloudflare-browser/`
   - 功能: 截图 (`screenshot.js`)、录制视频 (`video.js`) 等。

## 8. 部署与初始化

配置完成后，执行最终部署：

```bash
npm run deploy
```

### 初始化步骤

1. 打开浏览器访问 `https://<your-worker>.workers.dev/_admin/`。
   *Cloudflare Access 会要求你进行邮箱验证。*
2. 验证通过后，在 Admin UI 中使用之前生成的 `MOLTBOT_GATEWAY_TOKEN` 进行配对。
3. 你的设备（手机/电脑）现在已连接，可以开始使用 OpenClaw 了！

## 本地开发与调试

如果需要在本地开发，可以创建 `.dev.vars` 文件跳过 Access 验证：

```ini
DEV_MODE=true
DEBUG_ROUTES=true
# 添加其他必要的 Secret 变量
```

运行 `npm run start` 启动本地环境。

## 常用命令参考

| 变量名 | 说明 |
| :--- | :--- |
| `ANTHROPIC_API_KEY` | Claude API 密钥 |
| `MOLTBOT_GATEWAY_TOKEN` | 网关连接凭证 |
| `CF_ACCESS_TEAM_DOMAIN` | Zero Trust 团队域名 |
| `CF_ACCESS_AUD` | Access 应用受众 Tag |
| `R2_ACCESS_KEY_ID` | R2 存储 Key ID |
| `R2_SECRET_ACCESS_KEY` | R2 存储 Secret |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token |
| `DISCORD_BOT_TOKEN` | Discord Bot Token |
| `CDP_SECRET` | 浏览器自动化认证密钥 |
