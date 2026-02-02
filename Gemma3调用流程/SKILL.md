---
name: gemma3调用流程
description: 谷歌 Gemma 3 模型调用流程 (基于 Next.js Edge Runtime 验证)
---

# Gemma 3 调用流程与最佳实践

本 Skill 基于 `src/lib/gemini.ts` 和 `src/app/api/analyze/route.ts` 的生产环境验证经验，总结了在 Next.js Edge Runtime 环境下调用 Google Gemma 3 27B 模型的标准流程。

## 1. 依赖安装

使用官方 Google Generative AI SDK：

```bash
npm install @google/generative-ai
```

## 2. 客户端初始化 (Singleton 模式)

为了在 Serverless/Edge 环境中保持连接复用并避免重复初始化，建议使用单例模式导出 Model 实例。

**文件路径建议**: `src/lib/gemini.ts`

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";

// 优先使用环境变量，支持本地开发回退（注意：生产环境务必使用环境变量）
const API_KEY = process.env.GOOGLE_API_KEY || ""; 

const genAI = new GoogleGenerativeAI(API_KEY);

console.log("[Gemini] Initializing Google Generative AI with model: gemma-3-27b-it");

// 导出配置好的模型实例
export const gemmaModel = genAI.getGenerativeModel({
    model: "gemma-3-27b-it", // 明确指定 27B Instruct 版本
    generationConfig: {
        temperature: 0.6,    // 0.6 平衡了创造性与准确性
        maxOutputTokens: 8192, // Gemma 3 27B 支持最高 8192 tokens
    }
});
```

## 3. Edge Runtime API 路由实现

在 Next.js App Router 中，API Route 需要特别配置以支持流式传输或长时间运行（虽然本例非流式，但 Edge Runtime 更适合高并发 IO）。

**文件路径建议**: `src/app/api/analyze/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { gemmaModel } from '@/lib/gemini';

// 🚨 关键配置：指定 Edge Runtime
export const runtime = 'edge';

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { title, content } = body;

        // 构建提示词 (详见下文 Prompt Engineering)
        const prompt = buildPrompt(title, content);

        // 调用生成 API
        const result = await gemmaModel.generateContent(prompt);
        const text = result.response.text();

        // 结果清理与解析
        const cleanedJson = text.replace(/```json\s*|\s*```/g, "");
        const data = JSON.parse(cleanedJson);

        return NextResponse.json({
            source: "gemma-3",
            data: data
        });

    } catch (error: any) {
        console.error("[Gemini] Error:", error);
        return NextResponse.json(
            { error: error.message || 'Analysis failed' }, 
            { status: 500 }
        );
    }
}
```

## 4. Prompt Engineering (提示词工程)

基于生产环境验证，以下策略能显著提高输出质量和格式遵循度：

### 4.1 语言强制锁定

在 Prompt 开头明确指定输出语言，防止模型中途切换到训练语料较多的英语或日语。

```text
【语言强制锁定】
**警告：本任务的唯一输出语言为简体中文（Simplified Chinese）。**
**禁止**在输出结果中包含任何日文句子。如果包含日文，任务视为失败。
```

### 4.2 JSON 格式强制与鲁棒解析

不要依赖模型的 JSON 模式（有时不稳定），而是明确要求返回纯 JSON 字符串，并在后处理时进行正则清洗。

**Prompt 指令**:

```text
【输出格式 (JSON)】
请直接返回 JSON 对象，不要包含 Markdown 格式标记（如 ```json）：
{
  "title": "...",
  "summary": "..."
}
```

**代码清洗**:

```typescript
const text = result.response.text();
// 移除 Markdown 代码块标记，防止 JSON.parse 失败
const jsonStr = text.replace(/```json\s*|\s*```/g, "");
return JSON.parse(jsonStr);
```

### 4.3 上下文注入 (Context Injection)

为了提高准确性，建议将搜索结果或“世界基准”事实注入 Prompt。

```typescript
const prompt = `
【世界基准 (World Baseline)】
${worldBaselineFacts}

【背景信息】
${searchResults}

【任务内容】
...
`;
```

## 5. 错误处理与重试

1. **Safety Filters**: 默认的安全过滤器可能会误杀新闻内容。如果遇到频繁的 `FinishReason.SAFETY`，需要调整 `safetySettings`。
2. **JSON 解析失败**: 即使有 Prompt 约束，模型偶尔也会输出非 JSON 内容。建议包裹 `JSON.parse` 在 `try-catch` 块中，并在失败时将原始文本作为 fallback 返回或记录日志。
3. **超时控制**: 在 Edge 环境中，虽然没有 Lambda 的冷启动，但通过 `AbortSignal.timeout` 控制上游请求（如抓取或搜索）的耗时非常重要，以免拖累整体响应时间。

## 6. 调试技巧

- **日志**: 在 Edge Runtime 中，`console.log` 是最直接的调试手段。记录 `prompt` 的简略版本和完整的 `error` 对象。
- **回退机制 (Fallback)**: 生产代码中展示了当 Gemini 失败时，可以尝试回退到本地模型或其他 API（但在纯 Cloudflare 环境通常只能回退到错误提示）。
