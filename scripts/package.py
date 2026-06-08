#!/usr/bin/env python3
"""Build an AstrBot plugin zip for Amiya Codex Chat."""

from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path
from typing import Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
METADATA_FILE = ROOT / "metadata.yaml"
DIST_DIR = ROOT / "dist"
ZIP_TIMESTAMP = (2024, 1, 1, 0, 0, 0)

STATIC_PACKAGE_FILES = [
    "main.py",
    "__init__.py",
    "metadata.yaml",
    "_conf_schema.json",
    ".astrbot-plugin/i18n/en-US.json",
    ".astrbot-plugin/i18n/zh-CN.json",
    "README.md",
    "README_CN.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "docs/INSTALL.md",
    "docs/INSTALL_CN.md",
    "docs/CONFIGURATION.md",
    "docs/CONFIGURATION_CN.md",
]


def _read_metadata() -> Tuple[str, str]:
    source = METADATA_FILE.read_text(encoding="utf-8")
    plugin_id = _match_metadata_value(source, "name")
    version = _match_metadata_value(source, "version")
    return plugin_id, version


def _match_metadata_value(source: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*[\"']?([^\"'\n]+)[\"']?\s*$", source, re.MULTILINE)
    if not match:
        raise SystemExit(f"Unable to find {name} in metadata.yaml")
    return match.group(1).strip()


def _write_file(zip_file: zipfile.ZipFile, relative_path: str) -> None:
    source_path = ROOT / relative_path
    if not source_path.is_file():
        raise SystemExit(f"Missing package file: {relative_path}")

    info = zipfile.ZipInfo(relative_path)
    info.date_time = ZIP_TIMESTAMP
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zip_file.writestr(info, source_path.read_bytes())


def _package_files() -> list[str]:
    files: list[str] = []
    seen: set[str] = set()
    for relative_path in STATIC_PACKAGE_FILES:
        files.append(relative_path)
        seen.add(relative_path)

    for source_path in sorted(ROOT.glob("SOUL*.md")):
        relative_path = source_path.relative_to(ROOT).as_posix()
        if relative_path not in seen:
            files.append(relative_path)
            seen.add(relative_path)
    return files


def build(output: Optional[Path] = None) -> Path:
    plugin_id, version = _read_metadata()
    target = output or DIST_DIR / f"{plugin_id}-{version}.zip"
    target.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(target, "w") as zip_file:
        for relative_path in _package_files():
            _write_file(zip_file, relative_path)

    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional output zip path. Defaults to dist/<plugin-id>-<version>.zip.",
    )
    args = parser.parse_args()
    target = build(args.output)
    try:
        print(target.relative_to(ROOT))
    except ValueError:
        print(target)


if __name__ == "__main__":
    main()
