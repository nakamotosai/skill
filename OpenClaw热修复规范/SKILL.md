---
name: OpenClaw-Hotfix
description: ⚠️ 强制性规范：修改 OpenClaw 容器内代码的标准化流程。
priority: HIGH
---

# OpenClaw 容器代码热修复规范

当需要修改正在运行的 OpenClaw 容器内代码或配置时，**严禁**直接在容器内编辑。必须遵循“本地修改 -> 远端推送 -> 容器注入”的闭环流程。

## 1. 核心链路 (Pipeline)

1. **本地修改 (Local Edit)**: 在 `C:\Users\sai\moltbot` 目录下找到对应的本地备份文件进行编辑。
2. **远端推送 (Remote Push)**: 使用 `scp` 将文件推送到服务器的 `/tmp` 目录。
3. **容器注入 (Container Injection)**: 使用 `docker cp` 将文件从宿主机 `/tmp` 覆盖到容器内部目标路径。
4. **最终验证 (Verification)**: 使用 `docker exec ... cat` 命令抽查容器内文件，确保变更已生效。

## 2. 远端环境参考

- **宿主机用户**: `ubuntu`
- **容器 ID**: `ba039416d0d1`
- **容器内部工作目录**: `/home/node/.openclaw/workspace`
- **SSH 密钥**: `C:\Users\sai\moltbot\ssh-key-2026-01-27.key`

## 3. 常用热修复命令模板

### 推送并覆盖脚本

```powershell
# 1. 上传本地文件到服务器中转站
scp -i "C:\Users\sai\moltbot\ssh-key-2026-01-27.key" -o StrictHostKeyChecking=no .\filename.ext ubuntu@141.147.154.37:/tmp/filename.ext

# 2. 从中转站注入到容器内部
ssh -i "C:\Users\sai\moltbot\ssh-key-2026-01-27.key" ubuntu@141.147.154.37 "sudo docker cp /tmp/filename.ext ba039416d0d1:/home/node/.openclaw/workspace/path/to/target"
```

### 重启容器以应用配置变更

```powershell
ssh -i "C:\Users\sai\moltbot\ssh-key-2026-01-27.key" ubuntu@141.147.154.37 "sudo docker restart ba039416d0d1"
```

## 4. 注意事项

- 注入完成后，必须优先使用 `date` 确认容器时间是否正确，防止日志时间错乱。
- 修改技能 (Skill) 相关文件时，确保容器内的 Python 路径与本地 `SKILL_*.md` 保持一致。
