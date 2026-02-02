---
name: 视频卡片组件
description: A premium, intelligent video card component designed for dashboards and wallpapers. Features adaptive scaling, resource efficiency (auto-pause), and aesthetic controls.
allowed-tools: Read, Write
---

# Intelligent Video Card Component

This skill encapsulates the best practices for creating a high-performance, aesthetically pleasing "Live Wallpaper" style video card component in React.

## 🌟 Core Features (The "Four Pillars")

### 1. Embedded Live Stream (params & config)

Optimized for "set and forget" background usage.

- **Clean Interface**: Removes YouTube branding, controls, and annotations.
- **Auto-Recovery**: Handles stream interruptions with a refresh mechanism.
- **Iframe Params**: `autoplay=1&mute=1&controls=0&disablekb=1&fs=0&loop=1&modestbranding=1&playsinline=1&rel=0&showinfo=0&iv_load_policy=3`

### 2. Resource Efficiency (Auto-Pause)

Crucial for persistent dashboards/wallpapers to save CPU/GPU/Bandwidth.

- **Visibility API**: Pauses video when browser tab is hidden.
- **Lively Wallpaper API**: Specific integration to pause when wallpaper is obscured by other windows (if using Lively).
- **Logic**:
  - Store `isPlaying` state in a `ref` for access inside event listeners.
  - Track `autoPaused` state to only resume videos that *we* paused (not user paused).

### 3. Intelligent Adaptive Scaling (Zoom/Fit)

Calculates geometry in real-time to handle any container aspect ratio.

- **Components**: `ResizeObserver` + Aspect Ratio Math.
- **Two Modes**:
  - **Cover (Zoom)**: Fills the entire card. Good for aesthetics.
    - *Math*: If `ContainerRatio > VideoRatio` -> Match Width (crop top/bottom). Else -> Match Height (crop sides).
  - **Contain (Fit)**: Shows full video. Good for information.
    - *Math*: If `ContainerRatio > VideoRatio` -> Match Height (pillarbox). Else -> Match Width (letterbox).
- **No Hardcoded Values**: Uses calculated pixel values based on `resizeObserver` entries.

### 4. Premium Control Overlay

Aesthetic functional controls that don't block the view.

- **Fade-on-Hover**: Controls only appear when needed.
- **Glassmorphism**: consistent `bg-black/40 backdrop-blur-md` styling.
- **Functional Set**:
  - `Refresh` (Reload iframe)
  - `Play/Pause` (Manual toggle)
  - `Zoom/Fit` (Toggle scaling mode)
  - `Mute/Unmute` (Audio control)

## 📋 Implementation Template

```tsx
import { useState, useRef, useEffect } from 'react';
import { Volume2, VolumeX, Play, Pause, RotateCw, Maximize, Minimize } from 'lucide-react';

export const VideoCard = () => {
    // --- 1. STATE & REFS ---
    const VIDEO_ID = "_k-5U7IeK8g"; // Replace ID
    const [isPlaying, setIsPlaying] = useState(true);
    const [isMuted, setIsMuted] = useState(true);
    const [isZoomed, setIsZoomed] = useState(true);
    const [containerSize, setContainerSize] = useState({ width: 0, height: 0 });
    const [refreshKey, setRefreshKey] = useState(0);
    
    // Refs for imperative access
    const iframeRef = useRef<HTMLIFrameElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);
    const isPlayingRef = useRef(isPlaying);
    const autoPausedRef = useRef(false);

    // --- 2. RESIZE OBSERVER (SMART SCALING) ---
    useEffect(() => {
        if (!containerRef.current) return;
        const resizeObserver = new ResizeObserver((entries) => {
            for (const entry of entries) {
                setContainerSize({
                    width: entry.contentRect.width,
                    height: entry.contentRect.height
                });
            }
        });
        resizeObserver.observe(containerRef.current);
        return () => resizeObserver.disconnect();
    }, []);

    // --- 3. RESOURCE EFFICIENCY LOGIC ---
    useEffect(() => {
        isPlayingRef.current = isPlaying; // Sync ref
    }, [isPlaying]);

    const sendCommand = (func: string, args: any[] = []) => {
        iframeRef.current?.contentWindow?.postMessage(JSON.stringify({
            event: 'command', func, args
        }), '*');
    };

    useEffect(() => {
        const handleVisibilityChange = () => {
            const isHidden = document.hidden; // Or Lively Wallpaper state 0
            if (isHidden && isPlayingRef.current) {
                sendCommand('pauseVideo');
                autoPausedRef.current = true;
                setIsPlaying(false);
            } else if (!isHidden && autoPausedRef.current) {
                sendCommand('playVideo');
                autoPausedRef.current = false;
                setIsPlaying(true);
            }
        };
        document.addEventListener('visibilitychange', handleVisibilityChange);
        // Add Lively Wallpaper listener here if needed
        return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
    }, []);

    // --- 4. ADAPTIVE MATH ---
    const getIframeStyle = () => {
        if (!containerSize.width || !containerSize.height) return { width: '100%', height: '100%' };
        
        const videoRatio = 16 / 9;
        const containerRatio = containerSize.width / containerSize.height;
        let width, height;

        if (isZoomed) {
             // COVER
             if (containerRatio > videoRatio) { width = containerSize.width; height = width / videoRatio; } 
             else { height = containerSize.height; width = height * videoRatio; }
        } else {
             // CONTAIN
             if (containerRatio > videoRatio) { height = containerSize.height; width = height * videoRatio; } 
             else { width = containerSize.width; height = width / videoRatio; }
        }

        return {
            width: `${width}px`, height: `${height}px`,
            top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
            position: 'absolute' as 'absolute'
        };
    };

    // --- RENDER ---
    return (
        <div ref={containerRef} className="relative w-full h-full overflow-hidden bg-black rounded-xl group">
            {/* Video Layer */}
            <div className="absolute inset-0 pointer-events-none" key={refreshKey}>
               <iframe 
                   ref={iframeRef}
                   style={getIframeStyle()} // Apply calculated style
                   src={`https://www.youtube.com/embed/${VIDEO_ID}?enablejsapi=1&autoplay=1&mute=1&controls=0&disablekb=1...`}
                   className="transition-all duration-700 ease-in-out"
               />
            </div>

            {/* Controls Layer */}
            <div className="absolute bottom-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10">
                 {/* Buttons implementation ... */}
                 <button onClick={() => setIsZoomed(!isZoomed)}>
                    {isZoomed ? <Minimize /> : <Maximize />}
                 </button>
            </div>
        </div>
    );
};
```
