---
name: OpenClaw安全配置
description: 沙箱、权限控制、安全审计和最佳实践
---

# OpenClaw 安全配置

> 沙箱隔离、权限控制和安全加固

---

## 🔒 安全审计

### 快速审计

```bash
openclaw security audit         # 基本审计
openclaw security audit --deep  # 深度审计
openclaw security audit --fix   # 自动修复
```

---

## 📦 沙箱 (Sandboxing)

### 概述

OpenClaw可以在Docker容器中运行工具，限制文件和进程访问。

### 沙箱模式

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main"  // off | non-main | all
      }
    }
  }
}
```

| 模式 | 说明 |
|:---|:---|
| `off` | 不使用沙箱 |
| `non-main` | 仅非主会话沙箱 |
| `all` | 所有会话都沙箱 |

### 沙箱范围

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "scope": "session"  // session | agent | shared
      }
    }
  }
}
```

### 工作区访问

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "workspaceAccess": "none"  // none | ro | rw
      }
    }
  }
}
```

| 模式 | 说明 |
|:---|:---|
| `none` | 使用隔离的沙箱工作区 |
| `ro` | 只读挂载Agent工作区 |
| `rw` | 读写挂载Agent工作区 |

### 沙箱设置

```bash
# 构建沙箱镜像
scripts/sandbox-setup.sh

# 浏览器沙箱
scripts/sandbox-browser-setup.sh
```

### 调试沙箱

```bash
openclaw sandbox list       # 列出沙箱
openclaw sandbox explain    # 解释当前沙箱配置
openclaw sandbox recreate   # 重建沙箱
```

---

## 🛡️ 工具权限

### 允许/禁止工具

```json
{
  "tools": {
    "allow": ["group:fs", "browser"],
    "deny": ["exec", "process"]
  }
}
```

> `deny` 优先于 `allow`

### 工具Profile

```json
{
  "tools": {
    "profile": "minimal"  // minimal | coding | messaging | full
  }
}
```

### 提权执行 (Elevated)

```json
{
  "tools": {
    "elevated": true  // 允许沙箱任务在主机执行
  }
}
```

> ⚠️ 提权执行绕过沙箱，仅在必要时启用

---

## 🔐 认证安全

### Gateway认证

```json
{
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "your-secure-token"
    }
  }
}
```

| 绑定模式 | 认证要求 |
|:---|:---|
| `loopback` | 可选 |
| `lan` | **必须** |
| `tailnet` | **必须** |

### DM安全 (Pairing)

```json
{
  "channels": {
    "discord": {
      "dm": {
        "policy": "pairing"  // pairing | allowlist | open | disabled
      }
    }
  }
}
```

---

## 📋 安全检查清单

### 配置级别

- [ ] 设置 `gateway.auth.token` (非loopback必须)
- [ ] 使用 `dmPolicy: "pairing"` 或 `"allowlist"`
- [ ] 配置 `allowFrom` 白名单
- [ ] 启用沙箱 (`sandbox.mode: "non-main"`)

### 运行级别

- [ ] 定期运行 `openclaw security audit`
- [ ] 检查日志中的未授权访问
- [ ] 更新到最新版本

### Skills安全

- [ ] 审查第三方Skills代码
- [ ] 在沙箱中运行不受信任的Skills
- [ ] 不在日志/提示中暴露API Key

---

## ⚙️ 最小安全配置

```json
{
  "gateway": {
    "mode": "local",
    "auth": {
      "mode": "token",
      "token": "your-secure-token"
    }
  },
  "channels": {
    "whatsapp": {
      "dmPolicy": "allowlist",
      "allowFrom": ["+your-number"]
    },
    "telegram": {
      "dmPolicy": "pairing"
    },
    "discord": {
      "dm": {
        "policy": "pairing"
      }
    }
  },
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "workspaceAccess": "none"
      }
    }
  }
}
```

---

## 🚨 安全红线

| 不要做 | 应该做 |
|:---|:---|
| 使用 `dmPolicy: "open"` 无限制 | 使用 `"pairing"` 或 `"allowlist"` |
| 非loopback无认证 | 设置 `gateway.auth.token` |
| 暴露Token在日志中 | 使用环境变量 |
| 给Bot管理员权限 | 只给必要的最小权限 |
| 信任所有第三方Skills | 审查代码后再使用 |

---

## 📚 详细文档

- 沙箱详解: `_raw/gateway/sandboxing.md`
- 安全概览: `_raw/gateway/security/`
- 工具策略: `_raw/gateway/sandbox-vs-tool-policy-vs-elevated.md`
- Exec审批: `_raw/tools/exec-approvals.md`
