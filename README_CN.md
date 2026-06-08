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

1. 已运行 AstrBot，并且平台适配器已经能正常收发消息。
2. 运行 AstrBot 的机器上已经安装并登录 Codex CLI。
3. AstrBot 进程能执行 `codex`。如果 AstrBot 是 systemd、Docker、screen、pm2 等方式
   启动，确认它的 PATH 里也能找到 Codex。

在 AstrBot 所在环境里先验证：

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

### 用 Codex 自然语言安装

如果另一台机器已经能运行 Codex，可以直接把下面这段话发给 Codex：

```text
请帮我把 https://github.com/Rememorio/Amiya 安装成 AstrBot 插件。
要求：
1. 先找到 AstrBot 的 data/plugins 目录；如果找不到，先问我。
2. 把仓库克隆或更新到 data/plugins/astrbot_plugin_amiya_codex。
3. 不要把任何本机账号、token、绝对路径写进仓库文件。
4. 运行 python -m py_compile main.py scripts/package.py tests/test_plugin_core.py。
5. 运行 python -m unittest discover -s tests -v。
6. 提醒我在 AstrBot WebUI 里配置 soul_file、command_prefixes、sandbox、require_admin。
7. 如果 AstrBot 正在运行，说明需要重载插件或重启 AstrBot，但不要擅自停止我的服务。
```

## 最小配置

打开 AstrBot WebUI，进入本插件的配置页。先只改这些字段：

| 字段 | 推荐值 | 说明 |
| --- | --- | --- |
| `soul_file` | `SOUL-Amiya.md` | 默认人格。切换艾雅法拉时填 `SOUL-Eyjafjalla.md`。 |
| `command_prefixes` | `兔兔,Amiya,阿米娅` | 触发插件的前缀。艾雅法拉可用 `艾雅法拉,Eyjafjalla,小羊`。 |
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

插件不会拦截 AstrBot 原生 `/help`、`/reset` 等斜杠命令；只有命中
`command_prefixes` 的普通文本会被本插件处理。

## 推荐配置模板

安全聊天：

```text
soul_file=SOUL-Amiya.md
command_prefixes=兔兔,Amiya,阿米娅
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

MIT
