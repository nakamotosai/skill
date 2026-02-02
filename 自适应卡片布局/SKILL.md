---
name: 自适应卡片布局
description: 处理仪表盘等空间受限、分辨率多变场景下的自适应卡片布局标准。核心方法是“固定优先，弹性填充”。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# 自适应弹性卡片构建标准 (Adaptive Card Layout)

> **哲学：** 布局不是静态的容器，而是动态的平衡。先稳住地基，再调整核心。
> **核心原则：** 固定优先，弹性填充 (Fixed-First, Elastic-Fill)。

---

## 🎯 核心行为准则 (MANDATORY)

当用户要求由于屏幕缩放或分辨率变化导致的“自适应”布局修改时，必须遵循以下流程：

### 1. 结构化解构 (Constraint Analysis)

在动手修改任何代码前，必须将卡片内容分为两类：

- **🔴 固定层 (Fixed Elements)**：必须完整显示的、尺寸相对恒定的关键信息（如页眉日期、页脚进度条、操作按钮）。
- **🟢 弹性层 (Elastic Elements)**：视觉核心、可以根据剩余空间任意伸缩的内容（如居中的大数字、实时图表、视频预览）。

### 2. 识别与反问 (ASK BEFORE ACTING)

如果用户没有明确指出哪些内容应该被“保护”，**必须**先进行确认：
> **反问示例：** “为了确保最佳显示效果，请问您希望**固定**哪部分内容（如页眉页脚）？我会让中间的 [具体内容] 根据卡片的实际高度自动缩放。”

---

## 🔧 技术实现指南

### 1. 物理锚定 (Layout Anchor)

使用 Flex 布局结合 `shrink` 属性锁定关键空间：

- **保护固定层**：添加 `shrink-0` (Tailwind) 或 `flex-shrink: 0` (CSS)，确保系统在压缩空间时绝对不会牺牲这些部分。
- **强制页脚吸附**：使用 `mt-auto` (Tailwind) 或 `margin-top: auto` (CSS)，将页脚锚定在容器最底部。

### 2. 容器感知缩放 (Container-Aware Scaling)

放弃滥用 `vw/vh`，改用容器查询 (Container Queries) 实现真正的布局闭环：

- **定义容器**：在父卡片添加 `[container-type:size]`。
- **选择正确的自适应维度**：
  - **宽度敏感型 (Width-Sensitive)**：如果内容主要是长文字或横向排列的数字（如：时间 `09:41:59`），必须使用 **`cqw`**。这能防止内容从侧面溢出卡片。
  - **高度敏感型 (Height-Sensitive)**：如果卡片非常矮，且需要保全页眉页脚，使用 **`cqh`** 确保内容不会在垂直方向上互相重叠。
- **使用 `clamp()` 锁定范围**：`text-[clamp(min, preferred_cqw/cqh, max)]`。

### 3. 内容防抖 (Layout Stability)

当弹性层包含频繁变动的数字（如秒数、实时流量）时：

- **固定位宽与字形**：使用 `lining-nums` (等高数字) 配合 `tabular-nums`，彻底杜绝数字跳动，尤其是金融类大数字。
- **物理分栏**：将小时、分钟、秒分别放入独立的 Grid 列中，防止数字宽度的微小变动导致整张卡片内容“漂移”。

### 4. 结构解耦与不对称对齐 (Structural Decoupling)

当卡片左右两侧内容在 **行数不一致** 或 **垂直对齐逻辑冲突**（如：左侧垂直居中，右侧需贴顶贴底）时：

- **物理分栏 (Physical Columns)**：**严禁**试图在同一个 Flex 容器中通过 margin 强行对齐。必须建立左右两个独立的 `flex-col` 容器。
  - **左列**：`flex-1`，设定独立的 `justify-center`。
  - **右列**：`justify-between`，确保首尾元素分别物理贴顶和贴底，与左侧内容完全解耦。
- **括号式对称 (Bracket Symmetry)**：利用右列 `justify-between` 创造视觉上的“括号”，包裹住左侧的中心内容，形成高级的平衡感。

### 5. 极端场景舍弃 (Strategic Hiding)

在卡片极度被压缩时（如高度 < 80px），应果断通过 **Container Queries** 隐藏次要信息以保全核心：

```css
/* ⚠️ 注意：Container Query 计算的是 Content Box。如果有 p-5 (40px)，阈值需相应调低 */
@container (max-height: 60px) {
  .optional-footer {
    display: none;
  }
}
```

---

## ⚠️ 避坑检查单 (Anti-Patterns)

- [ ] **严禁禁止 `flex-1` 霸屏**：除非配合 `overflow-hidden` 且已经处理了页脚锚定，否则 `flex-1` 会无情地将其他内容推出视野。
- [ ] **不要盲目使用媒体查询 (@media)**：媒体查询感知的是“屏幕”，而卡片需要感知的是“网格容器”。优先使用 **Container Queries**。
- [ ] **保留内边距平衡**：在极端缩放时，手动通过 `clamp()` 减小 `p-` 或 `gap-`，而不是彻底消除它们，以保持视觉的高级感。

---

> **记住：** 好的自适应布局应该像呼吸一样自然。当外部压力（空间缩小）增大时，不重要的内容应该优雅地收缩，以保全关键信息的露脸权。
