# Amiya Codex Chat

Amiya Codex Chat 是一个 AstrBot 插件，用于把带前缀的聊天消息转发给
Codex CLI，并把最终结果回复回聊天平台。它的目标是保持轻量、可配置、适合公开
发布：人格由 `SOUL` 文件定义；Codex 默认使用保守沙箱；开启会话后，插件会使用
Codex 原生 session 并通过 thread id 恢复上下文。

本仓库是公开仓库。请不要提交账号 ID、令牌、私有路径或本机专属配置。

[English README](README.md)

## 功能

- 使用 AstrBot Star 插件布局，包含 `main.py`、`metadata.yaml`、
  `_conf_schema.json` 和 WebUI i18n 资源。
- 支持 AstrBot 的 OneBot、QQ 官方、Telegram、Discord、Slack、Kook、企业微信、
  Lark、DingTalk、Satori 等平台适配器。
- 人格文件可配置。仓库默认使用 `SOUL-Amiya.md`，并内置
  `SOUL-Eyjafjalla.md` 作为可选示例；通用回退文件名为 `SOUL.md`。
- 用户可见回复支持 `zh-CN` 和 `en-US`。
- 内置命令：帮助、连通测试、运行状态、人格状态、会话状态、会话重置和 Codex 聊天。
- 兼容 AstrBot 原生 `/` 斜杠命令。插件只处理配置前缀命中的普通文本消息。
- Codex 原生 session 恢复，支持过期时间、轮数、活跃会话数和清理策略。
- 记录隐私安全的运行日志，不包含消息正文或账号 ID。
- 默认安全策略保守：Codex 使用 `read-only` 沙箱，群聊里仅管理员和白名单用户
  可以调用 Codex。
- 关闭会话记忆时使用 `codex exec --ephemeral`。

## 运行要求

- 已安装并能正常运行的官方 AstrBot。
- 已配置可用的 AstrBot 平台适配器。
- 运行 AstrBot 的机器上已安装并登录 Codex CLI。
- AstrBot 所在 Python 环境能从进程环境中执行 `codex`。

## 快速开始

构建插件 zip：

```bash
python scripts/package.py
```

通过 AstrBot 插件管理器安装 `dist/` 中生成的 zip，或者把本仓库放到 AstrBot 的
`data/plugins` 目录作为本地插件。在 AstrBot 插件配置中，可以保留默认人格文件
`SOUL-Amiya.md`，也可以把 `soul_file` 指向 `SOUL-Eyjafjalla.md` 或你自己的文件。

下面示例使用默认插件前缀：

```text
兔兔 帮助
兔兔 连通测试
兔兔 状态
兔兔 人格
兔兔 会话状态
兔兔 新会话
兔兔 介绍一下你自己
```

如果切换到艾雅法拉人格，可以同时把 `command_prefixes` 改成类似
`艾雅法拉,Eyjafjalla,小羊`。

## 文档

- [安装指南](docs/INSTALL_CN.md)
- [配置说明](docs/CONFIGURATION_CN.md)
- [Installation](docs/INSTALL.md)
- [Configuration](docs/CONFIGURATION.md)

## 安全建议

除非明确需要让机器人改文件，否则保持 `read-only` 沙箱。群聊场景建议保持
`require_admin` 开启，只把可信操作者加入 `allow_users`。不要在人格文件、
文档、提交信息或 issue 中写入密钥、账号标识、真实本机路径等敏感信息。

## 许可证

MIT
