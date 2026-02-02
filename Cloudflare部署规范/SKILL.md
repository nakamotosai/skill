# Cloudflare Pages 部署：全栈架构技术准则

本指南旨在通过严格的工程化手段，彻底解决 Next.js 15+ 在 Cloudflare Pages 部署中出现的“依赖冲突”、“运行时错误”及“锁文件不一致”问题。

## 1. 核心版本管理：严格锁定原则

### 🔴 严禁使用版本模糊符 (^)

在 `package.json` 中，核心依赖**严禁**使用 `^` 或 `~` 等前缀。Cloudflare 的构建适配器对版本兼容性有极高的敏感度。

* **强制标准**: 必须直接声明确切的版本号（例如 `"next": "15.5.2"`）。
* **推荐基准配置**:
  * `Next.js`: `15.5.2` (当前 Cloudflare 适配器的稳定上限)
  * `React`: `19.0.0`
  * `ESLint`: `9.17.0`
  * `@cloudflare/next-on-pages`: `1.13.16`

### 🟢 显式声明构建依赖

必须在 `devDependencies` 中显式包含 `wrangler` 和 `vercel`。这能确保构建服务器在执行 `npm ci` 时，能从当前项目的锁文件中获取确定的二进制依赖，避免其隐式环境引发冲突。

## 2. 边缘运行时 (Edge Runtime) 兼容性

### ⚙️ 模块别名强制映射

Cloudflare 无法直接解析不带 `node:` 前缀的内置模块。必须在 `next.config.js` 中配置 Webpack 强制重定向：

```javascript
webpack: (config, { webpack, isServer }) => {
    if (isServer) {
        // 将旧式引用强制映射到边缘运行时支持的新引用
        config.resolve.alias['async_hooks'] = 'node:async_hooks';
        config.resolve.alias['fs'] = 'node:fs';
    }
    return config;
}
```

### 🧬 Next.js 15 异步参数适配

在 Next.js 15 架构下，API 路由的 `params` 已变为 `Promise` 类型。

* **强制要求**: 必须使用 `await params` 来解构参数，否则部署后将出现运行时变量未定义的致命错误。

## 3. 部署准备流程：物理协同机制

当遇到 `EUSAGE` (锁文件不同步) 或 `ERESOLVE` (依赖冲突) 错误时，严禁只修改 `package.json` 文本。必须执行物理级别的重置流程：

1. **物理清除**: 彻底删除本地项目中的 `node_modules` 文件夹及 `package-lock.json` 文件。
2. **强制策略**: 在项目根目录建立 `.npmrc` 文件，声明 `legacy-peer-deps=true`。
3. **重新生成**: 执行 `npm install --legacy-peer-deps` 重新构建依赖树，强制生成具备最高一致性的锁文件。
4. **云端推送**: 将更新后的 lock 文件推送至 GitHub，触发 Cloudflare 的 `npm ci` 流程。

## 4. 故障排除参考表

| 报错关键字 | 根本原因 | 修复动作 |
| :--- | :--- | :--- |
| `Could not resolve "async_hooks"` | 构建器无法识别 Node.js 原生模块 | 在 `next.config.js` 中添加 `node:` 前缀重定向 |
| `npm error ERESOLVE` | 多库之间的 Peer Dependency 冲突 | 将所有核心库对齐到本指南第 1 节的固定版本 |
| `npm error EUSAGE` | 锁文件与 package.json 指纹不匹配 | 执行上述“部署准备流程”中的物理清除与重新安装 |
| `params.xxx is undefined` | Next.js 15 的异步参数兼容性失效 | 在 API 代码中补全 `await params` 逻辑 |

## 5. 云端环境配置红线

部署成功后，必须在 Cloudflare 管理后台验证：

* **兼容性标志 (Compatibility Flags)**: 确认已启用 `nodejs_compat`。
* **绑定关联 (Bindings)**: 确认 R2 Bucket（或 KV）已通过后台界面正确手动关联至 Pages 项目。
