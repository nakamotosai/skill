---
name: Favicon获取逻辑
description: 网站图标（Favicon）抓取策略 - 处理RSS新闻源等场景的图标获取与缓存
---

# Favicon 抓取策略

## 适用场景

- RSS新闻聚合显示来源图标
- 网站列表展示favicon
- 任何需要动态获取第三方网站图标的场景

## 核心策略

### 1. 图标获取方式

**推荐使用 Google Favicon 服务**（无CORS限制）：

```
https://www.google.com/s2/favicons?domain={domain}&sz=128
```

**直接作为`<img src>`使用**，不要用`fetch`（会触发CORS）：

```tsx
<img 
  src={`https://www.google.com/s2/favicons?domain=${domain}&sz=128`}
  referrerPolicy="no-referrer"
/>
```

### 2. 域名映射表（MEDIA_MAP）

为确保一致性，建立**来源名称→域名**的映射：

```typescript
const MEDIA_MAP: Record<string, string> = {
  'reuters': 'reuters.com',
  'ロイター': 'reuters.com',
  '日本経済新聞': 'nikkei.com',
  'yahoo': 'yahoo.co.jp',
  // ... 按需扩展
};
```

**优先级**：

1. MEDIA_MAP关键词匹配
2. 从sourceUrl提取hostname
3. 从文章link提取hostname
4. 硬编码fallback

### 3. 本地缓存策略

记录成功加载的domain到localStorage：

```typescript
const saveDomainToCache = (domain: string) => {
  const cache = JSON.parse(localStorage.getItem('domain_cache') || '{}');
  cache[domain] = true;
  localStorage.setItem('domain_cache', JSON.stringify(cache));
};
```

**注意**：由于CORS限制无法将图片转为base64缓存，只能缓存"哪些domain可用"。

### 4. React最佳实践

**避免使用index作为key**：

```tsx
// ❌ 错误
{items.map((item, index) => <Item key={index} />)}

// ✅ 正确
{items.map(item => <Item key={item.id} />)}
```

**处理无限滚动**：复制列表时使用组合key：

```tsx
{[...items, ...items].map((item, idx) => (
  <Item key={`${item.id}-${idx}`} />
))}
```

### 5. Fallback UI

图标加载失败时显示文字缩写：

```tsx
<img 
  onError={(e) => {
    e.target.style.display = 'none';
    fallbackEl.style.display = 'flex';
  }}
/>
<div className="fallback">{source.substring(0, 4)}</div>
```

## 常见日本新闻源映射

| 来源名 | 域名 |
|--------|------|
| Yahoo!ニュース | yahoo.co.jp |
| 日本経済新聞 | nikkei.com |
| 朝日新聞 | asahi.com |
| 読売新聞 | yomiuri.co.jp |
| 毎日新聞 | mainichi.jp |
| NHK | nhk.or.jp |
| Reuters/ロイター | reuters.com |
| tenki.jp | tenki.jp |
| TBS NEWS | tbs.co.jp |
| Bloomberg | bloomberg.co.jp |
