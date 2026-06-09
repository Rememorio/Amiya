# AGENTS.md

These instructions apply to this repository: `Rememorio/Amiya`.

## Project Identity

- This is a public AstrBot plugin repository.
- The plugin bridges AstrBot chat messages to local Codex CLI.
- AstrBot platform adapters, plugin loading, message events, and WebUI config are
  provided by `AstrBotDevs/AstrBot`.
- Always credit AstrBot in user-facing docs and release notes.
- Do not imply this is an official AstrBot plugin unless that becomes true.

## Repository Shape

Keep the AstrBot plugin root layout intact:

- `main.py`
- `metadata.yaml`
- `_conf_schema.json`
- `.astrbot-plugin/i18n/*.json`
- `SOUL*.md`
- `docs/`
- `tests/`
- `scripts/package.py`

The plugin should keep zero runtime dependencies beyond AstrBot and the Python
standard library unless there is a strong reason to change that.

## Documentation Standards

Docs should be practical and short. A new user should know exactly:

- what AstrBot must already provide;
- how to bootstrap AstrBot from the official repository when it is not already
  installed;
- how QQ personal-account deployments should connect through LLBot and
  OneBot v11 reverse WebSocket;
- how to install the plugin;
- which WebUI fields to fill first;
- how to verify the plugin without calling Codex;
- how to verify the Codex CLI path;
- how to switch persona files;
- how the plugin coexists with AstrBot native slash commands.

Maintain both English and Chinese docs when behavior changes:

- `README.md`
- `README_CN.md`
- `docs/INSTALL.md`
- `docs/INSTALL_CN.md`
- `docs/CONFIGURATION.md`
- `docs/CONFIGURATION_CN.md`
- `.astrbot-plugin/i18n/en-US.json`
- `.astrbot-plugin/i18n/zh-CN.json`

Do not add `CHANGELOG.md`. Release notes live on GitHub Releases.

## Compatibility Rules

- Do not intercept AstrBot native `/` slash commands.
- Keep `command_prefixes` runtime-configurable.
- Keep default `sandbox=read-only`.
- Keep group access restricted by default with `require_admin=true`.
- Keep persona file resolution relative to the plugin directory unless an
  absolute path is explicitly configured.
- Keep packaged release files portable; do not include local runtime state.

## Privacy And Security

Never commit:

- account IDs;
- QQ group IDs;
- API keys, tokens, passwords, cookies, or session IDs;
- local absolute paths from a developer machine;
- AstrBot runtime config containing secrets;
- Codex native session files.

Examples and docs may mention placeholder IDs such as `<trusted sender IDs>`.

## Validation

Before committing, run:

```bash
python -m py_compile main.py scripts/package.py tests/test_plugin_core.py
python -m unittest discover -s tests -v
python -m json.tool _conf_schema.json >/dev/null
python -m json.tool .astrbot-plugin/i18n/en-US.json >/dev/null
python -m json.tool .astrbot-plugin/i18n/zh-CN.json >/dev/null
python scripts/package.py
```

Then inspect the generated zip:

- it must include `main.py`, `metadata.yaml`, `_conf_schema.json`, and bundled
  `SOUL*.md` files;
- it must not include `.git`, `__pycache__`, local env files, or runtime state;
- it must not include `CHANGELOG.md`.

## Release Notes

GitHub Release notes should be useful to an installer:

- one-line summary;
- prerequisites;
- install steps;
- minimal WebUI config fields;
- verification messages;
- safety notes;
- credit to AstrBot.
- if natural-language install instructions are shown, they must clone AstrBot
  from `https://github.com/AstrBotDevs/AstrBot`, use an isolated Python
  environment, avoid writing secrets or machine-specific paths into repository
  files, and stop only for mandatory human steps such as chat-platform login or
  system password prompts.
- natural-language install instructions should use LLBot for QQ personal
  accounts, configure AstrBot as the OneBot v11 reverse WebSocket server, and
  configure LLBot with a `ws-reverse` connection to AstrBot. Use AstrBot source mode with
  Python 3.12, install dependencies from the official checkout, and start source
  deployments with `python main.py` unless the package CLI was installed and
  initialized separately.
- include a short license note: AstrBot is AGPL-3.0; this repository does not
  redistribute AstrBot itself.

Do not use release notes as a raw commit log.

## Commit Style

Use concise imperative commit messages, for example:

- `Improve setup documentation`
- `Release v0.0.1`
- `Fix prefix handling`

Do not add generated attribution, AI assistant signatures, or local environment
details to commits, docs, or PR descriptions.
