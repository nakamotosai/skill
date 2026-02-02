---
name: OpenClaw故障排查决策树
description: 常见问题的快速诊断流程和解决方案
---

# OpenClaw 故障排查决策树

> 遇到问题？按照这个流程快速定位

---

## 🚨 快速诊断（60秒）

```bash
openclaw status         # 1. 基本状态
openclaw health         # 2. Gateway健康
openclaw doctor         # 3. 自动诊断
openclaw logs --follow  # 4. 实时日志
```

---

## 🌳 问题决策树

### Bot不回复消息

```
Bot不回复？
├── Gateway运行吗？
│   └── `openclaw gateway status`
│       ├── 没运行 → `openclaw gateway start`
│       └── 运行但端口不监听 → 检查 gateway.mode=local
│
├── 认证配置了吗？
│   └── `openclaw models status`
│       └── 没配置 → `openclaw onboard` 或 `openclaw models auth setup-token`
│
├── 是DM还是群？
│   ├── DM → 检查pairing
│   │   └── `openclaw pairing list <channel>` → 批准 → `openclaw pairing approve`
│   │
│   └── 群 → 检查mention要求
│       └── 是否需要@bot? → 设置 requireMention: false
│
└── 查看日志
    └── `openclaw logs --follow | grep "blocked\|skip\|unauthorized"`
```

### Gateway启动失败

```
Gateway启动失败？
├── "configuration invalid"
│   └── `openclaw doctor --fix`
│
├── "set gateway.mode=local"
│   └── `openclaw config set gateway.mode local`
│
├── "Address Already in Use"
│   └── 端口被占用
│       ├── Windows: `netstat -ano | findstr :18789`
│       └── 解决: 停止占用进程 或 改端口
│
└── "refusing to bind without auth"
    └── 非loopback需要认证
        └── `openclaw config set gateway.auth.token "your-token"`
```

### 认证/API错误

```
API错误？
├── "No API key found"
│   └── `openclaw models auth setup-token --provider anthropic`
│
├── "OAuth token refresh failed"
│   └── 推荐改用setup-token
│       └── `openclaw models auth setup-token --provider anthropic`
│
├── "All models failed"
│   ├── 检查凭据: `openclaw models status`
│   ├── 检查模型配置: agents.defaults.model.primary
│   └── 查看日志获取具体错误
│
└── "Antigravity version not supported"
    └── 更新版本字符串或重新认证
```

### 渠道问题

```
渠道问题？
├── WhatsApp断开
│   └── `openclaw channels login --verbose` 重新扫码
│
├── Discord Bot不响应
│   ├── 检查Message Content Intent
│   ├── 检查groupPolicy设置
│   └── `openclaw channels status --probe`
│
├── Telegram群里不回复
│   ├── 检查Privacy Mode (BotFather)
│   └── 或设Bot为管理员
│
└── Pairing码不到达
    └── 待批准列表已满(默认3个)
        └── 批准现有请求腾出空间
```

---

## 🔧 常用修复命令

### 重启服务

```bash
# Linux (systemd)
systemctl --user restart openclaw-gateway

# macOS (launchd)
launchctl kickstart -k gui/$UID/bot.molt.gateway

# 通用
openclaw gateway restart
```

### 重置配置

```bash
# 只重置配置
openclaw reset --scope config

# 完全重置（需重新登录）
openclaw reset --scope full --yes
```

### 清理状态

```bash
# 停止服务
openclaw gateway stop

# 删除状态（谨慎！）
rm -rf ~/.openclaw

# 重新配置
openclaw onboard
```

---

## 📍 日志位置

| 平台 | 日志位置 |
|:---|:---|
| 通用 | `/tmp/openclaw/openclaw-YYYY-MM-DD.log` |
| macOS服务 | `~/.openclaw/logs/gateway.log` |
| Linux systemd | `journalctl --user -u openclaw-gateway -n 200` |
| Windows | `schtasks /Query /TN "OpenClaw Gateway"` |

### 日志过滤

```bash
# 查找错误
openclaw logs --follow | grep "error\|failed\|blocked"

# 看渠道活动
openclaw logs --follow | grep "discord\|telegram\|whatsapp"

# 看认证问题
openclaw logs --follow | grep "auth\|token\|oauth"
```

---

## 🔍 深度诊断

```bash
# 完整状态报告（可分享）
openclaw status --all

# 深度健康检查
openclaw status --deep

# 安全审计
openclaw security audit --deep

# 渠道探测
openclaw channels status --probe
```

---

## ⚠️ 已知问题

| 问题 | 解决方案 |
|:---|:---|
| Bun运行时+WhatsApp/Telegram | 使用Node运行时 |
| Node 22+ 长轮询中断 | 升级OpenClaw或用Node 20 |
| Snap版Chromium浏览器问题 | 安装Google Chrome |

---

## 📞 获取帮助

1. 先检查日志：`/tmp/openclaw/`
2. 搜索GitHub Issues
3. 提交Issue时附上：
   - OpenClaw版本
   - 相关日志片段
   - 复现步骤
   - 配置（隐藏敏感信息！）
