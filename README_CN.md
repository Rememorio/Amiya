# Amiya Codex Chat

[English](README.md)

Amiya Codex Chat 是一个运行在 [AstrBot](https://github.com/AstrBotDevs/AstrBot)
上的插件：它监听指定前缀的聊天消息，调用本机 Codex CLI，再把最终回答发回聊天平台。

> Credit: 多平台接入、插件系统、配置 WebUI 和消息事件能力由
> [AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot) 提供。本项目不是
> AstrBot 官方插件。

## 适合什么场景

- 在 QQ / OneBot / Telegram / Discord / 企业微信等 AstrBot 已支持的平台里调用
  Codex。
- 用 `SOUL*.md` 文件定义人格，例如默认的 `SOUL-Amiya.md` 或
  `SOUL-Eyjafjalla.md`。
- 需要简单、可控的 IM 入口，而不是把 AstrBot 配成新的大模型服务提供商。

## 你需要先准备

1. 运行目标机器上已经安装并登录 Codex CLI。
2. 如果你要接 QQ 个人号，准备使用 [LLBot](https://luckylillia.com/)
   作为 OneBot v11 协议端；其他平台按 AstrBot 官方适配器接入。
3. 如果你已有 AstrBot，确认平台适配器已经能正常收发消息。
4. AstrBot 进程能执行 `codex`。如果 AstrBot 是 systemd、Docker、screen、pm2 等方式
   启动，确认它的 PATH 里也能找到 Codex。

先验证 Codex：

```bash
codex --version
codex exec --help
```

## 安装

推荐从 GitHub Release 下载 `astrbot_plugin_amiya_codex-<version>.zip`，然后在
AstrBot WebUI 的插件管理页面上传安装。

本地开发或手动安装时，也可以把仓库放进 AstrBot 的 `data/plugins` 目录：

```text
data/plugins/astrbot_plugin_amiya_codex/
```

安装后重启 AstrBot，或在 WebUI 里重载插件。

### 用 Codex 一个 prompt 从零部署

如果另一台机器只有 Codex，还没有 AstrBot，可以直接把下面这段话发给 Codex。它会
从 AstrBot 官方仓库拉取项目、创建环境、安装插件并启动服务；QQ 个人号默认使用
LLBot 连接 AstrBot。只有 QQ 登录、扫码、系统密码这类必须人工介入的步骤才停下来。

```text
请在这台机器上基于 AstrBot 官方源码仓库端到端部署 AstrBot + Amiya Codex Chat。
除非遇到 QQ/聊天平台登录或扫码、系统密码/sudo、网络不可用、磁盘权限不足这些必须人工处理的步骤，不要再向我确认；请自己选择安全默认值并继续。

规则：
1. AstrBot 只能使用官方仓库：https://github.com/AstrBotDevs/AstrBot。不要使用非官方 fork。
2. QQ 个人号协议端使用 LLBot：https://luckylillia.com/。macOS 优先使用 GitHub Release 里的 `LLBot-Desktop-macos-arm64.tar.xz`；不要改用其他 QQ 协议端，除非我明确要求。
3. 使用 LLBot Desktop 时不要手动安装或配置 PMHQ。PMHQ 是 LLBot 的内部组件，应由 LLBot Desktop 自动下载、启动和管理。
4. 使用 Python 3.12 的隔离环境。有 conda 时优先创建 `astrbot-amiya`，并用 `conda run -n astrbot-amiya ...` 执行命令，避免 shell activate 问题。没有 conda 时使用 Python 3.12 venv。只有系统已经安装 uv 时才用 uv，不要强制依赖 uv。
5. 不要修改系统 Python。不要把本机账号、token、密码、绝对路径写进任何仓库文件。

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
9. 在 AstrBot WebUI 创建 `OneBot v11` 机器人：启用，反向 WebSocket host 用 `0.0.0.0`，端口用 `6199`，token 留空，除非你也会在 LLBot 里设置同一个 token。
10. 安装并启动 LLBot Desktop。打开 LLBot WebUI 或左侧 `Bot 配置`，启用 OneBot 11，并添加反向 WebSocket：type=`ws-reverse`，enable=true，url=`ws://127.0.0.1:6199/ws`，messageFormat=`array`，token 留空。登录或扫码步骤必须停下来让我处理。
11. 在 AstrBot Console 看到 OneBot v11 adapter connected 之后，输出 WebUI 地址、用户名、初始密码或日志位置、AstrBot 目录、插件目录、启动命令、停止命令，以及你实际跑过的测试。
12. 最后提醒我在聊天里发送：兔兔 连通测试、兔兔 状态、兔兔 请只回复 OK。
```

## 最小配置

打开 AstrBot WebUI，进入本插件的配置页。先只改这些字段：

| 字段 | 推荐值 | 说明 |
| --- | --- | --- |
| `soul_file` | `SOUL-Amiya.md` | 默认人格。切换艾雅法拉时填 `SOUL-Eyjafjalla.md`。 |
| `command_prefixes` | `兔兔,Amiya,阿米娅` | 触发插件的前缀；@ 本 bot 也会触发。艾雅法拉可用 `艾雅法拉,Eyjafjalla,小羊`。 |
| `unmatched_policy` | `pass` | `pass` 兼容 AstrBot 原生处理；没配 provider 时用 `silent`；想让 Codex 接管所有非斜杠普通文本时用 `codex`。 |
| `workdir` | 留空 | 留空表示 AstrBot 进程目录。需要让 Codex 看某个项目时再填项目目录。 |
| `sandbox` | `read-only` | 默认只读，先确认链路跑通。 |
| `require_admin` | `true` | 群聊里只允许群主/管理员和白名单用户调用 Codex。 |
| `allow_users` | 留空 | 需要给非管理员授权时，填发送者 ID，多个用英文逗号分隔。不要提交到仓库。 |

保存配置后，在聊天里测试：

```text
兔兔 连通测试
兔兔 状态
兔兔 请只回复 OK
```

前两条不调用 Codex；第三条会真正走 Codex CLI。

## 常用命令

| 消息 | 行为 |
| --- | --- |
| `兔兔 帮助` | 查看命令。 |
| `兔兔 连通测试` | 检查插件是否在线，不调用 Codex。 |
| `兔兔 状态` | 查看版本、沙箱、人格、会话等状态。 |
| `兔兔 人格` | 查看当前人格文件是否加载成功。 |
| `兔兔 会话状态` | 查看当前聊天的 Codex session 状态。 |
| `兔兔 新会话` | 重置当前聊天的 Codex session。 |
| `兔兔 <问题>` | 把问题交给 Codex。 |
| `@阿米娅 <问题>` | 聊天平台把 @ 本 bot 传给 AstrBot 时，把问题交给 Codex。 |

插件永远不会拦截 AstrBot 原生 `/help`、`/reset` 等斜杠命令。未命中
`command_prefixes` 但在 AstrBot 消息链里 @ 本 bot 的消息，会像前缀消息一样触发。
其他非斜杠普通文本由 `unmatched_policy` 决定：`pass` 放行给 AstrBot，`silent`
静默拦截，`codex` 交给 Codex；`codex` 仍然遵守 `require_admin`、`allow_users`
和 `enable_private`。

## 推荐配置模板

安全聊天：

```text
soul_file=SOUL-Amiya.md
command_prefixes=兔兔,Amiya,阿米娅
unmatched_policy=pass
sandbox=read-only
require_admin=true
session_enabled=true
```

艾雅法拉人格：

```text
soul_file=SOUL-Eyjafjalla.md
command_prefixes=艾雅法拉,Eyjafjalla,小羊
sandbox=read-only
require_admin=true
```

受控项目助手：

```text
workdir=<你的项目目录>
sandbox=workspace-write
require_admin=true
allow_users=<可信用户 ID>
```

`danger-full-access` 只应在你明确接受风险的受控环境里使用。

## 文档

- [安装指南](docs/INSTALL_CN.md)
- [配置说明](docs/CONFIGURATION_CN.md)
- [Installation](docs/INSTALL.md)
- [Configuration](docs/CONFIGURATION.md)

## 开发

```bash
python -m py_compile main.py scripts/package.py tests/test_plugin_core.py
python -m unittest discover -s tests -v
python scripts/package.py
```

## 许可证

本插件使用 MIT License。AstrBot 本体由
[AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot) 提供，使用
AGPL-3.0 License；如果你修改 AstrBot 并对外提供网络服务，需要自行遵守 AGPL-3.0
条款。本项目只引导用户从官方仓库安装 AstrBot，不再分发 AstrBot 本体。
