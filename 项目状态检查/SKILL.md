---
description: 显示智能体和项目状态。进度跟踪和状态看板。
---

# /status - 显示状态

$ARGUMENTS

---

## 任务

显示当前项目和智能体状态。

### 显示内容

1. **项目信息**
   - 项目名称和路径
   - 技术栈
   - 当前功能

2. **智能体状态看板**
   - 哪些智能体正在运行
   - 哪些任务已完成
   - 待处理工作

3. **文件统计**
   - 创建的文件数量
   - 修改的文件数量

4. **预览状态**
   - 服务器是否正在运行
   - URL
   - 健康检查

---

## 输出示例

```
=== Project Status ===

📁 Project: my-ecommerce
📂 Path: C:/projects/my-ecommerce
🏷️ Type: nextjs-ecommerce
📊 Status: active

🔧 Tech Stack:
   Framework: next.js
   Database: postgresql
   Auth: clerk
   Payment: stripe

✅ Features (5):
   • product-listing
   • cart
   • checkout
   • user-auth
   • order-history

⏳ Pending (2):
   • admin-panel
   • email-notifications

📄 Files: 73 created, 12 modified

=== Agent Status ===

✅ database-architect → Completed
✅ backend-specialist → Completed
🔄 frontend-specialist → Dashboard components (60%)
⏳ test-engineer → Waiting

=== Preview ===

🌐 URL: http://localhost:3000
💚 Health: OK
```

---

## 技术细节

Status 使用以下脚本：
- `session_manager.py status`
- `auto_preview.py status`
