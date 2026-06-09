# 安装指南

本插件依赖 AstrBot 的插件系统和平台适配器。先把 AstrBot 本体和聊天平台接通，再安装
Amiya Codex Chat。

## 1. 安装并启动 AstrBot

按 AstrBot 官方文档安装：<https://github.com/AstrBotDevs/AstrBot>

确认两件事：

- AstrBot WebUI 可以打开。
- 你的平台适配器已经能收发消息，例如 OneBot、QQ 官方、Telegram、Discord、企业微信等。

本插件不替代平台适配器，也不处理 QQ 登录、OneBot 连接或 AstrBot provider 配置。

## 2. 准备 Codex CLI

在运行 AstrBot 的同一台机器上安装并登录 Codex CLI。然后在启动 AstrBot 的同一个
Python/服务环境里验证：

```bash
codex --version
codex exec --help
```

如果这里能运行，但 AstrBot 里提示找不到 Codex，通常是 AstrBot 启动方式的 PATH
不一样。把 `codex_binary` 配成完整可执行文件路径，或修正服务环境。

## 3. 安装插件

### 方式 A：从 Release 安装

1. 在 GitHub Release 下载 `astrbot_plugin_amiya_codex-<version>.zip`。
2. 打开 AstrBot WebUI。
3. 进入插件管理页面，上传 zip。
4. 安装后重启 AstrBot，或在 WebUI 中重载插件。

### 方式 B：本地插件目录

把仓库放到 AstrBot 的插件目录：

```text
data/plugins/astrbot_plugin_amiya_codex/
```

目录根部应该能看到：

```text
main.py
metadata.yaml
_conf_schema.json
SOUL-Amiya.md
SOUL-Eyjafjalla.md
```

然后重启 AstrBot 或重载插件。

## 4. 用 Codex 一个 prompt 从零部署

如果目标机器只有 Codex，还没有 AstrBot，可以让 Codex 根据实际环境完成部署。它会
拉取 AstrBot 官方仓库、创建隔离环境、安装 Amiya 插件并启动 AstrBot；只有 QQ 登录、
扫码、系统密码等必须人工处理的步骤才停下来。

```text
请在这台机器上基于 AstrBot 官方源码仓库端到端部署 AstrBot + Amiya Codex Chat。
除非遇到 QQ/聊天平台登录或扫码、系统密码/sudo、网络不可用、磁盘权限不足这些必须人工处理的步骤，不要再向我确认；请自己选择安全默认值并继续。

规则：
1. AstrBot 只能使用官方仓库：https://github.com/AstrBotDevs/AstrBot。不要使用非官方 fork。
2. 不要安装、启动或依赖 LLOneBot/LLBot。如果旧的 LLOneBot/LLBot 进程占用端口，可以停止该进程并在总结里说明；除非我明确要求，不要删除用户数据。
3. 使用 Python 3.12 的隔离环境。有 conda 时优先创建 `astrbot-amiya`，并用 `conda run -n astrbot-amiya ...` 执行命令，避免 shell activate 问题。没有 conda 时使用 Python 3.12 venv。只有系统已经安装 uv 时才用 uv，不要强制依赖 uv。
4. 不要修改系统 Python。不要把本机账号、token、密码、绝对路径写进任何仓库文件。

目标：
1. 把 https://github.com/AstrBotDevs/AstrBot 克隆或更新到一个 AstrBot 工作目录。
2. 在这个源码 checkout 中安装 AstrBot 依赖。可用 uv 时执行 `uv sync`；否则在 AstrBot 目录执行 `python -m pip install -U pip` 和 `python -m pip install -r requirements.txt`。
3. 在 AstrBot 目录下创建 `data/plugins` 和 `data/config`。
4. 把 https://github.com/Rememorio/Amiya 克隆或更新到 `data/plugins/astrbot_plugin_amiya_codex`。
5. 在 AstrBot 的 `data/config` 写入本地插件配置：soul_file=SOUL-Amiya.md，command_prefixes=兔兔,Amiya,阿米娅，sandbox=read-only，require_admin=true，session_enabled=true，unmatched_policy=silent。首次部署先用 `silent`，因为 AstrBot 可能还没有配置 provider 模型。
6. 在插件目录运行：
   - python -m py_compile main.py scripts/package.py tests/test_plugin_core.py
   - python -m unittest discover -s tests -v
7. 从源码 checkout 用 `python main.py` 启动 AstrBot。源码模式不要直接用 `astrbot run`，除非你安装了 package CLI 并初始化了该目录。如果 6185 端口被占用，用 `DASHBOARD_PORT` 选择其他空闲端口。
8. 用 screen/tmux/nohup 后台运行 AstrBot，并捕获日志。首次启动可能下载 dashboard 静态资源，WebUI 初始密码会打印在启动日志里。
9. 输出 WebUI 地址、用户名、初始密码或日志位置、AstrBot 目录、插件目录、启动命令、停止命令，以及你实际跑过的测试。
10. 如果需要 QQ、OneBot 或其他聊天平台登录或扫码，停下来告诉我需要在 AstrBot WebUI 里配置什么；我完成后你继续检查平台连接。
11. 最后提醒我在聊天里发送：兔兔 连通测试、兔兔 状态、兔兔 请只回复 OK。
```

