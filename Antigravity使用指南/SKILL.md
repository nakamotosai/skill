---
name: Antigravity使用指南
description: 指导如何在 Antigravity 环境中创建、管理和使用 Skill (技能) 系统。
---

# Antigravity Skills 使用手册

> **在 Antigravity Kit 中创建与使用技能的权威指南**

---

## 📋 简介

虽然 Antigravity 的核心模型（如 Gemini）拥有强大的通用能力，但它们并不自动了解特定项目的上下文或您的团队标准。如果将每个规则或工具都硬塞进 Agent 的上下文窗口，会导致“工具膨胀”、成本增加、响应延迟以及模型混淆。

**Antigravity Skills** 通过 **渐进式披露 (Progressive Disclosure)** 机制解决了这一问题。技能是一包专门的知识，在需要之前处于休眠状态。只有当您的具体请求与技能的描述匹配时，相关信息才会被加载进 Agent 的上下文。

---

## 📁 结构与范围

技能是基于目录的包。您可以根据需要定义以下范围：

| 范围 | 路径 | 描述 |
|---------|-----------|-------|
| **Workspace** | `<workspace-root>/.agent/skills/` | 仅在特定项目中可用 |
| **Global** | `C:\Users\sai\.agent\skills\` | 在所有本地项目中全局可用 |

### 技能目录结构

```
my-skill/
├── SKILL.md      # (必填) 元数据与指令
├── scripts/      # (可选) Python 或 Bash 脚本
├── references/   # (可选) 文本、文档、模板
└── assets/       # (可选) 图片或图标
```

---

## 🔍 示例 1：代码审查技能 (Code Review Skill)

这是一个纯指令型的技能，只需要创建一个 `SKILL.md` 文件。

### 第一步：创建目录

```bash
mkdir -p ~/.agent/skills/code-review
```

### 第二步：编写 SKILL.md

```markdown
---
name: code-review
description: 审查代码变更中的 Bug、格式问题和最佳实践。用于 PR 审查或代码质量检查。
---

# 代码审查技能

在审查代码时，请遵循以下步骤：

## 审查清单

1. **正确性**：代码是否实现了预期功能？
2. **边缘情况**：是否处理了错误和异常？
3. **风格**：是否符合项目的编码规范？
4. **性能**：是否存在明显的效率低下？

## 如何提供反馈

- 指出需要修改的具体位置
- 解释“为什么”要改，而不仅仅是“改什么”
- 尽可能提供替代方案
```

> **注意**：`SKILL.md` 的顶部包含元数据 (name, description)，Agent 会先读取元数据，仅在需要时才会加载后续指令。

---

## 📄 示例 2：许可证头部技能 (License Header Skill)

此技能演示了如何使用 `resources/` 目录中的参考文件。

### 第一步：创建目录结构

```bash
mkdir -p .agent/skills/license-header-adder/resources
```

### 第二步：创建模板文件

**`.agent/skills/license-header-adder/resources/HEADER.txt`**:

```
/*
 * Copyright (c) 2026 YOUR_COMPANY_NAME LLC.
 * All rights reserved.
 * This code is proprietary and confidential.
 */
```

### 第三步：编写 SKILL.md

```markdown
---
name: license-header-adder
description: 为新源代码文件自动添加标准的商业许可证头部。
---

# 许可证头部添加器

此技能确保所有新文件都包含正确的版权声明。

## 操作指令

1. **读取模板**：读取 `resources/HEADER.txt` 的内容。
2. **应用到文件**：在创建新文件时，将此内容原样置于文件最顶部。
3. **适配语法**：
   - C 风格语言（Java, TS）：保持 `/* */` 块。
   - Python/Shell：转换为 `#` 注释风格。
```

---

## 🎯 总结

通过创建 Skills，您可以将通用的 AI 模型转变为您项目的专属专家：

- ✅ 系统化最佳实践
- ✅ 强制执行代码审查规则
- ✅ 自动化重复性任务（如添加 License）
- ✅ 让 Agent 自动适应团队的工作流

不再需要反复提醒 AI “记得加注释”或“注意格式”，Agent 现在会自动学会！
