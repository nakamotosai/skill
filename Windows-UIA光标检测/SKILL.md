---
name: Windows UIA 光标位置检测
description: 使用 Windows UI Automation TextPattern 检测光标是否在文本末尾的最佳实践
---

# Windows UIA 光标位置检测 (Smart Insertion)

## 问题背景

在语音输入应用中，需要判断光标是否位于文本末尾：

- **末尾 (Append Mode)**：自动添加句号
- **中间 (Insertion Mode)**：不添加句号，防止出现双标点

## 核心 API

使用 `uiautomation` 库的 `TextPattern` 模式：

```python
import uiautomation as auto

focused = auto.GetFocusedControl()
pattern = focused.GetPattern(auto.PatternId.TextPattern)
selections = pattern.GetSelection()
caret = selections[0]  # 光标位置的 TextRange
```

---

## ❌ 失败方案总结

### 方案 1: 简单 Move(1) + isspace()

```python
moved = chk_range.Move(auto.TextUnit.Character, 1)
if peek_char.isspace():
    is_at_end = True
```

**问题**：空格判定过于宽泛。某些编辑器（如 VSCode）即使在文字中间，`peek_char` 也可能返回空格，导致**误判为末尾**。

### 方案 2: MoveEndpoint 替代 Move

```python
moved = chk_range.MoveEndpoint(auto.TextPatternRangeEndpoint.End, auto.TextUnit.Character, 1)
```

**问题**：部分编辑器不支持 `MoveEndpoint`，会抛异常或返回错误值，导致**句号完全消失**。

### 方案 3: Move(Word) 单词级检测

```python
moved = chk_range.Move(auto.TextUnit.Word, 1)
```

**问题**：很多控件不支持 `Word` 粒度，会回退到异常处理，导致判定失效。

### 方案 4: 复杂 Lookahead 循环

```python
for _ in range(10):
    m_next = chk_range.Move(auto.TextUnit.Character, 1)
    # 多步探测...
```

**问题**：循环逻辑在某些编辑器中行为不一致，导致**要么没句号，要么双句号**。

### 方案 5: 单纯 Move(2)

```python
moved = chk_range.Move(auto.TextUnit.Character, 2)
```

**问题**：跳过了光标紧邻的字符。如果光标后是最后一个句号 `文字|。`，Move(2) 会跳过句号看到换行/空，误判为末尾，导致**双句号**。

---

## ✅ 成功方案 (V13 - DualStep)

**核心思路**：**逐位智能探测 + 异步状态同步**

针对多行编辑器（如 VSCode）中行尾换行符干扰以及短语音识别竞态问题，目前最完美的方案：

### 1. V13-DualStep 逻辑 (核心算法)

```python
# 第一步：探测紧邻的第一个字符
moved_1 = chk_range.Move(auto.TextUnit.Character, 1)

if moved_1 == 0:
    is_at_end = True  # 绝对末尾
else:
    chk_range.ExpandToEnclosingUnit(auto.TextUnit.Character)
    peek_1 = chk_range.GetText()
    
    # A. 换行符 -> 判定为行尾 (出句号)
    if peek_1 in ('\r', '\n', '\r\n'):
        is_at_end = True
    
    # B. 空格 -> 关键的“再看一眼”
    elif peek_1.isspace():
        next_check = chk_range.Clone()
        next_check.Collapse(False)  # 折叠到第一个字符后
        moved_2 = next_check.Move(auto.TextUnit.Character, 1)
        
        if moved_2 == 0:
            is_at_end = True  # 空格后没东西 -> 末尾
        else:
            next_check.ExpandToEnclosingUnit(auto.TextUnit.Character)
            peek_2 = next_check.GetText()
            # 后面又是空气 -> 末尾；后面是文字 -> 插入模式
            is_at_end = (not peek_2 or peek_2 in ('\r', '\n', '\r\n') or peek_2.isspace())
            
    # C. 标点符号 -> 插入模式 (防双标点)
    elif peek_1 in ('，', '。', '！', '？', '；', '：', ',', '.', '!', '?', ';', ':'):
         is_at_end = False
    
    # D. 普通文字 -> 插入模式
    else:
         is_at_end = False
```

### 2. 异步同步机制 (解决竞态)

由于 ASR 识别速度可能快于 UIA 探测速度（尤其短语音），必须使用同步原语：

```python
# 初始化
self._insertion_check_done = threading.Event()

def trigger_insertion_check(self):
    self._insertion_check_done.clear()
    def _worker():
        self._cached_state = self.is_likely_insertion()
        self._insertion_check_done.set()
    threading.Thread(target=_worker, daemon=True).start()

def get_cached_insertion(self):
    # 最多等待 300ms。这是根据 UIA 性能和用户感官卡顿临界点设定的
    wait_ok = self._insertion_check_done.wait(timeout=0.3)
    return self._cached_state
```

---

## 关键经验教训

### 1. 为什么 Move(2) 在 V12 失败了？

在 VSCode 等编辑器中，行尾往往跟着不可见的 `\n`。`Move(2)` 会跨越行边界看到下一行的内容，导致系统误以为你在“文字中间”，从而剥离句号。**必须使用逐位探测 (DualStep)**。

### 2. 竞态问题的隐蔽性

短语音（如“好的”）转写极快，如果不加 `threading.Event.wait`，系统会读取到触发瞬间尚未更新的假结果。

### 3. 性能金标准：300ms

UIA 探测不宜过久。如果 300ms 内没结果（Timeout），应强行返回，以保证打字体验不卡顿。

---

## 依赖

```bash
pip install uiautomation
```

**注意**：需要在 `build_exe.py` 中确认打包包含该库，对 `EditControl` 兼容性最佳。
