---
name: GitHub文档下载器
description: 从GitHub仓库批量下载官方文档（仅MD文件），支持Sparse Checkout优化，自动过滤非文档文件。
---

# GitHub 文档下载器

> 自动从 GitHub 仓库下载官方文档目录，过滤只保留 Markdown 文件。

---

## 🎯 使用场景

- 下载开源项目的官方文档（如 OpenClaw、Next.js、Prisma 等）
- 为 AI 学习准备本地文档库
- 生成结构化 Skill 的第一步

---

## 🚀 快速使用

### 方式一：PowerShell 脚本（推荐）

```powershell
# 下载到指定目录
.\scripts\fetch_docs.ps1 -Repo "openclaw/openclaw" -DocsPath "docs" -OutputDir "C:\temp\openclaw-docs"
```

### 方式二：手动命令

```powershell
# 1. Sparse Checkout 只下载 docs 目录
git clone --filter=blob:none --sparse https://github.com/openclaw/openclaw.git
cd openclaw
git sparse-checkout set docs

# 2. 过滤非 MD 文件
Get-ChildItem docs -Recurse -File | 
    Where-Object { $_.Extension -notin @('.md', '.mdx') } | 
    Remove-Item -Force

# 3. 删除空目录
Get-ChildItem docs -Recurse -Directory | 
    Where-Object { (Get-ChildItem $_.FullName).Count -eq 0 } | 
    Remove-Item -Force -Recurse
```

---

## 📂 输出结构

```
<OutputDir>/
├── index.md
├── cli/
│   ├── setup.md
│   ├── onboard.md
│   └── ...
├── gateway/
│   ├── configuration.md
│   └── ...
└── ...
```

---

## ⚙️ 参数说明

| 参数 | 说明 | 示例 |
|:---|:---|:---|
| `-Repo` | GitHub 仓库（owner/repo） | `openclaw/openclaw` |
| `-DocsPath` | 仓库中的文档目录 | `docs` |
| `-OutputDir` | 本地输出目录 | `C:\temp\docs` |
| `-KeepGit` | 是否保留 .git 目录 | `$false`（默认删除） |

---

## 🔧 后续操作

下载完成后，可以：

1. **手动阅读**：直接查看 MD 文件
2. **AI 汇总**：让 AI 分析生成结构化 Skill
3. **定期更新**：重新运行脚本拉取最新文档
