# Amiya Codex Chat

Amiya Codex Chat is an AstrBot plugin that lets a chat bot answer prefixed
messages through Codex CLI. It keeps the integration small: persona comes from a
configurable `SOUL` file, Codex runs with conservative defaults, and optional
native Codex sessions are bounded by TTL, turn count, and active-chat limits.

This repository is public. Do not commit account IDs, tokens, private paths, or
machine-specific configuration.

[简体中文文档](README_CN.md)

## Features

- AstrBot Star plugin layout with `main.py`, `metadata.yaml`, `_conf_schema.json`,
  and WebUI i18n resources.
- Works with AstrBot platform adapters such as OneBot, QQ official, Telegram,
  Discord, Slack, Kook, WeCom, Lark, DingTalk, and Satori.
- Configurable persona file. This repository defaults to `SOUL-Amiya.md` and
  also bundles `SOUL-Eyjafjalla.md` as an optional example; the generic fallback
  is `SOUL.md`.
- Bilingual user-facing replies: `zh-CN` and `en-US`.
- Built-in commands: help, ping, status, persona status, session status, session
  reset, and Codex chat.
- Compatible with AstrBot's native `/` slash commands. The plugin only handles
  plain text messages that match configured prefixes.
- Native Codex session resume with TTL, turn, active-chat, and cleanup limits.
- Privacy-safe operational logs without message text or account IDs.
- Conservative default security: Codex runs with `read-only` sandbox and group
  access is limited to admins and allow-listed users.
- `codex exec --ephemeral` fallback when session memory is disabled.

## Requirements

- A working AstrBot installation.
- A supported AstrBot platform adapter configured for your chat platform.
- Codex CLI installed and authenticated on the same machine that runs AstrBot.
- The Python environment used by AstrBot must be able to execute `codex`.

## Quick Start

Build a plugin zip:

```bash
python scripts/package.py
```

Install the generated zip from `dist/` through AstrBot's plugin manager, or place
this repository under AstrBot's `data/plugins` directory as a local plugin. In
the AstrBot plugin configuration, keep the default `SOUL-Amiya.md` persona file
or point `soul_file` to `SOUL-Eyjafjalla.md` or your own file.

Examples below assume the default plugin prefixes:

```text
兔兔 帮助
兔兔 连通测试
兔兔 状态
兔兔 人格
兔兔 会话状态
兔兔 新会话
兔兔 介绍一下你自己
```

When switching to the Eyjafjalla persona, you can also set `command_prefixes` to
something like `艾雅法拉,Eyjafjalla,小羊`.

## Documentation

- [Installation](docs/INSTALL.md)
- [Configuration](docs/CONFIGURATION.md)
- [中文安装指南](docs/INSTALL_CN.md)
- [中文配置说明](docs/CONFIGURATION_CN.md)

## Safety Notes

Use `read-only` sandbox unless the bot explicitly needs to edit files. Keep
`require_admin` enabled for group chats, and use `allow_users` only for trusted
operators. Never place credentials, private account identifiers, or sensitive
machine details in `SOUL` files or documentation.

## License

MIT
