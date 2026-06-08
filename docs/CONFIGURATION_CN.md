# 配置说明

配置可以在 AstrBot 插件 WebUI 中设置。启动进程时提供的环境变量可以覆盖同名含义
的配置项。

## 配置项

| 配置键 | 环境变量 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `language` | `ASTRBOT_AMIYA_LANGUAGE`, `AMIYA_LANGUAGE` | `zh-CN` | 用户可见语言，支持 `zh-CN`、`en-US`。 |
| `codex_binary` | `ASTRBOT_AMIYA_CODEX_BINARY`, `AMIYA_CODEX_BINARY` | `codex` | Codex 可执行文件名或路径。 |
| `workdir` | `ASTRBOT_AMIYA_CODEX_WORKDIR`, `AMIYA_CODEX_WORKDIR` | 空 | Codex 工作目录。留空表示 AstrBot 进程目录。 |
| `sandbox` | `ASTRBOT_AMIYA_CODEX_SANDBOX`, `AMIYA_CODEX_SANDBOX` | `read-only` | Codex 沙箱：`read-only`、`workspace-write`、`danger-full-access`。 |
| `timeout_seconds` | `ASTRBOT_AMIYA_CODEX_TIMEOUT_SECONDS`, `AMIYA_CODEX_TIMEOUT_SECONDS` | `120` | 单次请求超时时间。 |
| `max_output_chars` | `ASTRBOT_AMIYA_CODEX_MAX_OUTPUT_CHARS`, `AMIYA_CODEX_MAX_OUTPUT_CHARS` | `3500` | 回复到聊天平台的最大字符数。 |
| `require_admin` | `ASTRBOT_AMIYA_CODEX_REQUIRE_ADMIN`, `AMIYA_CODEX_REQUIRE_ADMIN` | `true` | 群聊中仅管理员和白名单用户可调用 Codex。 |
| `enable_private` | `ASTRBOT_AMIYA_CODEX_ENABLE_PRIVATE`, `AMIYA_CODEX_ENABLE_DIRECT` | `true` | 是否允许私聊调用 Codex。 |
| `allow_users` | `ASTRBOT_AMIYA_CODEX_ALLOW_USERS`, `AMIYA_CODEX_ALLOW_USERS` | 空 | 总是允许调用 Codex 的发送者 ID，多个值用英文逗号分隔。 |
| `model` | `ASTRBOT_AMIYA_CODEX_MODEL`, `AMIYA_CODEX_MODEL` | 空 | 可选 Codex 模型覆盖。留空表示使用 Codex CLI 默认模型。 |
| `soul_file` | `ASTRBOT_AMIYA_CODEX_SOUL_FILE`, `AMIYA_CODEX_SOUL_FILE` | `SOUL-Amiya.md` | 人格文件。相对路径从插件目录解析。 |
| `strip_thinking` | `ASTRBOT_AMIYA_CODEX_STRIP_THINKING`, `AMIYA_CODEX_STRIP_THINKING` | `true` | 回复前移除常见思考标签。 |
| `command_prefixes` | `ASTRBOT_AMIYA_CODEX_COMMAND_PREFIXES`, `AMIYA_CODEX_COMMAND_PREFIXES` | `兔兔,Amiya,阿米娅` | 触发插件的普通文本前缀，多个值用英文逗号分隔。 |
| `log_events` | `ASTRBOT_AMIYA_CODEX_LOG_EVENTS`, `AMIYA_CODEX_LOG_EVENTS` | `true` | 记录隐私安全的插件事件，不包含消息正文、群号或用户号。 |
| `session_enabled` | `ASTRBOT_AMIYA_CODEX_SESSION_ENABLED`, `AMIYA_CODEX_SESSION_ENABLED` | `true` | 使用 Codex 原生 session，并通过 thread id 恢复。关闭后使用 `--ephemeral`。 |
| `session_ttl_minutes` | `ASTRBOT_AMIYA_CODEX_SESSION_TTL_MINUTES`, `AMIYA_CODEX_SESSION_TTL_MINUTES` | `360` | 原生会话多久未活跃后自动丢弃，单位分钟。 |
| `session_max_turns` | `ASTRBOT_AMIYA_CODEX_SESSION_MAX_TURNS`, `AMIYA_CODEX_SESSION_MAX_TURNS` | `16` | 单个聊天达到多少轮 Codex 调用后自动重置。 |
| `session_max_sessions` | `ASTRBOT_AMIYA_CODEX_SESSION_MAX_SESSIONS`, `AMIYA_CODEX_SESSION_MAX_SESSIONS` | `64` | 进程内最多保留多少个活跃聊天会话，超出后淘汰最旧会话。 |
| `session_persist_state` | `ASTRBOT_AMIYA_CODEX_SESSION_PERSIST_STATE`, `AMIYA_CODEX_SESSION_PERSIST_STATE` | `true` | 跨 AstrBot 重启保存哈希后的聊天 key 和 Codex thread id。 |
| `session_cleanup_native_files` | `ASTRBOT_AMIYA_CODEX_SESSION_CLEANUP_NATIVE_FILES`, `AMIYA_CODEX_SESSION_CLEANUP_NATIVE_FILES` | `true` | 会话过期或重置时，尽量删除匹配的 Codex session 文件。 |
| `session_state_file` | `ASTRBOT_AMIYA_CODEX_SESSION_STATE_FILE`, `AMIYA_CODEX_SESSION_STATE_FILE` | 空 | 可选会话索引文件路径。留空时使用 AstrBot `data/plugin_data`。 |

