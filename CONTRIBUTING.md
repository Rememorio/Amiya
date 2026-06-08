# Contributing

Thank you for improving Amiya Codex Chat.

## Development

Use a Python version supported by your AstrBot installation. This plugin
intentionally depends only on AstrBot and the Python standard library.

Before submitting a change, run:

```bash
python -m py_compile main.py scripts/package.py
python -m unittest discover -s tests
python scripts/package.py
```

If you change user-facing behavior, update both English and Chinese
documentation and the WebUI i18n resources under `.astrbot-plugin/i18n`.

## Project Rules

- Keep changes minimal and compatible with AstrBot plugin loading.
- Keep `main.py`, `metadata.yaml`, and `_conf_schema.json` at the plugin root.
- Preserve bilingual user-facing strings where practical.
- Do not commit private account identifiers, access tokens, local absolute
  paths, or machine-specific configuration.
- Do not add generated attribution or tool signatures to code, docs, commits,
  or pull requests.

## Persona Changes

Bundled `SOUL*.md` files are public example personas. Keep them concise and
safe for public distribution. User-specific persona files should live in
private runtime configuration, not in this repository.