## 5. 填最小配置

在 AstrBot WebUI 打开 `Amiya Codex Chat` 插件配置。

| 字段 | 建议 |
| --- | --- |
| `soul_file` | 先用 `SOUL-Amiya.md`。 |
| `command_prefixes` | 先用 `兔兔,Amiya,阿米娅`。 |
| `unmatched_policy` | 兼容 AstrBot 时保持 `pass`；没配 provider 模型时用 `silent`。 |
| `sandbox` | 先用 `read-only`。 |
| `workdir` | 先留空。 |
| `require_admin` | 群聊建议保持 `true`。 |
| `allow_users` | 非管理员需要调用时再填。 |

保存后，如果 AstrBot 没有自动重载插件，手动重载或重启。

## 6. 验证

在聊天平台里发送：

```text
兔兔 连通测试
兔兔 状态
兔兔 请只回复 OK
```

判断结果：

- `连通测试` 有回复：插件已加载，平台链路正常。
- `状态` 里显示 `SOUL: 已加载 SOUL-Amiya.md`：人格文件路径正确。
- 第三条回复 `OK` 或接近固定内容：Codex CLI 调用链路正常。

## 常见问题

### 插件没回复

先检查三处：

1. AstrBot 日志里是否加载了 `astrbot_plugin_amiya_codex`。
2. 平台适配器是否已经连接。
3. 发送消息是否以 `command_prefixes` 中的前缀开头。

### 无前缀消息触发 AstrBot provider 报错

如果 AstrBot 没有配置 provider 模型，而且你只想用带前缀的 Amiya/Codex 聊天，
设置 `unmatched_policy=silent`。只有想让 Codex 接管所有非斜杠普通文本时，才用
`unmatched_policy=codex`。斜杠命令始终放行给 AstrBot。

### AstrBot 的 `/help`、`/reset` 会被抢吗

不会。本插件不处理 `/` 开头的原生斜杠命令。

### 我需要在 AstrBot 里配置模型 API Key 吗

不需要。本插件直接调用本机 Codex CLI，不走 AstrBot provider。Codex 的认证由
Codex CLI 自己管理。

### 这样拉 AstrBot 官方仓库有法律风险吗

通常没有额外风险：这是让用户从官方仓库安装 AstrBot，不是把 AstrBot 打包进本项目
release，也不会移除 AstrBot 的 license 或 credit。需要注意的是 AstrBot 本体使用
AGPL-3.0；如果你修改 AstrBot 并对外提供网络服务，需要自行遵守 AGPL-3.0。

### 想换成艾雅法拉人格

把配置改成：

```text
soul_file=SOUL-Eyjafjalla.md
command_prefixes=艾雅法拉,Eyjafjalla,小羊
```

保存并重载插件后，用 `艾雅法拉 状态` 测试。
