---
description: Electron 应用生产环境打包、稳定性优化与常见崩溃排查指南
---

# Electron Production Stability & Troubleshooting

本 Skill 总结了将 Electron 应用从开发环境迁移到生产环境（打包）时常见的稳定性问题及其解决方案。涵盖资源路径、原生依赖、快捷键冲突及崩溃防护。

## 1. 资源路径处理 (Resource Paths)

在 Electron 中，文件路径在 `npm run dev` (不打包) 和 `npm run build` (打包为 ASAR) 环境下表现截然不同。

### ❌ 常见错误

- 使用相对路径 `../public/icon.png`：打包后相对关系会改变。
- 依赖 `__dirname` 定位资源：在 ASAR 中 `__dirname` 行为不可靠。
- 引用了不存在的扩展名（如代码写 `.ico` 但文件是 `.png`）：会导致窗口创建失败或 Tray 初始化崩溃。

### ✅ 最佳实践

创建一个兼容的路径获取辅助函数，并始终使用绝对路径。

```typescript
import { app } from 'electron';
import path from 'path';

// 获取资源文件的正确路径
function getResourcePath(relativePath: string): string {
  // app.getAppPath() 
  // 开发环境: .../project-root
  // 打包环境: .../resources/app.asar
  return path.join(app.getAppPath(), relativePath);
}

// 使用示例
const iconPath = getResourcePath('public/icon.png');
// electron-builder.json 必须包含 "files": ["public/**/*"]
```

## 2. 原生模块与依赖懒加载 (Native Modules & Lazy Loading)

像 `ffmpeg-static`, `fluent-ffmpeg`, `sharp` 等包含二进制或原生绑定的模块，如果在主进程启动时（全局作用域）加载失败，会导致应用**立即闪退**（任务栏图标一闪而过）。

### ❌ 常见错误 (导致启动崩溃)

```typescript
// main.ts 顶部
import { app } from 'electron';
const ffmpeg = require('fluent-ffmpeg'); // 如果路径不对，这里直接崩，捕获不到
const ffmpegPath = require('ffmpeg-static'); // 同上
```

### ✅ 最佳实践 (懒加载)

将易出错的依赖移入在该功能被调用时才加载（如 IPC Handler 内部）。

```typescript
ipcMain.handle('start-conversion', async () => {
  try {
    // 仅在需要时加载
    const ffmpeg = require('fluent-ffmpeg');
    let ffmpegPath = require('ffmpeg-static');
    
    // 修正 ASAR 路径问题 (针对 ffmpeg.exe 等二进制文件)
    if (app.isPackaged) {
      ffmpegPath = ffmpegPath.replace('app.asar', 'app.asar.unpacked');
    }
    ffmpeg.setFfmpegPath(ffmpegPath);
    
    // ... 业务逻辑 ...
  } catch (e) {
    console.error('依赖加载失败:', e);
  }
});
```

**electron-builder 配置**: 确保二进制文件不被打包进 ASAR。

```json
"asarUnpack": [
  "**/node_modules/ffmpeg-static/**"
]
```

## 3. 快捷键冲突处理 (Global Shortcuts)

`globalShortcut.register` 在不同机器上可能因其他软件（如 Snipaste, QQ）占用而失败。

### ✅ 最佳实践

1. **返回值检查**：必须检查 `register` 的返回值。
2. **用户反馈**：如果注册失败，通过 Notification 告知用户。
3. **模式切换**：提供“标准模式”和“防冲突模式”（如 `F1` vs `Alt+F1`），允许用户在托盘菜单切换。

```typescript
function registerShortcuts(mode: 'standard' | 'safe') {
  globalShortcut.unregisterAll();
  
  const key = mode === 'standard' ? 'F1' : 'Alt+F1';
  const success = globalShortcut.register(key, () => { /* ... */ });
  
  if (!success) {
    showNotification(`快捷键 ${key} 注册失败，可能被占用`);
  }
}
```

## 4. 全局崩溃捕获 (Crash Protection)

未捕获的异常会导致主进程直接退出。在生产环境这是致命的。

### ✅ 最佳实践

在 `main.ts` 最顶部添加全局捕获，并写入日志文件。

```typescript
process.on('uncaughtException', (error) => {
  const logPath = path.join(app.getPath('userData'), 'crash.log');
  fs.appendFileSync(logPath, `[${new Date().toISOString()}] ${error.stack}\n`);
  
  // 尽量弹窗提示，而不是静默消失
  if (app.isReady()) {
    dialog.showErrorBox('程序发生严重错误', error.message);
  }
});
```

## 5. 进程残留与文件锁 (Zombie Processes)

如果打包失败提示 `EBUSY: resource busy or locked`，说明旧的进程没退干净。

### ✅ 最佳实践

构建脚本前加清理命令。

**Windows PowerShell**:

```powershell
taskkill /F /IM "YourAppName.exe" /T
npm run build
```

## 6. 排查 "JS冲突" / 双击无反应

当用户反馈“软件打不开”、“JS冲突”时，通常对应以下情况：

1. **资源丢失**：Icon 路径错误 -> `new Tray()` 抛出异常 -> 崩溃。
2. **依赖缺失**：全局 `require` 了打包后路径错误的模块 -> 启动时 Crash。
3. **权限问题**：尝试写入 `Program Files` 下的文件（应始终写入 `app.getPath('userData')` 或用户指定的目录）。

**解决步骤**：

1. 检查 `main.ts` 是否有全局异常捕获。
2. 将所有外部依赖改为懒加载。
3. 确保所有 `try-catch` 块都包裹了关键的初始化代码 (`createWindow`, `createTray`)。
