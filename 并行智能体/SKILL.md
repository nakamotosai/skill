---
description: 协调多个智能体完成复杂任务。用于多视角分析、综合审查或需要不同领域专长的任务。
---

# 多智能体编排 (Multi-Agent Orchestration)

你现在处于 **编排模式 (ORCHESTRATION MODE)**。你的任务：协调专业智能体来解决这个复杂问题。

## 待编排任务
$ARGUMENTS

---

## 🔴 关键：最低智能体要求

> ⚠️ **编排 = 至少 3 个不同的智能体**
>
> 如果你使用的智能体少于 3 个，你不是在编排——你只是在委派。
>
> **完成前验证：**
> - 统计已调用的智能体
> - 如果 `agent_count < 3` → 停止并调用更多智能体
> - 单个智能体 = 编排失败

### 智能体选择矩阵

| 任务类型 | 必需智能体 (最低要求) |
|-----------|---------------------------|
| **Web 应用** | frontend-specialist, backend-specialist, test-engineer |
| **API** | backend-specialist, security-auditor, test-engineer |
| **UI/设计** | frontend-specialist, seo-specialist, performance-optimizer |
| **数据库** | database-architect, backend-specialist, security-auditor |
| **全栈** | project-planner, frontend-specialist, backend-specialist, devops-engineer |
| **调试** | debugger, explorer-agent, test-engineer |
| **安全** | security-auditor, penetration-tester, devops-engineer |

---

## 预检：模式检查

| 当前模式 | 任务类型 | 动作 |
|--------------|-----------|--------|
| **plan** | 任何 | ✅ 继续采用“先规划”的方法 |
| **edit** | 简单执行 | ✅ 直接继续 |
| **edit** | 复杂/多文件 | ⚠️ 询问："此任务需要规划。切换到 plan 模式吗？" |
| **ask** | 任何 | ⚠️ 询问："准备编排。切换到 edit 或 plan 模式吗？" |

---

## 🔴 严格的两阶段编排

### 第一阶段：规划 (顺序执行 - 无并行智能体)

| 步骤 | 智能体 | 动作 |
|------|-------|--------|
| 1 | `project-planner` | 创建 docs/PLAN.md |
| 2 | (可选) `explorer-agent` | 如果需要，进行代码库探索 |

> 🔴 **规划期间不得使用其他智能体！** 仅限 project-planner 和 explorer-agent。

### ⏸️ 检查点：用户批准

```
PLAN.md 完成后，询问：

"✅ 计划已创建: docs/PLAN.md

您是否批准？(Y/N)
- Y: 开始实施 (Implementation)
- N: 我将修改计划"
```

> 🔴 **没有明确的用户批准，切勿进入第二阶段！**

### 第二阶段：实施 (批准后并行智能体)

| 并行组 | 智能体 |
|----------------|--------|
| 基础 | `database-architect`, `security-auditor` |
| 核心 | `backend-specialist`, `frontend-specialist` |
| 润色 | `test-engineer`, `devops-engineer` |

> ✅ 用户批准后，并行调用多个智能体。

## 可用智能体 (共 17 个)

| 智能体 | 领域 | 适用场景 |
|-------|--------|----------|
| `project-planner` | 规划 | 任务拆解, PLAN.md |
| `explorer-agent` | 探索 | 代码库映射 |
| `frontend-specialist` | UI/UX | React, Vue, CSS, HTML |
| `backend-specialist` | 服务端 | API, Node.js, Python |
| `database-architect` | 数据 | SQL, NoSQL, Schema |
| `security-auditor` | 安全 | 漏洞, 认证 |
| `penetration-tester` | 安全 | 主动测试 |
| `test-engineer` | 测试 | 单元, E2E, 覆盖率 |
| `devops-engineer` | 运维 | CI/CD, Docker, 部署 |
| `mobile-developer` | 移动端 | React Native, Flutter |
| `performance-optimizer` | 速度 | Lighthouse, 性能分析 |
| `seo-specialist` | SEO | Meta, Schema, 排名 |
| `documentation-writer` | 文档 | README, API 文档 |
| `debugger` | 调试 | 错误分析 |
| `game-developer` | 游戏 | Unity, Godot |
| `orchestrator` | 元 | 协调 |

