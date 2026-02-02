---
description: 针对 OpenClaw (前 MoltBot) 的高级集成方案：如何让远程 VPS 访问本地文件，以及如何本地部署并连接 Ollama。
---

# OpenClaw 本地交互与 Ollama 集成指南

本 Skill 旨在解决 OpenClaw 在远程 VPS 部署时无法操作本地文件的问题，并提供本地部署接入 Ollama 的完整流程。

## 方案一：远程 VPS 访问/操作本地文件 (Node 模式)

如果你希望保留 VPS 上的机器人（例如为了保证 24 小时在线），但又想让它能操作你手头这台 Windows 电脑的文件，最推荐的方法是使用 **Node (节点) 模式**。

### 1.1 在本地物理机安装 OpenClaw CLI

在你的本地 Windows 电脑上（确保已安装 Node.js）：

```powershell
npm install -g @openclaw/openclaw
```

### 1.2 启动本地节点并配对

在本地终端运行：

```powershell
# 先设置环境变量（替换为你自己的 Token）
$env:OPENCLAW_GATEWAY_TOKEN = "777addeb16861f895326c1f69d40c4a2c9658a55470dbe63"

# 再启动连接
openclaw node run --display-name my-local-pc --host 141.147.154.37
```

你会看到一个 8 位的配对码（Pairing Code）。

### 1.3 在 VPS 上完成配对

登录你的 VPS，运行命令将本地电脑添加为节点：

```bash
openclaw nodes approve --code <8位配对码>
```

### 1.4 如何使用

配对成功后，VPS 上的 AI 助手现在可以感知到 `my-local-pc` 节点。

- **操作文件**：AI 可以调用 `nodes.run` 工具，传入 `node: "my-local-pc"`，并在其中执行 `dir`, `type`, `move` 等 Windows 命令来处理你的本地文件。
- **系统通知**：AI 可以向你的 Windows 弹出通知。

---

## 方案二：本地部署 + Ollama 集成 (全本地化)

如果你希望数据完全不出本地，且直接调用本地的 Ollama 模型。

### 2.1 准备环境

1. **安装 Ollama**: 从 [ollama.com](https://ollama.com) 下载并运行。
2. **拉取模型**:

   ```powershell
   # 用户指定的 qwen3:8b (建议确认为 qwen2.5:7b，目前 Qwen 2.5 是主流)
   ollama pull qwen2.5:7b
   ```

### 2.2 本地启动 OpenClaw (Docker 方式)

使用 Docker 部署可以避免环境污染，且最容易访问本地文件。

```bash
docker run -d \
  --name openclaw \
  -v ~/.openclaw:/root/.openclaw \
  -v /:/root/host:ro \
  -e OLLAMA_API_KEY="ollama-local" \
  openclaw/openclaw:latest
```

> [!TIP]
> 设置 `OLLAMA_API_KEY="ollama-local"` 后，OpenClaw 会自动发现 `http://localhost:11434` 上的所有具备 Tool 能力的模型。

### 2.3 配置模型切换

编辑本地的 `~/.openclaw/clawdbot.json`，将主模型修改为 Ollama 模型：

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/qwen2.5:7b" // 请根据你实际 pull 的模型名称修改
      }
    }
  }
}
```

### 2.4 访问本地文件

在 Docker 启动命令中，我们使用了 `-v /:/root/host:ro`，这意味着：

- AI 可以在工作区中看到主机的整个磁盘（以只读方式，如需读写去掉 `:ro`）。
- 你可以告诉 AI：“在 `/root/host/Users/你的用户名/Desktop` 下寻找文件”。

---

## 方案对比

| 维度 | 方案一 (Remote Gateway + Local Node) | 方案二 (Pure Local + Ollama) |
| :--- | :--- | :--- |
| **优势** | 机器人 24h 在线，低能耗 | 隐私极高，模型免费，无延迟文件读写 |
| **劣势** | 依赖网络连接，本地需运行 Node 进程 | 对电脑显卡有要求，关机即下线 |
| **文件交互** | 通过 `nodes.run` 异步执行 | 直接在 `/root/host` 挂载路径读写 |

## 故障排查

- **Ollama 连不上**：如果 OpenClaw 在 Docker 中运行，`baseUrl` 应设为 `http://host.docker.internal:11434/v1`。
- **Node 不在线**：确保本地防火墙没有拦截 OpenClaw 节点的网络出站请求。
- **权限不足**：在 `openclaw.json` 中确保 `tools.elevated` 设置为 `true`，否则 `nodes.run` 可能会受到严格限制。
