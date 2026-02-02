---
description: 创建新应用指令。触发应用构建技能并与用户开始交互式对话。
---

# /create - 创建应用

$ARGUMENTS

---

## 任务

此指令启动新应用的创建流程。

### 步骤:

1. **需求分析**
   - 理解用户想要什么
   - 如果信息缺失，使用 `conversation-manager` 技能进行询问

2. **项目规划**
   - 使用 `project-planner` 智能体进行任务拆解
   - 确定技术栈
   - 规划文件结构
   - 创建计划文件并进入构建阶段

3. **应用构建 (获得批准后)**
   - 使用 `app-builder` 技能进行编排
   - 协调专家智能体:
     - `database-architect` → 数据库架构
     - `backend-specialist` → 后端 API
     - `frontend-specialist` → 前端 UI

4. **预览**
   - 完成后使用 `auto_preview.py` 启动
   - 向用户展示 URL

---

## 使用示例

```
/create blog site
/create e-commerce app with product listing and cart
/create todo app
/create Instagram clone
/create crm system with customer management
```

---

## 开始之前

如果请求不清楚，请问这些问题:
- 什么样的应用？
- 有哪些基本功能？
- 谁会使用它？

使用默认设置，稍后添加细节。
