---
description: 规划并实现 UI
---

# UI/UX Pro Max - 设计智能

可搜索的数据库，包含 UI 风格、调色板、字体搭配、图表类型、产品推荐、UX 指南和特定技术栈的最佳实践。

## 前置条件

检查 Python 是否已安装：

```bash
python3 --version || python --version
```

如果未安装 Python，请根据用户的操作系统进行安装：

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## 如何使用此工作流

当用户请求 UI/UX 工作（设计、构建、创建、实现、审查、修复、改进）时，请遵循此工作流：

### 步骤 1: 分析用户需求

从用户请求中提取关键信息：
- **产品类型**: SaaS, 电子商务, 作品集, 仪表盘, 落地页等
- **风格关键词**: 极简, 俏皮, 专业, 优雅, 深色模式等
- **行业**: 医疗, 金融科技, 游戏, 教育等
- **技术栈**: React, Vue, Next.js, 或默认为 `html-tailwind`

### 步骤 2: 搜索相关领域

多次使用 `search.py` 收集全面信息。搜索直到你有足够的上下文。

```bash
python3 .shared/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**推荐搜索顺序：**

1. **Product** - 获取产品类型的风格推荐
2. **Style** - 获取详细风格指南（颜色、效果、框架）
3. **Typography** - 获取带有 Google Fonts 导入的字体搭配
4. **Color** - 获取调色板（主色、辅助色、CTA、背景、文本、边框）
5. **Landing** - 获取页面结构（如果是落地页）
6. **Chart** - 获取图表推荐（如果是仪表盘/分析）
7. **UX** - 获取最佳实践和反模式
8. **Stack** - 获取特定技术栈的指南（默认：html-tailwind）

### 步骤 3: 技术栈指南 (默认: html-tailwind)

如果用户未指定技术栈，**默认为 `html-tailwind`**。

```bash
python3 .shared/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

可用技术栈: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`

---

## 搜索参考

### 可用领域

| 领域 | 用途 | 关键词示例 |
|--------|---------|------------------|
| `product` | 产品类型推荐 | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style` | UI 风格, 颜色, 效果 | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | 字体搭配, Google Fonts | elegant, playful, professional, modern |
| `color` | 按产品类型的调色板 | saas, ecommerce, healthcare, beauty, fintech, service |
| `landing` | 页面结构, CTA 策略 | hero, hero-centric, testimonial, pricing, social-proof |
| `chart` | 图表类型, 库推荐 | trend, comparison, timeline, funnel, pie |
| `ux` | 最佳实践, 反模式 | animation, accessibility, z-index, loading |
| `prompt` | AI 提示词, CSS 关键词 | (style name) |

### 可用技术栈

| 技术栈 | 重点 |
|-------|-------|
| `html-tailwind` | Tailwind 工具类, 响应式, 无障碍 (默认) |
| `react` | 状态, hooks, 性能, 模式 |
| `nextjs` | SSR, 路由, 图片, API 路由 |
| `vue` | 组合式 API, Pinia, Vue Router |
| `svelte` | Runes, stores, SvelteKit |
| `swiftui` | 视图, 状态, 导航, 动画 |
| `react-native` | 组件, 导航, 列表 |
| `flutter` | Widgets, 状态, 布局, 主题 |
| `shadcn` | shadcn/ui 组件, 主题, 表单, 模式 |

---

## 示例工作流

**用户请求：** "Làm landing page cho dịch vụ chăm sóc da chuyên nghiệp" (做一个专业护肤服务的落地页)

**AI 应当：**

```bash
# 1. Search product type
python3 .shared/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --domain product

# 2. Search style (based on industry: beauty, elegant)
python3 .shared/ui-ux-pro-max/scripts/search.py "elegant minimal soft" --domain style

# 3. Search typography
python3 .shared/ui-ux-pro-max/scripts/search.py "elegant luxury" --domain typography

# 4. Search color palette
python3 .shared/ui-ux-pro-max/scripts/search.py "beauty spa wellness" --domain color

# 5. Search landing page structure
python3 .shared/ui-ux-pro-max/scripts/search.py "hero-centric social-proof" --domain landing

# 6. Search UX guidelines
python3 .shared/ui-ux-pro-max/scripts/search.py "animation" --domain ux
python3 .shared/ui-ux-pro-max/scripts/search.py "accessibility" --domain ux

# 7. Search stack guidelines (default: html-tailwind)
python3 .shared/ui-ux-pro-max/scripts/search.py "layout responsive" --stack html-tailwind
```

