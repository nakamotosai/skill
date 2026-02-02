---
name: OpenClaw聊天渠道配置
description: Discord、Telegram、WhatsApp等22个聊天渠道的配置和故障排查
---

# OpenClaw 聊天渠道配置

> 支持22个渠道：Discord、Telegram、WhatsApp、Slack、Signal等

---

## 📋 渠道概览

| 渠道 | 状态 | 配置方式 |
|:---|:---|:---|
| Discord | 生产就绪 | Bot Token |
| Telegram | 生产就绪 | Bot Token |
| WhatsApp | 生产就绪 | 扫码登录 |
| Slack | 生产就绪 | Bot Token |
| Signal | 可用 | signal-cli |
| iMessage | 可用(macOS) | imsg CLI |
| MS Teams | 可用 | Azure配置 |
| Matrix | 可用 | 账号密码 |
| Mattermost | 可用(插件) | Bot Token |
| Google Chat | 可用 | Service Account |

---

## 🎮 Discord 配置

### 快速设置

1. **创建Bot**：Discord Developer Portal → Applications → New Application → Bot
2. **启用Intent**：Bot → Privileged Gateway Intents → 启用 Message Content Intent
3. **生成邀请链接**：OAuth2 → URL Generator → 勾选 bot + applications.commands
4. **配置Token**：

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN"
    }
  }
}
```

或使用环境变量：`DISCORD_BOT_TOKEN=YOUR_TOKEN`

### 群组配置

```json
{
  "channels": {
    "discord": {
      "dm": { "enabled": true, "policy": "pairing" },
      "guilds": {
        "YOUR_GUILD_ID": {
          "requireMention": true,
          "channels": {
            "help": { "allow": true }
          }
        }
      }
    }
  }
}
```

### 常见问题

| 问题 | 解决方案 |
|:---|:---|
| Bot不回复 | 检查Message Content Intent是否启用 |
| `requireMention: false` 无效 | 设置 `groupPolicy: "open"` 或添加guild条目 |
| DM不工作 | 检查 `dm.policy` 设置，批准pairing |

---

## 📱 Telegram 配置

### 快速设置

1. **创建Bot**：@BotFather → `/newbot`
2. **配置Token**：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "123456:ABC...",
      "dmPolicy": "pairing"
    }
  }
}
```

或使用环境变量：`TELEGRAM_BOT_TOKEN=YOUR_TOKEN`

### 群组配置

```json
{
  "channels": {
    "telegram": {
      "groups": {
        "*": { "requireMention": true },
        "-1001234567890": { "requireMention": false }
      }
    }
  }
}
```

### Privacy Mode

> 默认情况下Bot只能看到@提及的消息

要接收所有消息：

1. @BotFather → `/setprivacy` → Disable
2. **或**将Bot设为群管理员

### 常见问题

| 问题 | 解决方案 |
|:---|:---|
| 群里不回复 | 检查Privacy Mode或设为管理员 |
| `/activation always` 无效 | 这只改session，需改config才持久 |
| IPv6问题 | 强制使用IPv4解析 `api.telegram.org` |

---

## 💬 WhatsApp 配置

### 快速设置

```bash
# 扫码登录
openclaw channels login
```

在WhatsApp → 设置 → 已连接设备 中扫描二维码

### 配置文件

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "dmPolicy": "pairing",
      "allowFrom": ["+15555550123"]
    }
  }
}
```

### Self-Chat 模式

```json
{
  "channels": {
    "whatsapp": {
      "selfChatMode": true,
      "dmPolicy": "allowlist",
      "allowFrom": ["+YOUR_NUMBER"]
    }
  }
}
```

### 常见问题

| 问题 | 解决方案 |
|:---|:---|
| 断开连接 | `openclaw channels login --verbose` 重新扫码 |
| 被登出 | 可能是另一设备使用了相同账号 |
| 媒体发送失败 | 检查文件大小限制（图片6MB，视频16MB） |

---

## 🔐 DM 安全策略 (Pairing)

所有渠道都支持 `dmPolicy` 设置：

| 策略 | 说明 |
|:---|:---|
| `pairing` | **默认**。陌生消息返回验证码，需批准 |
| `allowlist` | 只允许 `allowFrom` 中的用户 |
| `open` | 允许所有人（需设置 `allowFrom: ["*"]`） |
| `disabled` | 禁用DM |

### Pairing 操作

```bash
# 查看待批准列表
openclaw pairing list discord
openclaw pairing list telegram
openclaw pairing list whatsapp

# 批准
openclaw pairing approve discord <CODE>
openclaw pairing approve telegram <CODE>
openclaw pairing approve whatsapp <CODE>
```

---

## 🔗 渠道管理命令

```bash
# 列出渠道
openclaw channels list

# 状态检查
openclaw channels status
openclaw channels status --probe   # 深度检测

# 添加渠道
openclaw channels add --channel telegram --token $TOKEN
openclaw channels add --channel discord --token $TOKEN

# 登录/登出
openclaw channels login             # WhatsApp
openclaw channels logout

# 删除渠道
openclaw channels remove --channel discord --delete
```

---

## ⚙️ 通用配置选项

### 消息分块

```json
{
  "channels": {
    "discord": { "textChunkLimit": 2000 },
    "telegram": { "textChunkLimit": 4000 }
  }
}
```

### 媒体限制

```json
{
  "channels": {
    "discord": { "mediaMaxMb": 8 },
    "telegram": { "mediaMaxMb": 5 }
  }
}
```

### 重试策略

```json
{
  "channels": {
    "discord": {
      "retry": {
        "attempts": 3,
        "minDelayMs": 500,
        "maxDelayMs": 30000
      }
    }
  }
}
```

---

## 🔧 故障排查

### 通用诊断

```bash
openclaw doctor
openclaw channels status --probe
openclaw logs --follow | grep "channel\|discord\|telegram\|whatsapp"
```

### 获取ID

**Discord**：

1. 设置 → 高级 → 开发者模式
2. 右键 → 复制ID

**Telegram**：

1. 转发消息给 @userinfobot
2. 或查看 `openclaw logs --follow` 中的 `from.id`

**WhatsApp**：

- 电话号码格式：`+15555550123`

---

## 📚 详细文档

每个渠道的完整配置请查阅：

- `_raw/channels/discord.md`
- `_raw/channels/telegram.md`
- `_raw/channels/whatsapp.md`
- `_raw/channels/slack.md`
- `_raw/channels/signal.md`
- `_raw/channels/imessage.md`
- `_raw/channels/msteams.md`
