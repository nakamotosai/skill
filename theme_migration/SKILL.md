---
name: Web 应用主题替换与重构清单 (Web App Theme Replacement Checklist)
description: 提供一套通用的结构化检查清单，用于在更换应用主题时快速识别并修改所有受影响的设计维度。
---

# Web 应用主题替换与重构清单 (Theme Replacement Framework)

本经验指南定义了当需要将应用界面整体迁移至**任一新主题**时，必须审查并修改的核心区域。它不局限于特定颜色，而是一套确保主题一致性的工作流。

## 1. 全局设计配置 (Global Design Variables)

第一步应在全局样式文件（如 `globals.css`）中定义新主题的“灵魂”：

- [ ] **CSS 变量重定义 (`:root`)**: 修改背景色 (`--background`)、前景色 (`--foreground`)、主色调 (`--primary`)、边框色 (`--border`) 等基础变量。
- [ ] **全局文本基色**: 确保 `body` 的默认文字颜色符合新主题的明度与色调。
- [ ] **全局背景渐变**: 如果有背景层设计，需更新 `linear-gradient` 或 `background-image`。

## 2. 文本与语义化色彩 (Typography & Semantic Colors)

文本颜色的不统一是导致主题视觉“显脏”的主因：

- [ ] **正文与标题**: 检查 `text-slate-*`, `text-gray-*` 等类，替换为新主题的阶梯文本色（通常分为两级：Primary Text 和 Secondary/Muted Text）。
- [ ] **占位符颜色**: 检查所有输入框的 `placeholder:text-*`，确保其在淡色/深色背景下的对比度。
- [ ] **语义化状态**: 更新“成功、警告、错误”色彩，使其饱和度与新主色调匹配。

## 3. 组件级细节 (Component Aesthetics)

在切换主题时，组件的物理属性通常也需要随之微调：

- [ ] **边框策略**: 重塑所有组件的 `border` 风格（如：从深色细边框变为浅色粗边框，或改为仅有阴影无边框）。
- [ ] **圆角体系 (`rounded`)**: 确立新主题的亲和力基调（全圆角 `rounded-full` 代表柔和，小圆角 `rounded-lg` 代表专业）。
- [ ] **交互反馈 (Interaction Styles)**:
  - [ ] **Hover 状态**: 全面更新按钮、卡片、输入框的鼠标悬停颜色，严禁残留旧主题的基色。
  - [ ] **Active/Selected 状态**: 确保选中态的高亮色具有明显的视觉区分度。

## 4. 浮层与深度感 (Modals & Elevation)

- [ ] **遮罩层 (Overlays)**: 修改弹窗遮罩背景色及模糊度 (`backdrop-blur`)。
- [ ] **阴影效果 (`shadow`)**: 更新 `box-shadow` 的颜色。高质量主题通常使用**带色调的阴影**（如橙色主题使用淡橙色阴影而非纯灰色）。
- [ ] **面板背景**: 针对卡片、弹窗的 `bg-white/90` 或 `bg-slate-50` 进行替换。

## 5. 组件特定资产 (Assets & Micro-Details)

- [ ] **图标集 (Icons)**: 检查 `lucide-react` 等图标的 `text-*` 颜色。图标通常需要比普通文字更亮或更符合强调色。
- [ ] **加载动画 (Spinners/Loaders)**: 统一 `animate-spin` 元素的边框或 SVG 填充色。
- [ ] **上传/拖拽状态**: 修改文件上传组件在不同状态下的边框虚线颜色和背景。

## 6. 系统级细节平衡 (System-level Polish)

- [ ] **美化滚动条 (Scrollbar Styling)**: 滚动条的 `thumb` 颜色必须适配新主题的强调色，并采用不占位的悬浮模式 (`overflow-y: overlay`)。
- [ ] **选中文字背景 (`selection`)**: 修改页面文本被用户选中时的高亮色。

## 7. 布局稳定性验证

- [ ] **切换抖动检查**: 验证不同页面内容长度变化或标签切换时，布局中心点是否因为滚动条或布局计算而发生位移。

---
**核心原则：全面覆盖 & 拒绝残留。** 看到任何一处的颜色与新主题格格不入时，即刻溯源其属于上述哪个清单项。
