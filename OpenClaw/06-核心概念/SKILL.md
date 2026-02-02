---
name: OpenClaw核心概念
description: Agent、Session、Memory、Context等核心机制的理解指南
---

# OpenClaw 核心概念

> 理解OpenClaw内部机制

---

## 🤖 Agent 运行时

### 工作区 (Workspace)

Agent的工作目录，所有工具操作都在此进行：

```
~/.openclaw/workspace/
├── AGENTS.md      # 操作指令 + "记忆"
├── SOUL.md        # 人设、边界、语气
├── TOOLS.md       # 用户维护的工具说明
├── IDENTITY.md    # Agent名称/风格
├── USER.md        # 用户资料
├── BOOTSTRAP.md   # 首次运行仪式(完成后删除)
└── skills/        # 工作区Skills
```

### 多Agent设置

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.openclaw/workspace",
      "model": { "primary": "anthropic/claude-3.5-sonnet" }
    },
    "list": [
      {
        "id": "support",
        "workspace": "~/.openclaw/workspace-support",
        "tools": { "profile": "messaging" }
      }
    ]
  }
}
```

---

## 💬 Session 管理

### Session Key结构

| 类型 | Key格式 |
|:---|:---|
| 主会话(DM) | `agent:<agentId>:main` |
| 群聊 | `agent:<agentId>:<channel>:group:<id>` |
| 频道 | `agent:<agentId>:<channel>:channel:<id>` |
| Cron | `cron:<jobId>` |

### DM范围控制

```json
{
  "session": {
    "dmScope": "main"  // main | per-peer | per-channel-peer
  }
}
```

| 模式 | 说明 |
|:---|:---|
| `main` | 所有DM共享主会话 |
| `per-peer` | 按发送者隔离 |
| `per-channel-peer` | 按渠道+发送者隔离 |

### Session重置策略

```json
{
  "session": {
    "reset": {
      "mode": "daily",
      "atHour": 4,
      "idleMinutes": 120
    }
  }
}
```

### 重置触发器

- `/new` 或 `/reset` - 开始新会话
- `/new <model>` - 新会话并切换模型
- `/compact` - 压缩上下文

---

## 🧠 Memory 记忆系统

### 记忆文件

```
<workspace>/
├── MEMORY.md        # 主记忆文件
└── memory/          # 分类记忆
    ├── projects.md
    └── preferences.md
```

### 记忆搜索

```bash
openclaw memory status    # 索引状态
openclaw memory index     # 重建索引
openclaw memory search "query"  # 语义搜索
```

### 自动记忆刷新

Session接近压缩时，自动提醒Agent保存重要信息到磁盘。

---

## 📝 Context 上下文

### 系统提示组成

1. **Bootstrap文件**: AGENTS.md, SOUL.md, TOOLS.md等
2. **Skills列表**: 可用技能及其说明
3. **工具schema**: 可用工具的定义
4. **会话历史**: 之前的对话

### 查看上下文

```
/context list    # 列出上下文内容
/context detail  # 详细上下文
/status          # 当前状态
```

### 上下文压缩

```
/compact         # 手动压缩
/compact 保留最近讨论的项目细节   # 带指令压缩
```

---

## 📊 Model 配置

### 模型设置

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-3.5-sonnet"
      }
    }
  }
}
```

### 模型格式

```
provider/model
例如: anthropic/claude-3.5-sonnet
     openai/gpt-4
     google/gemini-pro
```

### 模型回退

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-3.5-sonnet",
        "fallbacks": ["openai/gpt-4"]
      }
    }
  }
}
```

---

## 🔄 消息队列

### 队列模式

| 模式 | 说明 |
|:---|:---|
| `steer` | 工具调用间注入新消息 |
| `followup` | 当前turn结束后处理 |
| `collect` | 收集多条消息一起处理 |

---

## 📡 Streaming 流式输出

### Block Streaming

```json
{
  "agents": {
    "defaults": {
      "blockStreamingDefault": "on"
    }
  }
}
```

### Draft Streaming (Telegram)

```json
{
  "channels": {
    "telegram": {
      "streamMode": "partial"  // off | partial | block
    }
  }
}
```

---

## 🗂️ 重要目录

| 路径 | 内容 |
|:---|:---|
| `~/.openclaw/openclaw.json` | 主配置 |
| `~/.openclaw/workspace/` | 默认工作区 |
| `~/.openclaw/agents/<id>/sessions/` | 会话数据 |
| `~/.openclaw/credentials/` | 凭据 |
| `~/.openclaw/skills/` | 共享Skills |

---

## 📚 详细文档

- Agent运行时: `_raw/concepts/agent.md`
- Session管理: `_raw/concepts/session.md`
- Memory系统: `_raw/concepts/memory.md`
- Context管理: `_raw/concepts/context.md`
- 多Agent: `_raw/concepts/multi-agent.md`
- 模型配置: `_raw/concepts/models.md`
