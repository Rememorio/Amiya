# Installation

This plugin depends on AstrBot's plugin system and platform adapters. Connect
AstrBot to your chat platform first, then install Amiya Codex Chat.

## 1. Install And Start AstrBot

Follow AstrBot's official project and documentation:
<https://github.com/AstrBotDevs/AstrBot>

Confirm both are true:

- AstrBot WebUI is reachable.
- Your platform adapter can send and receive messages, such as OneBot, QQ
  official, Telegram, Discord, or WeCom.

This plugin does not replace platform adapters and does not handle QQ login or
AstrBot provider configuration.

For a personal QQ account, prefer
[LLBot](https://luckylillia.com/) as the OneBot v11 protocol
implementation. The path is:

```text
Amiya Codex Chat -> AstrBot -> OneBot v11 reverse WebSocket -> LLBot -> QQ
```

In AstrBot, create a `OneBot v11` bot with reverse WebSocket host `0.0.0.0` and
port `6199`. In LLBot, enable OneBot 11 and add a `ws-reverse` connection with URL
`ws://127.0.0.1:6199/ws`. If AstrBot and LLBot are on different machines,
replace `127.0.0.1` with the AstrBot host.

When using LLBot Desktop, do not install or configure PMHQ manually. PMHQ is an
internal LLBot component; LLBot Desktop should download, start, and manage it.

## 2. Prepare Codex CLI

Install and authenticate Codex CLI on the same machine that runs AstrBot. Verify
from the same Python/service environment that starts AstrBot:

```bash
codex --version
codex exec --help
```

If the command works in your shell but AstrBot says Codex is missing, the AstrBot
process probably has a different PATH. Set `codex_binary` to the full executable
path or fix the service environment.

## 3. Install The Plugin

### Option A: Install From Release

1. Download `astrbot_plugin_amiya_codex-<version>.zip` from GitHub Releases.
2. Open AstrBot WebUI.
3. Upload the zip in the plugin manager.
4. Restart AstrBot or reload plugins from the WebUI.

### Option B: Local Plugin Directory

Place this repository under AstrBot's plugin directory:

```text
data/plugins/astrbot_plugin_amiya_codex/
```

The plugin root should contain:

```text
main.py
metadata.yaml
_conf_schema.json
SOUL-Amiya.md
SOUL-Eyjafjalla.md
SOUL-Requiem.md
```

Restart AstrBot or reload plugins.

## 4. One-Prompt Bootstrap With Codex

If the target machine has Codex but not AstrBot yet, let Codex adapt the
deployment to that environment. It clones AstrBot from the official repository,
creates an isolated environment, installs Amiya, and starts AstrBot. Personal QQ
accounts use LLBot by default. It should only stop for mandatory human steps
such as QQ login, QR scanning, or system password prompts.

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

## 5. Fill Minimal Configuration

Open the `Amiya Codex Chat` plugin configuration page in AstrBot WebUI.

| Field | Recommendation |
| --- | --- |
| `soul_file` | Start with `SOUL-Amiya.md`. Other bundled options include `SOUL-Eyjafjalla.md` and `SOUL-Requiem.md`. |
| `command_prefixes` | Start with `兔兔,Amiya,阿米娅`. |
| `unmatched_policy` | Keep `pass` for AstrBot compatibility. Use `silent` if AstrBot has no provider model. |
| `sandbox` | Start with `read-only`. |
| `workdir` | Leave empty at first. |
| `require_admin` | Keep `true` for group chats. |
| `allow_users` | Fill only when non-admin users should call Codex. |

Save the configuration. Reload or restart AstrBot if the plugin is not reloaded
automatically.

## 6. Verify

Send these messages in chat:

```text
兔兔 连通测试
兔兔 状态
兔兔 请只回复 OK
```

Expected result:

- `连通测试` replies: plugin and platform path are connected.
- `状态` shows `人格：已加载 SOUL-Amiya.md`: persona loading is correct.
- The third message returns `OK` or a close fixed answer: Codex CLI execution is
  working.

## FAQ

### No Reply In Chat

Check:

1. AstrBot logs show `astrbot_plugin_amiya_codex` loaded.
2. The platform adapter is connected.
3. The message starts with one configured `command_prefixes` value or mentions
   this bot in the AstrBot message chain.

### Non-Prefixed Messages Trigger AstrBot Provider Errors

Set `unmatched_policy=silent` if AstrBot has no provider model configured and
you only want prefixed Amiya/Codex chat. Use `unmatched_policy=codex` only when
Codex should handle every non-slash plain text message. Slash commands are
always passed to AstrBot.

### Does It Intercept AstrBot Slash Commands

No. The plugin does not handle native slash commands such as `/help` or `/reset`.

### Do I Need An AstrBot Model API Key

No. This plugin calls local Codex CLI directly and does not use AstrBot provider
API key / base URL settings.

### Is Cloning AstrBot From The Official Repository A Legal Problem

Normally no: the instructions tell users to install AstrBot from its official
repository; this project does not bundle AstrBot in its own release or remove
AstrBot's license/credit. AstrBot itself is AGPL-3.0. If you modify AstrBot and
provide it as a network service, you are responsible for complying with AGPL-3.0.

### Use The Eyjafjalla Persona

Set:

```text
soul_file=SOUL-Eyjafjalla.md
command_prefixes=艾雅法拉,Eyjafjalla,小羊
```

Save, reload the plugin, and test with `艾雅法拉 状态`.

### Use The Requiem Persona

Set:

```text
soul_file=SOUL-Requiem.md
command_prefixes=安魂曲,Requiem
```

Save, reload the plugin, and test with `安魂曲 状态`.
