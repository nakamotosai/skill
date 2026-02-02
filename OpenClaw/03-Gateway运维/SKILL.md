---
name: OpenClaw Gateway运维
description: Gateway配置、日志分析、健康检查和常见问题排查
---

# OpenClaw Gateway 运维指南

> Gateway是OpenClaw的核心服务，负责消息路由和Agent调用

---

## 🔧 Gateway 基础命令

### 服务管理

```bash
# 状态检查（含RPC探测）
openclaw gateway status

# 服务生命周期
openclaw gateway install   # 安装服务
openclaw gateway start     # 启动
openclaw gateway stop      # 停止  
openclaw gateway restart   # 重启
openclaw gateway uninstall # 卸载

# 前台运行（调试用）
openclaw gateway --port 18789 --verbose
```

### 日志查看

```bash
# 实时日志（推荐）
openclaw logs --follow

# 最近N条
openclaw logs --limit 200

# JSON格式
openclaw logs --json

# 日志文件位置
# - 主日志: /tmp/openclaw/openclaw-YYYY-MM-DD.log
# - macOS服务日志: ~/.openclaw/logs/gateway.log
# - Linux systemd: journalctl --user -u openclaw-gateway -n 200
```

---

## 📊 快速诊断流程

| 步骤 | 命令 | 用途 |
|:---|:---|:---|
| 1 | `openclaw status` | 快速概览 |
| 2 | `openclaw status --all` | 完整诊断（可分享） |
| 3 | `openclaw gateway status` | 服务状态+配置 |
| 4 | `openclaw health` | Gateway健康检查 |
| 5 | `openclaw logs --follow` | 实时日志（最有用） |
| 6 | `openclaw doctor` | 自动诊断修复 |

---

## ⚙️ 配置文件

### 主配置文件位置

```
~/.openclaw/openclaw.json
```

### 关键配置项

```json
{
  "gateway": {
    "mode": "local",      // local 或 remote
    "port": 18789,
    "bind": "loopback",   // loopback|lan|tailnet|auto
    "auth": {
      "mode": "token",
      "token": "your-token"  // 非loopback必须配置
    }
  },
  "logging": {
    "level": "info",      // trace|debug|info|warn|error
    "consoleLevel": "info",
    "file": "/tmp/openclaw/openclaw.log"
  }
}
```

---

## 🔥 常见问题解决

### 1. Gateway启动失败

**症状**: `Gateway won't start — configuration invalid`

```bash
# 诊断
openclaw doctor

# 自动修复
openclaw doctor --fix
```

### 2. 模式未配置

**症状**: `Gateway start blocked: set gateway.mode=local`

```bash
# 修复
openclaw config set gateway.mode local
# 或运行向导
openclaw configure
```

### 3. 端口被占用

**症状**: `Address Already in Use (Port 18789)`

```bash
# 检查谁在用
lsof -nP -iTCP:18789 -sTCP:LISTEN    # macOS/Linux
netstat -ano | findstr :18789         # Windows

# 强制占用
openclaw gateway --force
```

### 4. 无API Key

**症状**: `No API key found for provider "anthropic"`

```bash
# 重新配置认证
openclaw models auth setup-token --provider anthropic
openclaw models status
```

### 5. OAuth刷新失败

**症状**: `OAuth token refresh failed`

```bash
# 推荐使用setup-token代替OAuth
openclaw models auth setup-token --provider anthropic
openclaw models status
```

### 6. 服务运行但端口不监听

**检查清单**:

- `gateway.mode` 必须是 `local`
- 非loopback需要配置 `gateway.auth.token`
- Tailscale绑定需要Tailscale运行中

```bash
openclaw gateway status
openclaw doctor
```

### 7. 消息不触发回复

**检查清单**:

1. 发送者是否在allowlist中？
2. 群聊是否需要@mention?
3. DM是否需要pairing批准?

```bash
openclaw status
openclaw pairing list <channel>
openclaw logs --follow | grep "blocked\|skip"
```

### 8. WhatsApp断开连接

```bash
# 检查状态
openclaw status --deep

# 查看连接日志
openclaw logs --limit 200 | grep "connection\|disconnect"

# 重新登录
openclaw channels logout
openclaw channels login --verbose
```

### 9. Agent超时

**默认30分钟**，长任务需要调整：

```json
{
  "reply": {
    "timeoutSeconds": 3600  // 1小时
  }
}
```

### 10. 内存占用过高

```json
{
  "session": {
    "historyLimit": 100  // 限制历史消息数
  }
}
```

---

## 🔐 认证配置

### 绑定模式与认证要求

| 绑定模式 | 需要认证 | 说明 |
|:---|:---|:---|
| `loopback` | 可选 | 仅本机访问 |
| `lan` | **必须** | 局域网访问 |
| `tailnet` | **必须** | Tailscale网络 |
| `auto` | 取决于结果 | 自动选择 |

### 配置认证

```bash
# 设置Token认证
openclaw config set gateway.auth.mode token
openclaw config set gateway.auth.token "your-secure-token"

# 或通过环境变量
export OPENCLAW_GATEWAY_TOKEN="your-secure-token"
```

---

## 📝 日志级别配置

```json
{
  "logging": {
    "level": "debug",         // 文件日志级别
    "consoleLevel": "debug",  // 控制台日志级别
    "consoleStyle": "pretty"  // 控制台样式
  }
}
```

---

## 🔄 重置与恢复

### 软重置（保留登录）

```bash
openclaw reset --scope config
```

### 完全重置（需重新登录）

```bash
openclaw gateway stop
openclaw gateway uninstall
rm -rf ~/.openclaw
openclaw channels login
openclaw gateway restart
```

---

## 📁 重要目录

| 路径 | 内容 |
|:---|:---|
| `~/.openclaw/openclaw.json` | 主配置 |
| `~/.openclaw/credentials/` | 凭据 |
| `~/.openclaw/agents/<id>/sessions/` | 会话 |
| `~/.openclaw/logs/` | 服务日志 |
| `/tmp/openclaw/` | 运行时日志 |

---

## 📚 详细文档

- 完整配置参考: `_raw/gateway/configuration.md`
- 故障排查详情: `_raw/gateway/troubleshooting.md`
- 日志配置: `_raw/logging.md`
