---
name: OpenClaw工具与插件
description: Agent工具、Skills系统、插件开发和ClawHub使用指南
---

# OpenClaw 工具与插件

> Agent可用的工具、技能系统和插件扩展

---

## 🛠️ 核心工具概览

### 工具分组

| 分组 | 工具 | 说明 |
|:---|:---|:---|
| `group:runtime` | exec, bash, process | Shell执行 |
| `group:fs` | read, write, edit, apply_patch | 文件操作 |
| `group:web` | web_search, web_fetch | 网页搜索/抓取 |
| `group:ui` | browser, canvas | 浏览器/画布 |
| `group:sessions` | sessions_list/history/send/spawn | 会话管理 |
| `group:memory` | memory_search, memory_get | 记忆搜索 |
| `group:messaging` | message | 消息发送 |
| `group:automation` | cron, gateway | 自动化 |
| `group:nodes` | nodes | 节点控制 |

---

## 🔧 常用工具

### `exec` - Shell执行

```json
{
  "command": "ls -la",
  "yieldMs": 10000,
  "timeout": 1800,
  "elevated": false
}
```

**参数**：

- `command`: 命令
- `yieldMs`: 自动后台超时(默认10秒)
- `timeout`: 总超时(默认1800秒)
- `elevated`: 提权执行(沙箱→主机)

### `process` - 后台进程管理

```json
{ "action": "list" }
{ "action": "poll", "sessionId": "xxx" }
{ "action": "log", "sessionId": "xxx", "limit": 100 }
{ "action": "kill", "sessionId": "xxx" }
```

### `web_search` - 网页搜索

```json
{
  "query": "OpenClaw documentation",
  "count": 5
}
```

> 需要 Brave API Key：`openclaw configure --section web`

### `web_fetch` - 网页抓取

```json
{
  "url": "https://example.com",
  "extractMode": "markdown",
  "maxChars": 10000
}
```

### `browser` - 浏览器控制

```json
{ "action": "status" }
{ "action": "start" }
{ "action": "open", "url": "https://example.com" }
{ "action": "snapshot", "mode": "ai" }
{ "action": "act", "ref": 12, "action": "click" }
{ "action": "screenshot" }
```

### `message` - 消息发送

```json
{
  "action": "send",
  "channel": "telegram",
  "to": "123456789",
  "message": "Hello"
}
```

---

## 📦 工具策略配置

### 允许/禁止工具

```json
{
  "tools": {
    "allow": ["group:fs", "browser"],
    "deny": ["exec"]
  }
}
```

### 工具Profile

```json
{
  "tools": {
    "profile": "coding"  // minimal | coding | messaging | full
  }
}
```

| Profile | 包含工具 |
|:---|:---|
| `minimal` | 仅 session_status |
| `coding` | 文件、运行时、会话、记忆、图片 |
| `messaging` | 消息、会话 |
| `full` | 全部 |

---

## ⭐ Skills 系统

### Skill位置与优先级

| 位置 | 优先级 | 说明 |
|:---|:---|:---|
| `<workspace>/skills` | 最高 | 工作区特定 |
| `~/.openclaw/skills` | 中 | 共享/本地 |
| 内置skills | 最低 | 随安装附带 |

### Skill格式

```markdown
---
name: my-skill
description: 这个Skill做什么
metadata: {"openclaw": {"requires": {"bins": ["python"]}}}
---

# 使用说明

这里是Agent如何使用这个Skill的指导...
```

### 配置Skill

```json
{
  "skills": {
    "entries": {
      "my-skill": {
        "enabled": true,
        "apiKey": "xxx",
        "env": {
          "MY_API_KEY": "xxx"
        }
      }
    }
  }
}
```

### ClawHub (Skills商店)

```bash
# 安装Skill
clawhub install <skill-slug>

# 更新所有
clawhub update --all

# 同步
clawhub sync --all
```

浏览：<https://clawhub.com>

---

## 🔌 插件系统

### 插件管理

```bash
openclaw plugins list
openclaw plugins info <id>
openclaw plugins install <path|npm-spec>
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins doctor
```

### 插件配置

```json
{
  "plugins": {
    "entries": {
      "my-plugin": {
        "enabled": true
      }
    }
  }
}
```

### 常用插件

| 插件 | 功能 |
|:---|:---|
| Lobster | 可恢复工作流运行时 |
| LLM Task | JSON-only LLM步骤 |
| Voice Call | 语音通话 |

---

## 🎮 Slash命令

### 内置命令

| 命令 | 功能 |
|:---|:---|
| `/status` | 快速诊断 |
| `/reset` | 重置会话 |
| `/model` | 切换模型 |
| `/config` | 配置更改 |
| `/debug` | 调试选项 |

### 配置

```json
{
  "commands": {
    "native": true,   // 平台原生命令
    "text": true,     // 文本命令
    "config": true,   // 允许/config命令
    "restart": true   // 允许/restart命令
  }
}
```

---

## 🔒 安全注意

- 第三方Skills视为**可信代码**，使用前请审查
- 沙箱运行不受信任的输入
- `skills.entries.*.env` 注入到主机进程，不是沙箱
- 详见 `07-安全配置/SKILL.md`

---

## 📚 详细文档

- 工具索引: `_raw/tools/index.md`
- Skills系统: `_raw/tools/skills.md`
- ClawHub: `_raw/tools/clawhub.md`
- 浏览器工具: `_raw/tools/browser.md`
- 插件开发: `_raw/plugin.md`