**然后：** 综合所有搜索结果并实现设计。

---

## 获得更好结果的提示

1. **关键词要具体** - "healthcare SaaS dashboard" > "app"
2. **多次搜索** - 不同的关键词揭示不同的见解
3. **组合领域** - Style + Typography + Color = 完整的设计系统
4. **总是检查 UX** - 搜索 "animation", "z-index", "accessibility" 以查找常见问题
5. **使用 stack 标志** - 获取特定实现的最佳实践
6. **迭代** - 如果第一次搜索不匹配，尝试不同的关键词
7. **拆分为多个文件** - 为了更好的可维护性：
   - 将组件分离到单独的文件中 (例如 `Header.tsx`, `Footer.tsx`)
   - 提取可重用的样式到专用文件
   - 保持每个文件专注且在 200-300 行以内

---

## 专业 UI 的通用规则

这些是经常被忽视的问题，会导致 UI 看起来不专业：

### 图标与视觉元素

| 规则 | Do | Don't |
|------|----|----- |
| **无 Emoji 图标** | 使用 SVG 图标 (Heroicons, Lucide, Simple Icons) | 使用 🎨 🚀 ⚙️ 等 Emoji 作为 UI 图标 |
| **稳定的悬停状态** | 悬停时使用颜色/透明度过渡 | 使用会改变布局的缩放变换 |
| **正确的品牌 Logo** | 搜索 Simple Icons 的官方 SVG | 猜测或使用不正确的 Logo 路径 |
| **一致的图标尺寸** | 使用固定的 viewBox (24x24) 和 w-6 h-6 | 随意混合不同大小的图标 |

### 交互与光标

| 规则 | Do | Don't |
|------|----|----- |
| **指针光标** | 给所有可点击/可悬停的卡片添加 `cursor-pointer` | 交互元素保留默认光标 |
| **悬停反馈** | 提供视觉反馈 (颜色, 阴影, 边框) | 没有元素可交互的指示 |
| **平滑过渡** | 使用 `transition-colors duration-200` | 状态瞬间变化或太慢 (>500ms) |

### 浅色/深色模式对比度

| 规则 | Do | Don't |
|------|----|----- |
| **浅色模式玻璃卡片** | 使用 `bg-white/80` 或更高不透明度 | 使用 `bg-white/10` (太透明) |
| **浅色模式文本对比度** | 文本使用 `#0F172A` (slate-900) | 正文文本使用 `#94A3B8` (slate-400) |
| **浅色模式柔和文本** | 最低使用 `#475569` (slate-600) | 使用 gray-400 或更浅 |
| **边框可见性** | 浅色模式使用 `border-gray-200` | 使用 `border-white/10` (不可见) |

### 布局与间距

| 规则 | Do | Don't |
|------|----|----- |
| **悬浮导航栏** | 添加 `top-4 left-4 right-4` 间距 | 将导航栏贴在 `top-0 left-0 right-0` |
| **内容内边距** | 考虑到固定导航栏的高度 | 让内容隐藏在固定元素后面 |
| **一致的最大宽度** | 使用相同的 `max-w-6xl` 或 `max-w-7xl` | 混合不同的容器宽度 |

---

## 交付前检查清单

在交付 UI 代码之前，验证这些项目：

### 视觉质量
- [ ] 不使用 Emoji 作为图标 (使用 SVG 代替)
- [ ] 所有图标来自一致的图标集 (Heroicons/Lucide)
- [ ] 品牌 Logo 正确 (从 Simple Icons 验证)
- [ ] 悬停状态不会引起布局偏移

### 交互
- [ ] 所有可点击元素都有 `cursor-pointer`
- [ ] 悬停状态提供清晰的视觉反馈
- [ ] 过渡平滑 (150-300ms)
- [ ] 焦点状态对键盘导航可见

### 浅色/深色模式
- [ ] 浅色模式文本有足够的对比度 (最低 4.5:1)
- [ ] 玻璃/透明元素在浅色模式下可见
- [ ] 边框在两种模式下均可见
- [ ] 交付前测试两种模式

### 布局
- [ ] 悬浮元素与边缘有适当的间距
- [ ] 没有内容隐藏在固定导航栏后面
- [ ] 在 320px, 768px, 1024px, 1440px 响应式正常
- [ ] 移动端无水平滚动

### 无障碍性 (Accessibility)
- [ ] 所有图片都有 alt 文本
- [ ] 表单输入框有 label
- [ ] 颜色不是唯一的指示器
- [ ] 尊重 `prefers-reduced-motion`
