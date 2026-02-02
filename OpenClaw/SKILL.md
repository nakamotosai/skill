---
name: OpenClaw完整指南
description: OpenClaw官方文档的分层索引，按场景路由到对应子Skill获取详细操作指令。
---

# OpenClaw 分层知识库

> 本知识库从官方文档自动生成，覆盖301个MD文件。
> 来源: <https://github.com/openclaw/openclaw>

---

## 🎯 快速导航

| 场景 | 对应子Skill | 主要内容 |
| :--- | :--- | :--- |
| 首次安装/配置 | `01-快速开始/SKILL.md` | 安装、onboard、wizard、pairing |
| 查找CLI命令 | `02-CLI命令/SKILL.md` | 41个CLI命令速查 |
| Gateway不工作 | `03-Gateway运维/SKILL.md` | 配置、日志、健康检查 |
| 配置聊天渠道 | `04-聊天渠道/SKILL.md` | Discord/Telegram/WhatsApp等 |
| 工具与插件 | `05-工具与插件/SKILL.md` | Tools、Skills、Plugins |
| 理解内部机制 | `06-核心概念/SKILL.md` | Agent、Session、Memory |
| 安全加固 | `07-安全配置/SKILL.md` | Sandbox、权限、审计 |
| 报错排查 | `08-故障排查/SKILL.md` | 决策树快速排查 |

---

## 🔥 常用速查（无需加载子Skill）

### 服务控制

```bash
# 重启服务
systemctl --user restart openclaw-gateway

# 查看状态
systemctl --user status openclaw-gateway

# 查看日志
journalctl --user -u openclaw-gateway -f
```

### 关键配置文件

| 文件 | 用途 |
|:---|:---|
| `~/.openclaw/openclaw.json` | 主配置 |
| `~/.openclaw/clawdbot.json` | Agent配置（模型等） |
| `~/.openclaw/credentials/` | OAuth凭据 |
| `~/.openclaw/workspace/` | Agent工作区 |

### 快速诊断

```bash
openclaw status         # 当前状态
openclaw health         # 健康检查
openclaw doctor         # 诊断问题
openclaw security audit # 安全审计
```

### Pairing（绑定设备）

```bash
# 查看待批准列表
openclaw pairing list <channel>

# 批准绑定
openclaw pairing approve <channel> <code>
```

---

## 📁 原始文档

完整官方MD文档存放在 `_raw/` 目录，按原始目录结构保留：

```
_raw/
├── start/          # 入门指南 (9个)
├── cli/            # CLI命令 (41个)
├── gateway/        # Gateway (28个)
├── channels/       # 聊天渠道 (22个)
├── concepts/       # 核心概念
├── tools/          # 工具
├── plugins/        # 插件
├── security/       # 安全
├── help/           # 帮助
└── ...             # 其他
```

---

## 🔄 更新方法

使用 `GitHub文档下载器` Skill 重新拉取最新文档：

```powershell
# 在 C:\Users\sai\.agent\skills\GitHub文档下载器\scripts\ 下
.\fetch_docs.ps1 -Repo "openclaw/openclaw" -DocsPath "docs" -OutputDir "C:\Users\sai\.agent\skills\OpenClaw\_raw"
```

---

## 📖 使用说明

1. **遇到OpenClaw问题时**：先阅读本主Skill
2. **根据场景路由表**：`view_file` 加载对应子Skill
3. **需要深入细节时**：查阅 `_raw/` 目录的原始文档
