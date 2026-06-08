# Amiya Codex Chat

[简体中文](README_CN.md)

Amiya Codex Chat is an [AstrBot](https://github.com/AstrBotDevs/AstrBot) plugin
that listens for configured chat prefixes, runs Codex CLI on the same machine,
and sends the final answer back to the chat.

> Credit: platform adapters, plugin loading, the configuration WebUI, and message
> events are provided by [AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot).
> This project is not an official AstrBot plugin.

## When To Use It

- You already use AstrBot with QQ / OneBot / Telegram / Discord / WeCom or other
  supported platforms.
- You want a small Codex CLI bridge controlled by `SOUL*.md` persona files.
- You do not want to configure this as an AstrBot LLM provider with an API key
  and base URL; Codex CLI handles its own local authentication.

## Prerequisites

1. AstrBot is running, and your platform adapter can send and receive messages.
2. Codex CLI is installed and authenticated on the machine running AstrBot.
3. The AstrBot process can execute `codex`. Check the PATH used by your service
   manager, container, screen session, or process supervisor.

Verify from the same environment that starts AstrBot:

```bash
codex --version
codex exec --help
```

## Install

Download `astrbot_plugin_amiya_codex-<version>.zip` from GitHub Releases, then
upload it in AstrBot's plugin manager.

For local development or manual installation, place this repository under
AstrBot's plugin directory:

```text
data/plugins/astrbot_plugin_amiya_codex/
```

Restart AstrBot or reload plugins from the WebUI after installation.

### Natural-Language Install With Codex

If another machine already has Codex working, paste this prompt into Codex:

```text
Please install https://github.com/Rememorio/Amiya as an AstrBot plugin.
Requirements:
1. First find AstrBot's data/plugins directory. If you cannot find it, ask me.
2. Clone or update the repository at data/plugins/astrbot_plugin_amiya_codex.
3. Do not write local accounts, tokens, or absolute machine paths into repository files.
4. Run python -m py_compile main.py scripts/package.py tests/test_plugin_core.py.
5. Run python -m unittest discover -s tests -v.
6. Remind me to configure soul_file, command_prefixes, sandbox, and require_admin in AstrBot WebUI.
7. If AstrBot is already running, explain that I need to reload plugins or restart AstrBot, but do not stop my service without asking.
```

## Minimal Configuration

Open this plugin's configuration page in AstrBot WebUI. Start with these fields:

| Field | Recommended value | Notes |
| --- | --- | --- |
| `soul_file` | `SOUL-Amiya.md` | Use `SOUL-Eyjafjalla.md` for the Eyjafjalla persona. |
| `command_prefixes` | `兔兔,Amiya,阿米娅` | Text prefixes that trigger the plugin. Eyjafjalla example: `艾雅法拉,Eyjafjalla,小羊`. |
| `workdir` | empty | Empty means the AstrBot process directory. Set a project directory only when Codex should see it. |
| `sandbox` | `read-only` | Keep read-only until the chat path is confirmed. |
| `require_admin` | `true` | In group chats, only admins and allow-listed users can call Codex. |
| `allow_users` | empty | Optional sender IDs, comma-separated. Keep real IDs out of this public repository. |

Then test in chat:

```text
兔兔 连通测试
兔兔 状态
兔兔 请只回复 OK
```

The first two commands do not call Codex. The third command runs Codex CLI.

## Commands

| Message | Behavior |
| --- | --- |
| `兔兔 帮助` | Show help. |
| `兔兔 连通测试` | Check whether the plugin is online. Does not call Codex. |
| `兔兔 状态` | Show version, sandbox, persona, and session status. |
| `兔兔 人格` | Show whether the persona file was loaded. |
| `兔兔 会话状态` | Show current Codex session status for this chat. |
| `兔兔 新会话` | Reset the Codex session for this chat. |
| `兔兔 <prompt>` | Send the prompt to Codex. |

The plugin does not intercept AstrBot's native slash commands such as `/help` or
`/reset`. It only handles plain text messages matching `command_prefixes`.

## Configuration Recipes

Safe chat:

```text
soul_file=SOUL-Amiya.md
command_prefixes=兔兔,Amiya,阿米娅
sandbox=read-only
require_admin=true
session_enabled=true
```

Eyjafjalla persona:

```text
soul_file=SOUL-Eyjafjalla.md
command_prefixes=艾雅法拉,Eyjafjalla,小羊
sandbox=read-only
require_admin=true
```

Controlled project assistant:

```text
workdir=<your project directory>
sandbox=workspace-write
require_admin=true
allow_users=<trusted sender IDs>
```

Use `danger-full-access` only in a controlled environment where that risk is
intentional.

## Documentation

- [Installation](docs/INSTALL.md)
- [Configuration](docs/CONFIGURATION.md)
- [中文安装指南](docs/INSTALL_CN.md)
- [中文配置说明](docs/CONFIGURATION_CN.md)

## Development

```bash
python -m py_compile main.py scripts/package.py tests/test_plugin_core.py
python -m unittest discover -s tests -v
python scripts/package.py
```

## License

MIT
