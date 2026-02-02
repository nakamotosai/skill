---
name: Electron录屏稳定性
description: Best practices for stable screen recording, global shortcuts, and FFmpeg transcoding in Electron.
---

# Electron Recording & FFmpeg Best Practices

This skill summarizes critical patterns for building stable screen recording applications in Electron, specifically addressing `MediaRecorder`, `ffmpeg-static`, and `globalShortcut` issues.

## 1. MediaRecorder & File Integrity

### The "Invalid Data" / 0KB Bug

**Problem**: Using `recorder.start(1000)` (timeslice) generates multiple partial Blobs. While useful for streaming, concatenating these blobs manually often results in a WebM file with repeated or corrupted headers that FFmpeg cannot parse (`Invalid data found when processing input`).

**Solution**:

- **Remove Timeslice**: Use `recorder.start()` without arguments for local recording. This forces the browser to generate a single, standards-compliant Blob with a correct header and duration when `stop()` is called.
- **Buffer Safety**: When passing the buffer from Renderer to Main process, ensure you check `buffer.byteLength` (ArrayBuffer) rather than just `.length`.

```typescript
// Renderer (BackgroundRecorder.tsx)
// BAD: recorder.start(1000); 
// GOOD:
recorder.start(); 
```

## 2. Global Shortcut Lifecycle

### The "Dead Shortcut" Bug

**Problem**: dynamic registration/unregistration of shortcuts (e.g., registering 'F3' when recording starts and unregistering when it stops) is fragile. If the app crashes, or state desyncs, the shortcut becomes permanently unregistered or "dead".

**Solution**:

- **Static Registration**: Register shortcuts **ONCE** at app startup (`app.whenReady`). Never unregister them during runtime.
- **State-Driven Logic**: Inside the callback, check a state variable (`isRecording`) to determine behavior.

```typescript
// Main Process
let isRecording = false;

function registerShortcuts() {
  globalShortcut.register('F3', () => {
    if (isRecording) {
      stopRecording(); // Logic to stop
    } else {
      startRecording(); // Logic to start
    }
    // Do NOT toggle isRecording here immediately if the process is async;
    // let the start/stop handlers update the state.
  });
}
```

## 3. FFmpeg in Packaged Electron

### The "__dirname" & Path Bug

**Problem**:

1. `fluent-ffmpeg` relies on `__dirname` to find executables, but `__dirname` is undefined in ES Modules or some Electron build configs.
2. `ffmpeg-static` returns a path inside `app.asar`, but binaries cannot be executed directly from within an ASAR archive.

**Solution**:

- **Polyfill `__dirname`**:

  ```typescript
  import { fileURLToPath } from 'url';
  import path from 'path';
  const __dirname = path.dirname(fileURLToPath(import.meta.url));
  (global as any).__dirname = __dirname; // Critical for some libs
  ```

- **Unpack Executable**: Replace `app.asar` with `app.asar.unpacked` in the path.

```typescript
// Main Process
import ffmpeg from 'fluent-ffmpeg';
let staticPath = require('ffmpeg-static');
if (staticPath.path) staticPath = staticPath.path; // Handle object return

let ffmpegPath = staticPath;
if (app.isPackaged) {
    // Binaries are unpacked to a parallel directory
    ffmpegPath = staticPath.replace('app.asar', 'app.asar.unpacked');
}
ffmpeg.setFfmpegPath(ffmpegPath);
```

### The "Auto-Detect" Fix

**Problem**: Hardcoding `.inputFormat('webm')` causes failures if the header is slightly malformed or if `fluent-ffmpeg` fails to probe the pipe correctly.

**Solution**: Remove explicit input format. Let FFmpeg probe the file content.

```typescript
ffmpeg(inputPath)
  // .inputFormat('webm') // REMOVE THIS
  .inputOption('-fflags +genpts') // HELP with timestamps
  .save(outputPath);
```

## 4. Mouse Click-Through (鼠标穿透)

