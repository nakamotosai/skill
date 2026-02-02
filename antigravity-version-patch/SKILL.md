---
name: antigravity-version-patch
description: 专门修复 Antigravity "This version is no longer supported" 错误的应急指南。
---

# Antigravity 版本修复 Skill

当 Antigravity 报错 "This version is no longer supported" 时，通常是因为配置文件中持久化的 `userAgent` 字段过旧。本 Skill 提供了一套不依赖于官方更新的硬修补方案。

## 1. 核心原理

Google 的 Antigravity 服务会通过 `User-Agent` 和 `X-Goog-Api-Client` 头部检查客户端合法性。官方插件在更新后有时无法自动刷新本地 `.json` 账户文件中的版本字符串，导致请求被直接拦截。

## 2. 强制修复流程

### 步骤 A：彻底清理环境 (关键)

必须在修改文件前关闭所有相关进程，否则内存中的旧配置会在程序退出时覆盖你的修改。

- **Windows**: `taskkill /F /IM node.exe` / `taskkill /F /IM openclaw.exe`
- **Linux**: `sudo pkill -9 -f openclaw && sudo pkill -9 -f node`

### 步骤 B：定位并注入 JSON 配置

找到以下路径的配置文件，并将每一个 account 对象的版本号强制锁定。

- **本地路径**: `%APPDATA%\Roaming\opencode\antigravity-accounts.json`
- **服务器路径**: `~/.openclaw/agents/main/agent/auth-profiles.json`

**注入字段示例**:

```json
{
  "userAgent": "antigravity/1.15.8 linux/amd64",
  "apiClient": "google-cloud-sdk vscode/1.87.0",
  "ideType": "VSCODE",
  "platform": "LINUX",
  "pluginType": "GEMINI"
}
```

### 步骤 C：源码层伪装同步

确保 `node_modules` 中负责请求头的 `constants.js` 或 `provider-utils.js` 也同步修改为：

- `antigravity/1.15.8`
- `vscode/1.87.0` (或 `1.96.0`)

## 3. 防火墙红线 ⚠️

- **严禁重新认证**: 修补完成后，直接运行程序进行测试。**不要**立即运行 `auth login`。重新认证可能会导致客户端从服务器拉取并持久化旧版本信息，使补丁失效。
- **僵尸进程**: 如果修改后版本被自动改回，说明有隐藏的 `opencode` 或 `node` 进程未杀干净。

## 4. 推荐模型组合

修补完成后，建议使用以下模型以获得最佳稳定性：

- `google-antigravity/gemini-3-pro-high` (替代 gemini-3-pro)
- `google-antigravity/gemini-3-flash`
