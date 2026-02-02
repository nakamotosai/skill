---
description: 在现有应用中添加或更新功能。用于迭代开发。
---

# /enhance - 更新应用

$ARGUMENTS

---

## 任务

此指令用于向现有应用添加功能或进行更新。

### 步骤:

1. **理解当前状态**
   - 使用 `session_manager.py` 加载项目状态
   - 了解现有功能、技术栈

2. **规划变更**
   - 确定要添加/更改的内容
   - 检测受影响的文件
   - 检查依赖项

3. **向用户展示计划** (针对重大变更)
   ```
   "要添加管理面板:
   - 我将创建 15 个新文件
   - 更新 8 个文件
   - 大约需要 10 分钟

   我应该开始吗？"
   ```

4. **应用**
   - 调用相关智能体
   - 进行更改
   - 测试

5. **更新预览**
   - 热重载或重启

---

## 使用示例

```
/enhance add dark mode
/enhance build admin panel
/enhance integrate payment system
/enhance add search feature
/enhance edit profile page
/enhance make responsive
```

---

## 注意事项

- 重大变更需获得批准
- 对冲突请求发出警告 (例如: 项目使用 PostgreSQL 但请求 "使用 Firebase")
- 每次更改都要进行 git 提交
