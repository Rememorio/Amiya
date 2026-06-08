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

## 4. 用 Codex 自然语言安装

如果目标机器已经有 Codex，可以让 Codex 根据实际环境安装：

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

## 5. 填最小配置

在 AstrBot WebUI 打开 `Amiya Codex Chat` 插件配置。

| 字段 | 建议 |
| --- | --- |
| `soul_file` | 先用 `SOUL-Amiya.md`。 |
| `command_prefixes` | 先用 `兔兔,Amiya,阿米娅`。 |
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

### AstrBot 的 `/help`、`/reset` 会被抢吗

不会。本插件不处理 `/` 开头的原生斜杠命令。

### 我需要在 AstrBot 里配置模型 API Key 吗

不需要。本插件直接调用本机 Codex CLI，不走 AstrBot provider。Codex 的认证由
Codex CLI 自己管理。

### 想换成艾雅法拉人格

把配置改成：

```text
soul_file=SOUL-Eyjafjalla.md
command_prefixes=艾雅法拉,Eyjafjalla,小羊
```

保存并重载插件后，用 `艾雅法拉 状态` 测试。
