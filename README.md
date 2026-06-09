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

1. Codex CLI is installed and authenticated on the target machine.
2. For a personal QQ account, use [LLBot](https://luckylillia.com/)
   as the OneBot v11 protocol implementation. For other platforms, use the
   official AstrBot adapters.
3. If you already have AstrBot, your platform adapter can send and receive messages.
4. The AstrBot process can execute `codex`. Check the PATH used by your service
   manager, container, screen session, or process supervisor.

Verify Codex first:

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

### One-Prompt Bootstrap With Codex

If the target machine has Codex but not AstrBot yet, paste this prompt into
Codex. It clones AstrBot from the official repository, creates an environment,
installs this plugin, and starts the bot. Personal QQ accounts use LLBot by
default. It should only stop for mandatory human steps such as QQ login, QR
scanning, or system password prompts.

```text
Please deploy AstrBot + Amiya Codex Chat end to end on this machine from the official AstrBot source repository.
Do not ask me for confirmation unless you hit QQ/chat-platform login or QR scan, system password/sudo, unavailable network, or insufficient disk permissions. Choose safe defaults and keep going.

Rules:
1. Use only the official AstrBot repository: https://github.com/AstrBotDevs/AstrBot. Do not use unofficial forks.
2. Use LLBot for personal QQ account protocol support: https://luckylillia.com/. On macOS, prefer `LLBot-Desktop-macos-arm64.tar.xz` from GitHub Releases. Do not switch to another QQ protocol implementation unless I explicitly ask.
3. Do not manually install or configure PMHQ when using LLBot Desktop. PMHQ is an internal LLBot component and LLBot Desktop should download, start, and manage it automatically.
4. Use Python 3.12 in an isolated environment. Prefer a conda environment named `astrbot-amiya` when conda is available, and run commands with `conda run -n astrbot-amiya ...` to avoid shell activation issues. If conda is unavailable, use a Python 3.12 venv. Use uv only when it is already installed; do not require uv.
5. Do not modify system Python. Do not write local accounts, tokens, passwords, or absolute machine paths into repository files.

Goals:
1. Clone or update https://github.com/AstrBotDevs/AstrBot into an AstrBot working directory.
2. Install AstrBot dependencies from that source checkout. If uv is available, use `uv sync`; otherwise use `python -m pip install -U pip` and `python -m pip install -r requirements.txt` from the AstrBot directory.
3. Create `data/plugins` and `data/config` under the AstrBot directory.
4. Clone or update https://github.com/Rememorio/Amiya into `data/plugins/astrbot_plugin_amiya_codex`.
5. Write local plugin config under AstrBot's `data/config` with: soul_file=SOUL-Amiya.md, command_prefixes=兔兔,Amiya,阿米娅, sandbox=read-only, require_admin=true, session_enabled=true, unmatched_policy=silent. Use `silent` for first setup because AstrBot may not have a provider model configured yet.
6. In the plugin directory, run:
   - python -m py_compile main.py scripts/package.py tests/test_plugin_core.py
   - python -m unittest discover -s tests -v
7. Start AstrBot from the source checkout with `python main.py`. Do not use `astrbot run` for source mode unless you installed the package CLI and initialized that directory. If port 6185 is busy, choose another free dashboard port with `DASHBOARD_PORT`.
8. Run AstrBot in the background with screen/tmux/nohup and capture logs. First startup may download dashboard assets, and the initial WebUI password is printed in startup logs.
9. In AstrBot WebUI, create a `OneBot v11` bot: enable it, set reverse WebSocket host to `0.0.0.0`, port to `6199`, and leave the token empty unless you also set the same token in LLBot.
10. Install and start LLBot Desktop. In LLBot WebUI or the left-side `Bot Config` page, enable OneBot 11 and add a reverse WebSocket connection: type=`ws-reverse`, enable=true, url=`ws://127.0.0.1:6199/ws`, messageFormat=`array`, token empty. Stop for me to handle QQ login or QR scanning.
11. After AstrBot Console shows the OneBot v11 adapter connected, report the WebUI URL, username, initial password or log location, AstrBot directory, plugin directory, start command, stop command, and the exact tests you ran.
12. At the end, remind me to test in chat with: 兔兔 连通测试, 兔兔 状态, 兔兔 请只回复 OK.
```

## Minimal Configuration

Open this plugin's configuration page in AstrBot WebUI. Start with these fields:

| Field | Recommended value | Notes |
| --- | --- | --- |
| `soul_file` | `SOUL-Amiya.md` | Bundled personas include `SOUL-Amiya.md`, `SOUL-Eyjafjalla.md`, and `SOUL-Requiem.md`. |
| `command_prefixes` | `兔兔,Amiya,阿米娅` | Text prefixes that trigger the plugin; @ this bot also triggers it. Eyjafjalla example: `艾雅法拉,Eyjafjalla,小羊`. |
| `unmatched_policy` | `pass` | `pass` keeps AstrBot compatibility. Use `silent` when AstrBot has no provider, or `codex` to let Codex handle all non-slash plain text. |
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
| `@Amiya <prompt>` | Send the prompt to Codex when the platform delivers an AstrBot mention for this bot. |

The plugin never intercepts AstrBot's native slash commands such as `/help` or
`/reset`. A message that mentions this bot anywhere in the AstrBot message chain
is treated like a configured prefix. Other non-slash messages that do not match
`command_prefixes` follow `unmatched_policy`: `pass` sends them back to AstrBot,
`silent` stops them without a reply, and `codex` sends them to Codex while still
respecting `require_admin`, `allow_users`, and `enable_private`.

## Configuration Recipes

Safe chat:

```text
soul_file=SOUL-Amiya.md
command_prefixes=兔兔,Amiya,阿米娅
unmatched_policy=pass
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

Requiem persona:

```text
soul_file=SOUL-Requiem.md
command_prefixes=安魂曲,Requiem
sandbox=read-only
require_admin=true
```

SOUL files can start with optional front matter to customize built-in replies:

```text
---
display_name: 安魂曲
user_title: 鉴定师
help_prefix: 安魂曲
message.permission_denied: 鉴定师，这份委托……安魂曲现在还不能接。
---
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

This plugin is MIT-licensed. AstrBot itself is provided by
[AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot) under the AGPL-3.0
License. If you modify AstrBot and provide it as a network service, you are
responsible for AGPL-3.0 compliance. This project only guides users to install
AstrBot from the official repository and does not redistribute AstrBot itself.
