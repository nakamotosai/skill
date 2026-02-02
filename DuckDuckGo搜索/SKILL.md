---
name: ddgs网络搜索
description: 基于 Edge Runtime 兼容的 DuckDuckGo HTML 网页搜索实现
---

# DDGS 网络搜索 (Edge Runtime 兼容版)

本 Skill 提供了在 Next.js Edge Runtime (如 Cloudflare Pages) 环境下，通过直接抓取 DuckDuckGo HTML 版作为免费、免 Key 搜索源的完整实现方案。

## 1. 核心原理

由于 Cloudflare Workers/Pages 不支持 Node.js 原生模块（如 `http`、`net` 甚至 `duckduckgo-search` Python 库的很多 JS 移植版），最可靠的方法是使用 Web 标准的 `fetch` API 直接访问 `https://html.duckduckgo.com/html/`。

**优势**:

- **零依赖**: 仅需 `cheerio` 解析 HTML。
- **Edge 兼容**: 完全基于 Web API。
- **隐私**: 无需 API Key，完全匿名。

## 2. 依赖安装

```bash
npm install cheerio
```

## 3. 完整实现代码

建议保存为 `src/lib/ddgs.ts` 或在 API Route 中直接使用。

```typescript
import * as cheerio from 'cheerio';

export interface DDGSearchResult {
    title: string;
    url: string;
    description: string;
}

/**
 * Edge 兼容的 DDGS 搜索函数 (增强版: 重试 + 随机 UA)
 * @param query 搜索关键词
 * @param locale 地区代码 (默认: ja-jp, 可选: cn-zh, en-us 等)
 */
export async function ddgsSearch(query: string, locale: string = 'ja-jp'): Promise<DDGSearchResult[]> {
    const userAgents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    ];

    const maxRetries = 3;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            // DuckDuckGo HTML 搜索（Edge 兼容）
            // 参数: q=查询, kl=地区, df=时间范围(w=week, m=month, d=day)
            const encodedQuery = encodeURIComponent(query);
            const searchUrl = `https://html.duckduckgo.com/html/?q=${encodedQuery}&kl=${locale}`;
            
            const randomUA = userAgents[Math.floor(Math.random() * userAgents.length)];

            if (attempt > 0) {
                // 简单的避开速率限制延时
                await new Promise<void>(r => setTimeout(r, 1000 * attempt));
            }

            const response = await fetch(searchUrl, {
                headers: {
                    'User-Agent': randomUA,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': locale + ',en-US;q=0.8,en;q=0.7',
                    'Cache-Control': 'no-cache',
                    'Referer': 'https://html.duckduckgo.com/'
                },
                // 建议设置较短的超时，快速失败重试
                signal: AbortSignal.timeout(8000)
            });

            if (response.status === 403 || response.status === 429) {
                console.warn(`[DDGS] Rate limit (${response.status}) on attempt ${attempt + 1}`);
                continue;
            }

            if (!response.ok) continue;

            const html = await response.text();

            // 反爬虫验证页面检查
            if (html.includes("If this error persists, please let us know") || html.includes("Rate limit")) {
                console.warn(`[DDGS] Soft block detected on attempt ${attempt + 1}`);
                continue;
            }

            const $ = cheerio.load(html);
            const results: DDGSearchResult[] = [];

            // 解析 HTML 结果
            $('.result').each((i, elem) => {
                if (i >= 6) return false; // 限制返回数量

                const $result = $(elem);
                const $link = $result.find('.result__a');
                const title = $link.text().trim();
                let url = $link.attr('href') || '';
                const description = $result.find('.result__snippet').text().trim();

                // DDG 重定向链接解码
                if (url.startsWith('//duckduckgo.com/l/?')) {
                    const match = url.match(/uddg=([^&]+)/);
                    if (match) url = decodeURIComponent(match[1]);
                }

                // 过滤广告链接
                if (url.includes("duckduckgo.com/y.js") || url.includes("ad_provider")) {
                    return;
                }

                if (title && url) {
                    results.push({ title, url, description });
                }
            });

            if (results.length > 0) {
                return results;
            }
            
        } catch (e) {
            console.warn(`[DDGS] Attempt ${attempt + 1} failed:`, e);
        }
    }

    return [];
}
```

## 4. 最佳实践

1. **容错处理**: DDG 的 HTML 端点相比 API 更容易触发 403 或验证码。一定要在代码层面实现 `try-catch` 和重试循环。
2. **地区设置 (`kl`)**: 准确设置 `kl` 参数（如 `cn-zh`, `jp-jp`, `us-en`）能显著提高搜索结果的相关性。
3. **结果清洗**: 返回的 description 往往是截断的 snippet，如果需要详细内容，需要配合页面抓取（Scraping）工具再次访问目标 URL。
4. **广告过滤**: HTML 结果中混杂着 class 为 `.result` 的广告条目，通常链接包含 `/y.js` 或 `ad_provider`，务必过滤。
