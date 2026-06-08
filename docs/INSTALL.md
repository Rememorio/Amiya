# Installation

This guide assumes you already have AstrBot and a supported platform adapter
running. The plugin does not replace AstrBot or the adapter; it only adds a
Codex-backed chat handler.

## 1. Prepare Codex CLI

Install and authenticate Codex CLI by following the official Codex
documentation for your platform. On the machine that runs AstrBot, verify:

```bash
codex --version
codex exec --help
```

If AstrBot runs under a service manager, make sure that service has the same
environment needed to find and run `codex`.

## 2. Build the Plugin Zip

From this repository:

```bash
python scripts/package.py
```

The package is written to `dist/astrbot_plugin_amiya_codex-<version>.zip`. The
zip root contains `main.py`, `metadata.yaml`, `_conf_schema.json`, plugin i18n
resources, documentation, and bundled `SOUL*.md` persona files.

## 3. Install into AstrBot

Use one of these installation methods:

- Upload or install the generated zip through AstrBot's plugin manager.
- Place this repository under AstrBot's `data/plugins` directory as a local
  plugin, then restart AstrBot or reload plugins from the WebUI.

After installation, open AstrBot's plugin configuration page and confirm that
`Amiya Codex Chat` is listed. Configure `soul_file`, `sandbox`, `require_admin`,
and other settings as needed.

The repository includes `SOUL-Amiya.md` and `SOUL-Eyjafjalla.md`, and the plugin
config defaults to `SOUL-Amiya.md`. If you use your own persona file, place it
in the plugin directory or use a private runtime configuration path.

## 4. Verify in Chat

Examples below use the default plugin prefix:

```text
兔兔 连通测试
兔兔 帮助
兔兔 介绍一下你自己
```

The first two commands do not call Codex. The last command starts a Codex run.

## Upgrade

Build a new zip, install it through AstrBot's plugin manager, and reload the
plugin. Runtime configuration is managed by AstrBot and should not be stored in
this public repository.
