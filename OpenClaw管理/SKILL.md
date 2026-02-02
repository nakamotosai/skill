---
name: OpenClaw与1Panel管理
description: Oracle VPS上的1Panel与OpenClaw机器人日常维护、故障排查、模型切换等常用指令汇总。
---

# OpenClaw 与 1Panel 管理手册

> 本手册汇总了在 Oracle VPS 上运行 OpenClaw 和 1Panel 的所有核心管理指令。

---

## 1. 1Panel 管理 (Web面板)

| 目的 | 命令 |
| :--- | :--- |
| **查看面板信息** | `sudo 1panel user-info` |
| **重置面板密码** | `sudo 1panel update password` (需进入交互模式) |
| **放行面板端口** | `sudo iptables -I INPUT -p tcp --dport 33400 -j ACCEPT` |
| **持久化防火墙** | `sudo netfilter-persistent save` |

---

## 2. OpenClaw 基础维护

### 2.1 服务控制

```bash
# 重启 OpenClaw (当机器人不回话或下线时)
systemctl --user restart openclaw-gateway

# 查看运行状态
systemctl --user status openclaw-gateway

# 查看实时日志
journalctl --user -u openclaw-gateway -f
```

### 2.2 账号绑定 (Pairing)

当 Discord Bot 提示 "Access not configured" 并给出验证码时：

```bash
# 替换 <验证码> 为实际显示的 8 位代码
~/.npm-global/bin/openclaw pairing approve discord <验证码>
```

---

## 3. 模型切换 (Model Switching)

### 3.1 极速切换脚本 (自定义)

执行我为您录入的脚本：

```bash
# 格式: ./switch_model.sh openrouter:模型路径
./switch_model.sh openrouter:google/gemini-2.0-flash-001
```

### 3.2 手动修改配置

1. 编辑文件：`nano ~/.openclaw/clawdbot.json`
2. 找到 `"agents" -> "defaults" -> "model" -> "primary"` 字段进行修改。
3. 保存退出并执行重启命令。

---

## 4. 彻底重置 (恢复出厂设置)

当 `onboard` 报错或配置混乱，需要彻底清除旧记录时：

```bash
# 1. 停止一切相关进程
systemctl --user stop openclaw-gateway
killall node

# 2. 删除隐藏配置文件夹 (重要：会清空历史和配置)
rm -rf ~/.openclaw

# 3. 重新运行引导
openclaw onboard
```

---

## 5. 常见问题排查

- **无法从外网访问 1Panel**：检查 Oracle Cloud 控制台的 Ingress Rules 是否开放 TCP 33400。
- **Upstream error**: 通常是模型 ID 拼写错误或 API Key 在配置中丢失。
- **Command not found**: 很多命令位于 `~/.npm-global/bin/` 目录下，如果不生效请使用绝对路径。
