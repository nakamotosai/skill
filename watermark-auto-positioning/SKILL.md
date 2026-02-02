---
name: watermark-auto-positioning
description: 基于多模态 AI (Gemma 3) 的智能珠宝水印定位与避让系统开发规范
---

# 水印自动定位 (Smart Watermark Positioning) Skill

本 Skill 总结了在珠宝/奢侈品电商场景下，如何利用多模态模型实现水印的"智能位置推荐"与"边缘保护"功能。

## 1. 核心架构：AI 直接推荐水印位置

不同于传统的"检测珠宝边界框 → 计算水印位置"两步法，本方案采用**单步直出**策略：

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   上传图片   │ ──► │ AI 分析空旷   │ ──► │ 直接输出     │
│              │     │ 区域并推荐   │     │ {x, y} 坐标  │
└──────────────┘     └──────────────┘     └──────────────┘
```

**优势**：

- AI 综合考虑珠宝位置、背景复杂度、图片布局
- 避免边界框检测不准导致的位置偏移
- 实现逻辑更简单，不需要复杂的空间计算

## 2. 提示词工程 (Prompt Engineering)

```text
You are a professional image layout AI for jewelry e-commerce.

## YOUR TASK

Analyze this jewelry image and recommend the BEST position to place a watermark text.

### WATERMARK PLACEMENT RULES:

1. **FIND EMPTY SPACE**: Look for areas in the image that are:
   - Empty, plain, or have uniform background (skin, clothing, wall, etc.)
   - Close to the jewelry but NOT overlapping it
   - Preferably below or beside the jewelry

2. **AVOID THESE AREAS**:
   ❌ Do not place watermark directly on the jewelry
   ❌ Do not place too close to image edges (keep 10% margin)
   ❌ Avoid busy or cluttered backgrounds

3. **PRIORITY ORDER** for watermark placement:
   - 1st: Below the jewelry (if there's empty space)
   - 2nd: To the left or right of jewelry (on empty areas)
   - 3rd: Above the jewelry (if other options unavailable)

### OUTPUT FORMAT (JSON only):
{
  "watermark_position": { "x": number, "y": number },  // 0-1000 scale
  "description": "15 words summary",
  "copy": { ... }
}
```

## 3. 坐标归一化 (Coordinate Normalization)

AI 可能返回多种坐标格式，代码层需要统一处理：

```typescript
if (result.watermark_position) {
  const { x, y } = result.watermark_position;
  const maxVal = Math.max(x, y);
  
  if (maxVal > 100) {
    // 0-1000 范围 → 除以 10
    result.watermark_position.x /= 10;
    result.watermark_position.y /= 10;
  } else if (maxVal <= 1.01 && maxVal > 0) {
    // 0-1 范围 → 乘以 100
    result.watermark_position.x *= 100;
    result.watermark_position.y *= 100;
  }
}
```

## 4. 边缘裁切保护 (Edge Protection)

当 AI 推荐的位置可能导致水印被裁切时，自动向内平移：

```typescript
// 估算水印尺寸
const textWidth = watermarkText.length * fontSize * 0.6;
const textHeight = fontSize * 1.2;
const margin = width * 0.02; // 2% 边距

// 水平方向保护
const minX = textWidth / 2 + margin;
const maxX = width - textWidth / 2 - margin;
targetX = Math.max(minX, Math.min(maxX, targetX));

// 垂直方向保护
const minY = textHeight + margin;
const maxY = height - margin;
targetY = Math.max(minY, Math.min(maxY, targetY));
```

## 5. 日志输出格式

```
🎯 AI 推荐水印位置: X=xxx, Y=yyy
📏 水印位置归一化: 0-1000 -> 0-100
📍 AI 推荐位置 (百分比): X=xx.x%, Y=yy.y%
⚠️ 水印左侧/右侧可能裁切，向xxx平移
🎯 最终水印位置: X=xxx, Y=xxx
📏 图片尺寸: 1080x1080px
```

## 6. 关键文件

| 文件 | 职责 |
|-----|------|
| `src/lib/gemini.ts` | AI 调用 + 提示词 + 坐标归一化 |
| `src/lib/watermark.ts` | SVG 渲染 + 边缘保护 + 位置计算 |
| `src/app/api/enhance/route.ts` | 流程控制 + 参数传递 |

## 7. 调试技巧

如需调试，可在 `watermark.ts` 中临时添加调试层：

```typescript
const debugBox = `
  <circle cx="${finalPosX}" cy="${finalPosY}" r="12" fill="#00FFFF" stroke="#000000" stroke-width="3"/>
  <text x="${finalPosX + 20}" y="${finalPosY + 5}" fill="#00FFFF" font-size="20">AI Position</text>
`;
```

> **经验总结**：如果水印位置偏离预期，先检查日志中的坐标归一化步骤是否正确执行。
