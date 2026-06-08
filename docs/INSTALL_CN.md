# 安装指南

本文假设你已经运行了 AstrBot，并且已经配置好可用的平台适配器。本插件不会替代
AstrBot 或适配器，只是在 AstrBot 里增加一个调用 Codex 的聊天处理器。

## 1. 准备 Codex CLI

请按照 Codex 官方文档为你的平台安装并登录 Codex CLI。在运行 AstrBot 的机器上
确认以下命令可用：

```bash
codex --version
codex exec --help
```

如果 AstrBot 由服务管理器启动，需要确保服务进程也能找到并执行 `codex`。

## 2. 构建插件 zip

在本仓库目录执行：

```bash
python scripts/package.py
```

产物会写入 `dist/astrbot_plugin_amiya_codex-<version>.zip`。zip 根目录包含
`main.py`、`metadata.yaml`、`_conf_schema.json`、插件 i18n 资源、文档和内置的
`SOUL*.md` 人格文件。

## 3. 安装到 AstrBot

可选择任一方式安装：

- 通过 AstrBot 插件管理器上传或安装生成的 zip。
- 把本仓库放到 AstrBot 的 `data/plugins` 目录作为本地插件，然后重启 AstrBot 或在
  WebUI 中重载插件。

安装后，打开 AstrBot 插件配置页，确认 `Amiya Codex Chat` 已列出。按需配置
`soul_file`、`sandbox`、`require_admin` 等选项。

仓库内置 `SOUL-Amiya.md` 和 `SOUL-Eyjafjalla.md`，插件配置默认指向
`SOUL-Amiya.md`。如果要使用自定义人格文件，可以把文件放在插件目录中，也可以
通过私有运行时配置指定路径。

## 4. 在聊天中验证

下面示例使用默认插件前缀：

```text
兔兔 连通测试
兔兔 帮助
兔兔 介绍一下你自己
```

前两个命令不会调用 Codex；最后一个命令会启动一次 Codex 调用。

## 升级

重新构建 zip，通过 AstrBot 插件管理器安装，然后重载插件。运行时配置由 AstrBot
管理，不应写入这个公开仓库。
