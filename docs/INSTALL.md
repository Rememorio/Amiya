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

This plugin does not replace platform adapters and does not handle QQ login,
OneBot connection setup, or AstrBot provider configuration.

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
```

Restart AstrBot or reload plugins.

## 4. Natural-Language Install With Codex

If the target machine already has Codex working, let Codex adapt the install to
that environment:

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

## 5. Fill Minimal Configuration

Open the `Amiya Codex Chat` plugin configuration page in AstrBot WebUI.

| Field | Recommendation |
| --- | --- |
| `soul_file` | Start with `SOUL-Amiya.md`. |
| `command_prefixes` | Start with `兔兔,Amiya,阿米娅`. |
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
- `状态` shows `SOUL: loaded from SOUL-Amiya.md`: persona loading is correct.
- The third message returns `OK` or a close fixed answer: Codex CLI execution is
  working.

## FAQ

### No Reply In Chat

Check:

1. AstrBot logs show `astrbot_plugin_amiya_codex` loaded.
2. The platform adapter is connected.
3. The message starts with one configured `command_prefixes` value.

### Does It Intercept AstrBot Slash Commands

No. The plugin does not handle native slash commands such as `/help` or `/reset`.

### Do I Need An AstrBot Model API Key

No. This plugin calls local Codex CLI directly and does not use AstrBot provider
API key / base URL settings.

### Use The Eyjafjalla Persona

Set:

```text
soul_file=SOUL-Eyjafjalla.md
command_prefixes=艾雅法拉,Eyjafjalla,小羊
```

Save, reload the plugin, and test with `艾雅法拉 状态`.
