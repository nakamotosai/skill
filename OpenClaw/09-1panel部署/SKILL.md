---
name: 1panel部署指南
description: 通过1panel部署OpenClaw多模型备用配置的完整流程
---

# OpenClaw 1panel部署指南

本Skill适用于在1panel管理的Docker环境中部署和更新OpenClaw配置。

## 适用场景

- 更新OpenClaw配置文件
- 配置多模型备用方案
- 重启OpenClaw容器
- 故障排查与恢复

---

## 配置更新流程

### 步骤1: 进入容器终端

```
1panel → 容器 → 容器列表 → openclaw → 终端
```

### 步骤2: 备份原配置

```bash
cd /home/node/.openclaw/
cp openclaw.json openclaw.json.backup.$(date +%Y%m%d)
ls -la *.backup*
```

### 步骤3: 编辑配置文件

**方法A - nano编辑器（推荐）：**

```bash
nano openclaw.json
```

**方法B - cat重定向：**

```bash
cat > openclaw.json << 'EOF'
# 粘贴完整JSON内容
EOF
```

### 步骤4: 验证JSON格式

```bash
cat openclaw.json | python3 -m json.tool > /dev/null && echo "✓ 格式正确" || echo "✗ 格式错误"
```

### 步骤5: 重启容器

```
1panel → 容器 → openclaw → 重启
```

### 步骤6: 验证生效

```bash
docker logs openclaw --tail 50
```

---

## 多模型备用配置

### 免费模型组合示例

| 优先级 | 模型 | 来源 | 额度 |
|:---|:---|:---|:---|
| 主模型 | `qwen-portal/coder-model` | Qwen OAuth | 2000次/天 |
| 备用1 | `ollama/<model>` | 本地Ollama | 无限制 |
| 备用2 | `google-gemma/gemma-3-27b-it` | Google API | 14400次/天 |

### 配置JSON片段

```json
{
  "env": {
    "GEMINI_API_KEY": "你的Google API Key"
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "qwen-portal/coder-model",
        "fallbacks": ["ollama/qwen3:8b", "google-gemma/gemma-3-27b-it"]
      }
    }
  },
  "models": {
    "mode": "merge",
    "providers": {
      "ollama": {
        "baseUrl": "https://你的ollama地址/v1",
        "apiKey": "ollama-local",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3:8b",
            "name": "Qwen3 8B",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 32768,
            "maxTokens": 8192
          }
        ]
      },
      "google-gemma": {
        "baseUrl": "https://generativelanguage.googleapis.com/v1beta/openai",
        "apiKey": "${GEMINI_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "gemma-3-27b-it",
            "name": "Gemma 3 27B Instruct",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 128000,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

---

## 故障排查

### Bot无响应

```bash
# 查看日志
docker logs openclaw --tail 100

# 检查Session锁
docker exec -it openclaw ls -la /home/node/.openclaw/agents/main/sessions/*.lock

# 清理锁文件
docker exec -it openclaw rm -f /home/node/.openclaw/agents/main/sessions/*.jsonl.lock
docker restart openclaw
```

### Ollama连接失败

```bash
# 测试Ollama连通性
curl https://你的ollama地址/api/tags
```

### 恢复原配置

```bash
docker exec -it openclaw bash
cd /home/node/.openclaw/
cp openclaw.json.backup.YYYYMMDD openclaw.json
exit
docker restart openclaw
```

---

## 常用命令速查

| 操作 | 命令 |
|:---|:---|
| 查看日志 | `docker logs openclaw --tail 50` |
| 实时日志 | `docker logs openclaw --follow` |
| 进入容器 | `docker exec -it openclaw bash` |
| 重启容器 | `docker restart openclaw` |
| 查看配置 | `docker exec openclaw cat /home/node/.openclaw/openclaw.json` |
