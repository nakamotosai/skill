---
name: 微软语音合成
description: 实现兼容 Cloudflare Pages (Edge Runtime) 的微软 Edge TTS 功能
---

# Edge TTS Implementation Skill

此 Skill 包含在 Next.js (Edge Runtime) 环境下实现微软 Edge TTS 的完整解决方案。经验证可用于 Cloudflare Pages 部署。

## ⚠️ 关键维护说明 (CRITICAL)

**部署失败 (500 Error) 的首要原因**通常是硬编码的 `CHROMIUM_FULL_VERSION` 和 `User-Agent` 过期。微软服务器会主动拒绝旧版本客户端的连接。

- **症状**: 本地开发 (Python 库) 正常，但 Cloudflare 部署后 WebSocket 返回 500。
- **解决方案**: 定期检查并更新 `route.ts` 中的版本常量。
- **获取最新版本**: 参考 [edge-tts python 库](https://github.com/rany2/edge-tts) 的 `constants.py` 文件中的 `CHROMIUM_FULL_VERSION` 值。

## 核心架构

- **Backend (`/api/tts/edge`)**: 使用 Edge Runtime 处理 WebSocket 连接。关键在于处理 Cloudflare 的 WebSocket `upgrade` 和 `accept()` 逻辑。
- **Frontend (`EdgeTtsProvider`)**: 发送 WebSocket 协议数据（Config + SSML），接收二进制音频流并拼接播放。

## 关键文件

### 1. 后端 API (`src/app/api/tts/edge/route.ts`)

**关键点**：

- `export const runtime = 'edge';` (必须)
- **常量维护**：**务必保持与最新 Edge 浏览器版本一致**。

  ```typescript
  // 示例：2026年1月最新版
  const CHROMIUM_FULL_VERSION = '143.0.3650.75';
  ```

- **Cloudflare 特异性**：
  - 使用 `fetch` 带 `Upgrade: websocket` 头。
  - 获取 socket 后**必须立即调用 `socket.accept()`**。

```typescript
// 连接逻辑示例
async function connectToEdgeTTS(wsUrl: string): Promise<WebSocket> {
    // 1. Cloudflare Fetch Upgrade
    const fetchUrl = wsUrl.replace('wss://', 'https://');
    const connectResp = await fetch(fetchUrl, {
        headers: {
            'Upgrade': 'websocket',
            'Connection': 'Upgrade',
            // User-Agent 版本号必须与 CHROMIUM_FULL_VERSION 主版本一致
            'User-Agent': 'Mozilla/5.0 ... Chrome/143.0.0.0 ...' 
        }
    });

    if (connectResp.status === 101) {
        const socket = (connectResp as any).webSocket;
        if (socket) {
            // CRITICAL: Cloudflare requires accept()
            if (typeof socket.accept === 'function') socket.accept();
            return socket;
        }
    }
    // 2. Fallback: Standard WebSocket (Local)
    return new WebSocket(wsUrl);
}
```

### 2. 前端 Provider (`src/lib/tts/edge.ts`)

- 负责音频拼接、播放和字幕同步（WordBoundary）。

## 常见坑与解决方案

1. **500 Error / WebSocket 连接失败**：
   - **原因 1**：**User-Agent 或 Chromium 版本号过期**（最常见）。微软会屏蔽旧版。
     - **修复**：更新 `CHROMIUM_FULL_VERSION` 为最新真实 Chrome 版本。
   - **原因 2**：Cloudflare 环境未调用 `accept()`。

2. **本地可用，部署失败**：
   - **原因**：Node.js 支持标准 WebSocket，Edge Runtime 不支持。
   - **修复**：使用混合连接模式（优先 fetch upgrade，失败回退）。

3. **CORS 错误**：
   - **原因**：前端直连微软服务器被拒。
   - **修复**：必须使用后端 API 代理。
