---
description: 使用 project-planner 智能体创建项目计划。不编写代码——仅生成计划文件。
---

# /plan - 项目规划模式

$ARGUMENTS

---

## 🔴 关键规则

1. **不写代码** - 此指令仅创建计划文件
2. **使用 project-planner 智能体** - 不要使用 Claude Code 原生的 Plan 子智能体
3. **苏格拉底式门禁** - 规划前询问澄清性问题
4. **动态命名** - 基于任务命名计划文件

---

## 任务

使用 `project-planner` 智能体并提供此上下文：

```
CONTEXT:
- User Request: $ARGUMENTS
- Mode: PLANNING ONLY (no code)
- Output: docs/PLAN-{task-slug}.md (dynamic naming)

NAMING RULES:
1. Extract 2-3 key words from request
2. Lowercase, hyphen-separated
3. Max 30 characters
4. Example: "e-commerce cart" → PLAN-ecommerce-cart.md

RULES:
1. Follow project-planner.md Phase -1 (Context Check)
2. Follow project-planner.md Phase 0 (Socratic Gate)
3. Create PLAN-{slug}.md with task breakdown
4. DO NOT write any code files
5. REPORT the exact file name created
```

---

## 预期输出

| 交付物 | 位置 |
|-------------|----------|
| 项目计划 | `docs/PLAN-{task-slug}.md` |
| 任务拆解 | 计划文件内 |
| 智能体分配 | 计划文件内 |
| 验证检查清单 | 计划文件中的 Phase X |

---

## 规划之后

告诉用户：
```
[OK] Plan created: docs/PLAN-{slug}.md

Next steps:
- Review the plan
- Run `/create` to start implementation
- Or modify plan manually
```

---

## 命名示例

| 请求 | 计划文件 |
|---------|-----------|
| `/plan e-commerce site with cart` | `docs/PLAN-ecommerce-cart.md` |
| `/plan mobile app for fitness` | `docs/PLAN-fitness-app.md` |
| `/plan add dark mode feature` | `docs/PLAN-dark-mode.md` |
| `/plan fix authentication bug` | `docs/PLAN-auth-fix.md` |
| `/plan SaaS dashboard` | `docs/PLAN-saas-dashboard.md` |

---

## 用法

```
/plan e-commerce site with cart
/plan mobile app for fitness tracking
/plan SaaS dashboard with analytics
```
