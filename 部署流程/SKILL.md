---
description: 生产环境发布部署指令。包含预检和部署执行。
---

# /deploy - 生产环境部署

$ARGUMENTS

---

## 目的

此指令处理生产环境部署，包括预检、部署执行和验证。

---

## 子指令

```
/deploy            - 交互式部署向导
/deploy check      - 仅运行部署前检查
/deploy preview    - 部署到预览/暂存环境
/deploy production - 部署到生产环境
/deploy rollback   - 回滚到上一个版本
```

---

## 部署前检查清单

任何部署之前：

```markdown
## 🚀 部署前检查清单

### 代码质量
- [ ] 无 TypeScript 错误 (`npx tsc --noEmit`)
- [ ] ESLint 通过 (`npx eslint .`)
- [ ] 所有测试通过 (`npm test`)

### 安全性
- [ ] 无硬编码密钥
- [ ] 环境变量已记录文档
- [ ] 依赖项已审计 (`npm audit`)

### 性能
- [ ] 包大小可接受
- [ ] 无 console.log 语句
- [ ] 图片已优化

### 文档
- [ ] README 已更新
- [ ] CHANGELOG 已更新
- [ ] API 文档是最新的

### 准备好部署了吗？(y/n)
```

---

## 部署流程

```
┌─────────────────┐
│  /deploy        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Pre-flight     │
│  checks (预检)   │
└────────┬────────┘
         │
    通过? ──No──► 修复问题
         │
        Yes
         │
         ▼
┌─────────────────┐
│  Build          │
│  application    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Deploy to      │
│  platform       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Health check   │
│  & verify       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ✅ 完成         │
└─────────────────┘
```

---

## 输出格式

### 部署成功

```markdown
## 🚀 部署完成

### 摘要
- **版本:** v1.2.3
- **环境:** production
- **耗时:** 47 seconds
- **平台:** Vercel

### URL
- 🌐 生产环境: https://app.example.com
- 📊 仪表盘: https://vercel.com/project

### 变更内容
- 添加了用户资料功能
- 修复了登录 bug
- 更新了依赖项

### 健康检查
✅ API 响应正常 (200 OK)
✅ 数据库已连接
✅ 所有服务健康
```

### 部署失败

```markdown
## ❌ 部署失败

### 错误
构建失败于步骤: TypeScript compilation

### 详情
```
error TS2345: Argument of type 'string' is not assignable...
```

### 解决方案
1. 修复 `src/services/user.ts:45` 中的 TypeScript 错误
2. 在本地运行 `npm run build` 进行验证
3. 再次尝试 `/deploy`

### 可用回滚
上一版本 (v1.2.2) 仍然有效。
如果需要，运行 `/deploy rollback`。
```

---

## 平台支持

| 平台 | 指令 | 说明 |
|----------|---------|-------|
| Vercel | `vercel --prod` | Next.js 自动检测 |
| Railway | `railway up` | 需要 Railway CLI |
| Fly.io | `fly deploy` | 需要 flyctl |
| Docker | `docker compose up -d` | 用于自托管 |

---

## 示例

```
/deploy
/deploy check
/deploy preview
/deploy production --skip-tests
/deploy rollback
```