环境变量适合保存私有运行时配置。不要把真实账号 ID 或敏感本机路径提交到这个
公开仓库。

## 命令

插件监听非 `/` 开头的普通文本消息，然后只处理命中 `command_prefixes` 的消息。
未命中前缀的消息会直接交还给 AstrBot 后续流程；`/help`、`/reset` 等 AstrBot
原生斜杠命令不会被本插件拦截。下面示例使用 `兔兔`。

| 消息 | 行为 |
| --- | --- |
| `兔兔 帮助` 或 `兔兔 help` | 查看帮助。 |
| `兔兔 连通测试` 或 `兔兔 ping` | 确认插件已加载，不调用 Codex。 |
| `兔兔 状态` 或 `兔兔 status` | 查看安全处理后的运行状态。 |
| `兔兔 人格` 或 `兔兔 soul` | 查看人格文件加载状态。 |
| `兔兔 会话状态` 或 `兔兔 session` | 查看当前聊天的会话记忆状态。 |
| `兔兔 新会话` 或 `兔兔 reset` | 清空当前聊天的会话记忆。 |
| `兔兔 <问题>` | 把问题交给 Codex，并把最终回答发回聊天平台。 |

`帮助` 和 `连通测试` 是轻量命令。`状态`、`人格`、会话状态、会话重置和 Codex
聊天会遵守权限配置。

`command_prefixes` 会在运行时生效。中文前缀可以直接连着正文，例如
`兔兔状态`；ASCII 前缀大小写不敏感，但会避免把 `AmiyaBot` 误判成 `Amiya`。
如果使用 `SOUL-Eyjafjalla.md`，可以把前缀配置为
`艾雅法拉,Eyjafjalla,小羊`。

## 人格文件

`soul_file` 会按 UTF-8 文本读取，并在每次请求中作为人格提示传给 Codex。AstrBot
配置 schema 默认显示 `SOUL-Amiya.md`；仓库也内置了 `SOUL-Eyjafjalla.md`。没有
配置对象时，代码级回退是 `SOUL.md`。如果配置文件无法读取，插件会尝试
`SOUL.md`；如果两者都不存在，会使用一个很小的内置默认人格。

人格文件不要写入密钥。人格文本会在每次请求时发送给 Codex。

## 会话记忆

`session_enabled` 开启时，插件会创建 Codex 原生 session，并通过
`codex exec resume <thread_id>` 恢复上下文。本地 state 文件只保存 salt、
哈希后的聊天 key 和 Codex thread id；不会保存群号、用户号或消息正文。

默认限制是保守的：`session_ttl_minutes` 用于清理长期不活跃会话，
`session_max_turns` 用于重置过长聊天，`session_max_sessions` 在活跃聊天过多
时淘汰最旧会话。`session_cleanup_native_files` 开启时，插件还会在会话过期或
重置时尽量删除匹配的 Codex session 文件。

`session_enabled` 关闭时，插件回退到 `codex exec --ephemeral`，不保存 Codex
原生会话。

## 安全模型

- 默认沙箱为 `read-only`。
- 插件调用 Codex CLI 时传入 `approval_policy="never"`。
- 回复和状态消息会尽量脱敏本机文件路径。
- 发送给 Codex 的提示中不会包含群号或用户号。
- 插件事件日志不会记录消息正文、群号或用户号。
- Codex 原生会话受过期时间、轮数和活跃会话数限制。
- 关闭会话记忆后恢复为完全 ephemeral 的 Codex 调用。

仅在可信群和可信操作者场景下使用 `workspace-write`。只有在明确接受风险的受控
环境中才使用 `danger-full-access`。

## 故障排查

- 提示找不到 Codex：配置 `codex_binary`，或修正 AstrBot 进程环境。
- 请求超时：增大 `timeout_seconds`，或把问题拆小。
- 权限不足：将可信用户加入 `allow_users`、关闭 `require_admin`，或使用群管理员
  账号执行。
- 聊天中没有回复：先确认平台适配器连接、插件状态和 AstrBot 日志。
