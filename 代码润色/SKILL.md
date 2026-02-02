---
description: UI 一致性与 Token 执行器。强制执行“零硬编码”策略，将样式标准化为设计系统，并在应用中推广“黄金标准”风格。
---

# /polish - UI 一致性执行器

$ARGUMENTS

---

## ✨ 概述

此指令启动 **UI 标准化协议 (UI Standardization Protocol)**。它旨在治愈“UI 碎片化”并强制执行严格的 **零硬编码 (Zero Hardcoding)** 策略。

**主要目标：** 将混乱的 UI（硬编码值、不一致的样式）转化为 **Token 驱动的设计系统**。

**工作流阶段：**

1. **深度清除** (硬编码扫描与架构检查)
2. **Token 化** (提取黄金标准)
3. **推广** (全局重构)
4. **视觉审计** (最终润色)

---

## 1. 深度清除 (硬编码扫描)

**动作：**
扫描代码库中的“样式债务”（硬编码值）。

**步骤：**

1. **扫描颜色：**
    - `grep -rE "#[0-9a-fA-F]{3,6}|rgb\(|hsl\(" src/`
    - **规则：** 组件中不允许使用原始 Hex 代码。
2. **扫描排版：**
    - `grep -rE "font-size:|px" src/`
    - **规则：** 不允许魔术像素值 (`13px`, `18px`)。
3. **架构检查：**
    - **新项目：** 如果没有 `tailwind.config.js` 或 `theme.ts`，**立即创建**。
    - **旧项目：** 将现有的硬编码集群（例如：50 种不同的灰色）映射到最近的标准 Token。

**输出：**

- `docs/STYLE_DEBT_REPORT.md`: 列出所有硬编码违规行为。

---

## 2. Token 化 (标准化)

**动作：**
建立“黄金标准”并定义架构。

**步骤：**

1. **选择目标：**
    - 询问用户：*“哪个组件是黄金标准？”* (例如：主页上的搜索栏)。
    - 或询问风格：*“目标风格是什么？”* (例如：玻璃拟态、粗野主义)。
2. **提取与定义：**
    - 分析目标的 CSS。
    - **创建/更新 Token：**
        - 颜色：`bg-surface-primary`, `text-content-subtle`
        - 圆角：`rounded-box`
        - 阴影：`shadow-elevation-low`
    - **写入：** `tailwind.config.js` 或 `design-tokens.css`。

---

## 3. 推广 (重构)

**动作：**
大替换。全局应用 Token。

**步骤：**

1. **替换颜色：**
    - `sed` 或 Refactor Agent: 替换 `#efefef` -> `bg-surface-neutral`。
2. **替换间距：**
    - 将 margin/padding 标准化为 4px 网格 (`p-4`, `p-6`... 禁止 `p-[17px]`)。
3. **组件标准化：**
    - 如果用户请求“所有输入框都像 X”：
        - 将 X 的样式隔离为类或组件 (`.input-standard`)。
        - 将 `.input-standard` 应用于代码库中的**所有** `<input>` 元素。
4. **移除内联样式：**
    - 将 `style={{ ... }}` 移动到 CSS 类。

---

## 4. 视觉审计

**动作：**
验证外观和感觉。

**步骤：**

1. **间距审计：**
    - 检查对齐问题。
2. **移动端响应式：**
    - 调用 `移动端设计规范` 检查。
3. **主题检查：**
    - 验证深色/浅色模式切换是否适用于新 Token。
4. **图标一致性：**
    - 调用 `图标精调` 确保描边宽度/风格匹配。

---

## 使用示例

```bash
/polish enforce glassmorphism on all cards
/polish normalize all buttons to Primary Button style
/polish purge hardcoded colors
/polish fix inconsistent spacing
```

**发生什么：**

1. 扫描硬编码的“污垢”。
2. 用户选择“完美”的组件。
3. 系统提取其 DNA (Token)。
4. 系统用该 DNA 覆盖所有类似的组件。
5. 结果：100% 一致的 UI。
