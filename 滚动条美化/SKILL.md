---
name: 滚动条美化
description: Advanced techniques for custom, auto-hiding, and layout-neutral scrollbars. Ensures "luxury" feel by preventing scrollbar layout shift and maintaining perfect symmetry.
allowed-tools: Read, Write, Edit
---

# Luxury Scrollbar Styling

> **Philosophy:** A scrollbar should be a functional affordance that appears only when needed, never a permanent visual scar. It must never shift layout.

---

## 1. The "Ghost Overlay" Pattern (Golden Standard)

This pattern ensures that the scrollbar **never shifts layout**, sits **outside** the content's visual alignment boundary, and **auto-hides** when inactive.

### A. CSS Implementation (Index.css)

Add this global utility to your base CSS layer.

**Key Features:**

- `overflow-y: overlay` (WebKit) floats the scrollbar on top of content.
- `scrollbar-width/color` are **removed** to force Chromium/WebKit custom styling.
- `width: 0; height: 0` on buttons ensures no ugly arrows.
- `transparent` track and default thumb make it invisible when inactive.

```css
/* Custom Luxury Scrollbar - WebKit Only for Layout Stability */
.custom-scrollbar {
  overflow-y: overlay; /* Critical: floats scrollbar over content */
}

/* Force WebKit styling by NOT setting standard scrollbar-color/width */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px; /* Ultra-thin luxury feel */
  background: transparent;
}

/* Remove ugly up/down arrows */
.custom-scrollbar::-webkit-scrollbar-button {
  display: none;
  width: 0;
  height: 0;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: transparent; /* Default hidden */
  border-radius: 20px;
  transition: background-color 0.3s;
}

/* Apply color ONLY when scrolling or hovering */
.custom-scrollbar.scrolling::-webkit-scrollbar-thumb,
.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: rgba(212, 175, 55, 0.5); /* Adjust color to theme */
}

.custom-scrollbar.scrolling::-webkit-scrollbar-thumb:hover,
.custom-scrollbar:hover::-webkit-scrollbar-thumb:hover {
  background-color: rgba(212, 175, 55, 0.8);
}
```

### B. React Auto-Hide Logic

Use Javascript to toggle the `.scrolling` class. This provides a smoother UX than pure `:hover`, as it shows feedback *while* interacting.

```tsx
import { useRef, useEffect } from 'react';

// In your component:
const scrollContainerRef = useRef<HTMLDivElement>(null);

useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    let timeoutId: ReturnType<typeof setTimeout>;

    const handleScroll = () => {
        container.classList.add('scrolling');
        
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            container.classList.remove('scrolling');
        }, 1000); // 1s hide delay
    };

    container.addEventListener('scroll', handleScroll);
    return () => {
        container.removeEventListener('scroll', handleScroll);
        clearTimeout(timeoutId);
    };
}, []);

// Render
<div ref={scrollContainerRef} className="custom-scrollbar ...">
    ...
</div>
```

---

## 2. Layout Symmetry Strategy (Negative Margin Hack)

**Problem:** Even with overlay scrollbars, if you have a `p-5` container, the scrollbar appears *inside* the content box, potentially overlapping right-aligned text or looking asymmetrical vs the left side.

**Solution:** Push the scrollbar **into the padding/margin** area so content stays perfectly aligned.

### The Formula

1. **Extend Right:** Add negative right margin equal to the desired padding/gutter.
2. **Push Back:** Add positive right padding equal to the negative margin.

```tsx
<div 
  className="... pr-3 -mr-3" 
  // -mr-3: Pulls container 12px RIGHT (into the parent's padding)
  // pr-3: Pushes content 12px LEFT (back to original alignment)
>
```

**Visual Result:**

- **No Scrollbar:** Content aligns perfectly with headers/inputs above it. Left and Right margins visualy appear equal.
- **Scrollbar Visible:** The scrollbar floats in the *extra space* created by the negative margin, appearing to sit "outside" the content alignment line.

---

## 3. Checklist for Luxury Scrollbars

- [ ] **No Arrows**: Are top/bottom buttons completely hidden?
- [ ] **Ultra-Thin**: Is width <= 4px? (8px is too chunky for "luxury").
- [ ] **Auto-Hiding**: Does it vanish when not being used?
- [ ] **Symmetrical**: Does the container look balanced/aligned when the scrollbar is **NOT** visible?
- [ ] **Themed**: Does the thumb color match the app's accent (e.g., Gold, Neon) rather than system grey?