---

## 编排协议

### 步骤 1: 分析任务领域
识别此任务涉及的所有领域：
```
□ 安全         → security-auditor, penetration-tester
□ 后端/API     → backend-specialist
□ 前端/UI      → frontend-specialist
□ 数据库       → database-architect
□ 测试         → test-engineer
□ 运维         → devops-engineer
□ 移动端       → mobile-developer
□ 性能         → performance-optimizer
□ SEO          → seo-specialist
□ 规划         → project-planner
```

### 步骤 2: 阶段检测

| 如果计划存在 | 动作 |
|----------------|--------|
| 无 `docs/PLAN.md` | → 进入第一阶段 (仅规划) |
| 有 `docs/PLAN.md` + 用户已批准 | → 进入第二阶段 (实施) |

### 步骤 3: 基于阶段执行

**第一阶段 (规划):**
```
使用 project-planner 智能体创建 PLAN.md
→ 计划创建后停止
→ 询问用户批准
```

**第二阶段 (实施 - 批准后):**
```
并行调用智能体：
使用 frontend-specialist 智能体 [任务]
使用 backend-specialist 智能体 [任务]
使用 test-engineer 智能体 [任务]
```

**🔴 关键：上下文传递 (强制性)**

当调用**任何**子智能体时，必须包含：

1. **原始用户请求：** 用户询问的全文
2. **已做出的决定：** 用户对苏格拉底式提问的所有回答
3. **前序智能体工作：** 前一个智能体做了什么的总结
4. **当前计划状态：** 如果 `~/.claude/plans/` 有计划，包含它

**带有完整上下文的示例：**
```
使用 project-planner 智能体创建 PLAN.md:

**上下文:**
- 用户请求: "面向学生的社交平台，使用模拟数据"
- 决定: 技术栈=Vue 3, 布局=Grid Widget, 认证=Mock, 设计=年轻动态
- 前序工作: 编排器问了 6 个问题，用户选择了所有选项
- 当前计划: ~/.claude/plans/playful-roaming-dream.md 存在初始结构

**任务:** 基于以上决定创建详细的 PLAN.md。不要根据文件夹名称推断。
```

> ⚠️ **违规：** 调用子智能体不带完整上下文 = 子智能体会做出错误的假设！


### 步骤 4: 验证 (强制性)
**最后**一个智能体必须运行适当的验证脚本：
```bash
python ~/.claude/skills/vulnerability-scanner/scripts/security_scan.py .
python ~/.claude/skills/lint-and-validate/scripts/lint_runner.py .
```

### 步骤 5: 综合结果
将所有智能体的输出合并为统一的报告。

---

## 输出格式

```markdown
## 🎼 编排报告

### 任务
[原始任务摘要]

### 模式
[当前 Claude Code 模式: plan/edit/ask]

### 已调用的智能体 (最少 3 个)
| # | 智能体 | 关注领域 | 状态 |
|---|-------|------------|--------|
| 1 | project-planner | 任务拆解 | ✅ |
| 2 | frontend-specialist | UI 实现 | ✅ |
| 3 | test-engineer | 验证脚本 | ✅ |

### 已执行的验证脚本
- [x] security_scan.py → 通过/失败
- [x] lint_runner.py → 通过/失败

### 关键发现
1. **[智能体 1]**: 发现
2. **[智能体 2]**: 发现
3. **[智能体 3]**: 发现

### 交付物
- [ ] PLAN.md 已创建
- [ ] 代码已实现
- [ ] 测试通过
- [ ] 脚本已验证

### 总结
[一段话综合所有智能体的工作]
```

---

## 🔴 出口门禁

完成编排前，请验证：

1. ✅ **智能体数量：** `invoked_agents >= 3`
2. ✅ **脚本执行：** 至少运行了 `security_scan.py`
3. ✅ **报告生成：** 包含所有列出智能体的编排报告

> **如果有任何检查失败 → 不要标记编排完成。调用更多智能体或运行脚本。**

---

**现在开始编排。选择 3+ 个智能体，顺序执行，运行验证脚本，综合结果。**
