---
name: OpenClaw CLI命令速查
description: OpenClaw全部CLI命令的速查手册，包含41个命令的用法和常用选项
---

# OpenClaw CLI 命令速查

> 完整的 `openclaw` 命令参考手册

---

## 🌐 全局选项

| 选项 | 说明 |
|:---|:---|
| `--dev` | 隔离到 `~/.openclaw-dev` 目录 |
| `--profile <name>` | 隔离到 `~/.openclaw-<name>` |
| `--no-color` | 禁用ANSI颜色 |
| `-V`, `--version` | 显示版本 |

---

## 📋 命令树概览

```
openclaw
├── setup / onboard / configure    # 初始化
├── doctor / reset / uninstall     # 维护
├── status / health                # 状态
├── gateway                        # Gateway管理
├── channels                       # 渠道管理
├── message                        # 消息发送
├── agent / agents                 # Agent管理
├── models                         # 模型管理
├── pairing                        # 设备配对
├── plugins / skills               # 插件/技能
├── sandbox                        # 沙箱
├── browser                        # 浏览器控制
├── cron                          # 定时任务
├── memory                        # 记忆搜索
├── logs                          # 日志
└── security                      # 安全审计
```

---

## 🚀 初始化命令

### `onboard` - 引导向导

```bash
openclaw onboard                      # 交互式向导
openclaw onboard --install-daemon     # 安装后台服务

# 非交互式
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$KEY" \
  --gateway-port 18789 \
  --install-daemon
```

**常用选项**：

- `--mode <local|remote>`
- `--auth-choice <apiKey|setup-token|openai-codex|gemini-api-key|...>`
- `--gateway-port <port>`
- `--gateway-bind <loopback|lan|tailnet>`
- `--install-daemon` / `--no-install-daemon`
- `--daemon-runtime <node|bun>` (推荐node)

### `configure` - 重新配置

```bash
openclaw configure                    # 交互式
openclaw configure --section web      # 只配置Web搜索
```

### `doctor` - 诊断修复

```bash
openclaw doctor              # 健康检查
openclaw doctor --deep       # 深度扫描
openclaw doctor --yes        # 自动应用修复
```

---

## 📊 状态命令

### `status` - 当前状态

```bash
openclaw status           # 基本状态
openclaw status --all     # 完整诊断（可粘贴）
openclaw status --deep    # 探测渠道
openclaw status --usage   # 显示配额使用
openclaw status --json    # JSON输出
```

### `health` - 健康检查

```bash
openclaw health           # Gateway健康
openclaw health --json
```

---

## 🔌 Gateway 命令

### `gateway` - 运行/管理

```bash
# 前台运行
openclaw gateway --port 18789 --verbose

# 服务管理
openclaw gateway status    # 状态（含RPC探测）
openclaw gateway install   # 安装服务
openclaw gateway start     # 启动
openclaw gateway stop      # 停止
openclaw gateway restart   # 重启
openclaw gateway uninstall # 卸载

# 高级
openclaw gateway call <method> --params <json>
openclaw gateway discover   # 发现网络上的Gateway
```

**常用选项**：

- `--port <port>`
- `--bind <loopback|lan|tailnet|auto>`
- `--token <token>`
- `--tailscale <off|serve|funnel>`
- `--verbose`
- `--force` (强制占用端口)

### `logs` - 查看日志

```bash
openclaw logs --follow     # 实时跟踪
openclaw logs --limit 200  # 最近200条
openclaw logs --json       # JSON格式
```

---

## 💬 渠道命令

### `channels` - 渠道管理

```bash
openclaw channels list               # 列出渠道
openclaw channels status             # 渠道状态
openclaw channels status --probe     # 深度检测
openclaw channels login              # WhatsApp扫码登录
openclaw channels logout             # 登出

# 添加渠道
openclaw channels add --channel telegram --token $TOKEN
openclaw channels add --channel discord --token $TOKEN

# 删除渠道
openclaw channels remove --channel discord --delete
```

### `pairing` - 设备配对

```bash
openclaw pairing list whatsapp       # 查看待批准
openclaw pairing list telegram
openclaw pairing list discord

openclaw pairing approve whatsapp <code>   # 批准
openclaw pairing approve telegram <code>
openclaw pairing approve discord <code>
```

---

## 📤 消息命令

### `message` - 发送消息

```bash
# 发送
openclaw message send --target +15555550123 --message "Hi"
openclaw message send --channel discord --target channel:123 --message "Test"

# 投票
openclaw message poll --channel discord --target channel:123 \
  --poll-question "选择?" --poll-option A --poll-option B

# 其他
openclaw message react / read / edit / delete / pin / unpin
openclaw message thread create / list / reply
```

### `agent` - Agent调用

```bash
openclaw agent --message "Hello"
openclaw agent --message "Hi" --to +15555550123
openclaw agent --message "Hi" --local    # 本地运行
openclaw agent --message "Hi" --deliver  # 发送回复
openclaw agent --message "Hi" --json
```

### `agents` - 多Agent管理

```bash
openclaw agents list                     # 列出
openclaw agents add work --workspace ~/.openclaw/workspace-work
openclaw agents delete work --force
```

---

## 🤖 模型命令

### `models` - 模型管理

```bash
openclaw models                      # 等同于 models status
openclaw models list                 # 列出可用模型
openclaw models list --all           # 所有模型
openclaw models status               # 认证状态
openclaw models status --probe       # 实时探测

# 设置默认模型
openclaw models set openai/gpt-4
openclaw models set anthropic/claude-3.5-sonnet

# 认证
openclaw models auth add --provider anthropic
openclaw models auth setup-token --provider anthropic

# 别名
openclaw models aliases list
openclaw models aliases add fast openai/gpt-4-mini
openclaw models aliases remove fast

# 回退
openclaw models fallbacks list
openclaw models fallbacks add anthropic/claude-3.5-sonnet
```

---

## 🔧 其他命令

### `security` - 安全审计

```bash
openclaw security audit           # 审计配置
openclaw security audit --deep    # 深度审计
openclaw security audit --fix     # 自动修复
```

### `plugins` - 插件管理

```bash
openclaw plugins list
openclaw plugins info <id>
openclaw plugins install <path|npm-spec>
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins doctor
```

### `skills` - 技能管理

```bash
openclaw skills list
openclaw skills list --eligible   # 只显示可用
openclaw skills info <name>
openclaw skills check             # 检查依赖
```

### `sandbox` - 沙箱管理

```bash
openclaw sandbox list
openclaw sandbox recreate
openclaw sandbox explain
```

### `memory` - 记忆搜索

```bash
openclaw memory status            # 索引状态
openclaw memory index             # 重建索引
openclaw memory search "query"    # 语义搜索
```

### `browser` - 浏览器控制

```bash
openclaw browser status
openclaw browser start / stop
openclaw browser tabs
openclaw browser open <url>
openclaw browser screenshot
openclaw browser click / type / press
```

### `cron` - 定时任务

```bash
openclaw cron list
openclaw cron status
openclaw cron add
openclaw cron edit <id>
openclaw cron rm <id>
openclaw cron enable / disable <id>
```

### `reset` - 重置配置

```bash
openclaw reset --scope config                    # 只重置配置
openclaw reset --scope config+creds+sessions     # 重置配置+凭据
openclaw reset --scope full --yes                # 完全重置
```

### `uninstall` - 卸载

```bash
openclaw uninstall --service      # 卸载服务
openclaw uninstall --all --yes    # 完全卸载
```

---

## 📚 详细文档

完整CLI参考请查阅 `_raw/cli/` 目录下的41个命令文档。