### The "Can't Click Desktop During Recording" Bug

**Problem**: During screen recording, the transparent overlay window captures all mouse events, preventing users from interacting with the desktop.

**Solution**:

- **Use `setIgnoreMouseEvents` with `forward: true`**: This allows the window to be transparent to clicks while still tracking mouse position.
- **Enable `pointerEvents: 'none'`** on the root container in CSS.
- **Restore click handling on control elements**: Use `onMouseEnter`/`onMouseLeave` to toggle `setIgnoreMouseEvents`.

```typescript
// Main Process - IPC handler
ipcMain.on('set-ignore-mouse-events', (event, ignore, options) => {
  const win = BrowserWindow.fromWebContents(event.sender);
  if (win) {
    if (ignore) {
      win.setIgnoreMouseEvents(true, { forward: true }); // CRITICAL: forward must be true
    } else {
      win.setIgnoreMouseEvents(false);
    }
  }
});
```

```tsx
// Renderer - RecordingPanel.tsx
useEffect(() => {
  window.electronAPI.setIgnoreMouseEvents(true, { forward: true });
  return () => window.electronAPI.setIgnoreMouseEvents(false);
}, []);

// Control bar hover handlers
const handleControlMouseEnter = () => {
  window.electronAPI.setIgnoreMouseEvents(false); // Allow clicks
};
const handleControlMouseLeave = () => {
  window.electronAPI.setIgnoreMouseEvents(true, { forward: true }); // Resume pass-through
};
```

## 5. Vite HMR + Background Window (连续录制失败)

### The "Recording Works Once, Then Fails" Bug

**Problem**: In Vite dev mode, Hot Module Replacement (HMR) causes the background recorder window to reload, destroying the IPC listeners registered by React components. Subsequent recording attempts fail silently because `start-recording` messages are never received.

**Symptoms**:

- First 1-3 recordings work, then subsequent ones produce 0-byte videos
- Console shows `Background Recorder Mounted` multiple times
- `ondataavailable` never fires on subsequent recordings

**Solution**: **Destroy and recreate the recorder window before each recording**. This ensures a clean state with fresh IPC listeners.

```typescript
// Main Process
ipcMain.handle('start-recording-worker', async (_e, rect) => {
  // CRITICAL FIX: Destroy old window to avoid stale IPC listeners
  if (recorderWindow && !recorderWindow.isDestroyed()) {
    console.log('[Main] Destroying old recorderWindow for clean state');
    recorderWindow.destroy();
    recorderWindow = null;
  }
  
  console.log('[Main] Creating fresh recorderWindow');
  createRecorderWindow();
  
  // Wait for page load + React mount
  await new Promise<void>((resolve) => {
    recorderWindow!.webContents.once('did-finish-load', () => {
      setTimeout(() => resolve(), 100); // Extra delay for React
    });
  });
  
  recorderWindow?.webContents.send('start-recording', rect, settings);
});
```

### Renderer-Side Cleanup

Also clean up previous recording state at the start of `handleStart`:

```tsx
// BackgroundRecorder.tsx - inside handleStart
// Clean previous state
if (mediaRecorderRef.current?.state !== 'inactive') {
  try { mediaRecorderRef.current.stop(); } catch (e) {}
}
if (streamRef.current) {
  streamRef.current.getTracks().forEach(t => t.stop());
}
chunksRef.current = [];
```

## 6. Debugging Tips

### Add DevTools Menu to Tray

Add a submenu for quick access to DevTools during development:

```typescript
{
  label: '🔧 开发者工具',
  submenu: [
    { 
      label: '打开录制器 DevTools', 
      click: () => {
        if (recorderWindow && !recorderWindow.isDestroyed()) {
          recorderWindow.webContents.openDevTools({ mode: 'detach' });
        }
      }
    }
  ]
}
```

### Forward Console Logs to Terminal

```typescript
recorderWindow.webContents.on('console-message', (e, level, msg) => {
  console.log('[Recorder]:', msg);
});
```
