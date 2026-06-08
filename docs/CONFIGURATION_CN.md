# 配置说明

配置入口在 AstrBot WebUI 的插件配置页。环境变量可以覆盖同名含义的配置项，适合
服务部署时放私有路径或用户白名单。

## 先配这些字段

| 字段 | 默认值 | 什么时候改 |
| --- | --- | --- |
| `soul_file` | `SOUL-Amiya.md` | 切换人格时改。仓库内置 `SOUL-Amiya.md` 和 `SOUL-Eyjafjalla.md`。 |
| `command_prefixes` | `兔兔,Amiya,阿米娅` | 想换触发词时改。多个前缀用英文逗号分隔。 |
| `unmatched_policy` | `pass` | AstrBot 没配 provider 模型时用 `silent`；只有想让 Codex 接管所有非斜杠普通文本时才用 `codex`。 |
| `workdir` | 空 | 想让 Codex 在某个项目里回答或改文件时填项目目录。 |
| `sandbox` | `read-only` | 需要写文件时才改成 `workspace-write`。 |
| `require_admin` | `true` | 群聊是否只允许管理员和白名单用户调用 Codex。 |
| `allow_users` | 空 | 给非管理员授权时填发送者 ID，多个用英文逗号分隔。 |

## 推荐模板

### 默认安全聊天

适合刚安装时验证。

```text
soul_file=SOUL-Amiya.md
command_prefixes=兔兔,Amiya,阿米娅
unmatched_policy=pass
workdir=
sandbox=read-only
require_admin=true
allow_users=
session_enabled=true
```

### 艾雅法拉人格

```text
soul_file=SOUL-Eyjafjalla.md
command_prefixes=艾雅法拉,Eyjafjalla,小羊
sandbox=read-only
require_admin=true
```

### 项目助手

适合可信小群或私聊，让 Codex 读取一个项目。先用只读确认，再考虑写权限。

```text
workdir=<项目目录>
sandbox=read-only
require_admin=true
allow_users=<可信发送者 ID>
```

需要 Codex 修改工作区文件时：

```text
sandbox=workspace-write
```

不建议在群聊里使用 `danger-full-access`。

## 所有配置项

| 配置键 | 环境变量 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `language` | `ASTRBOT_AMIYA_LANGUAGE`, `AMIYA_LANGUAGE` | `zh-CN` | 用户可见语言，支持 `zh-CN`、`en-US`。 |
| `codex_binary` | `ASTRBOT_AMIYA_CODEX_BINARY`, `AMIYA_CODEX_BINARY` | `codex` | Codex 可执行文件名或路径。AstrBot 找不到 Codex 时填完整路径。 |
| `workdir` | `ASTRBOT_AMIYA_CODEX_WORKDIR`, `AMIYA_CODEX_WORKDIR` | 空 | Codex 工作目录。留空表示 AstrBot 进程目录。 |
| `sandbox` | `ASTRBOT_AMIYA_CODEX_SANDBOX`, `AMIYA_CODEX_SANDBOX` | `read-only` | `read-only`、`workspace-write` 或 `danger-full-access`。 |
| `timeout_seconds` | `ASTRBOT_AMIYA_CODEX_TIMEOUT_SECONDS`, `AMIYA_CODEX_TIMEOUT_SECONDS` | `120` | 单次 Codex 请求的最长等待秒数。 |
| `max_output_chars` | `ASTRBOT_AMIYA_CODEX_MAX_OUTPUT_CHARS`, `AMIYA_CODEX_MAX_OUTPUT_CHARS` | `3500` | 回复到聊天平台的最大字符数。 |
| `require_admin` | `ASTRBOT_AMIYA_CODEX_REQUIRE_ADMIN`, `AMIYA_CODEX_REQUIRE_ADMIN` | `true` | 群聊中仅管理员和白名单用户可调用 Codex。 |
| `enable_private` | `ASTRBOT_AMIYA_CODEX_ENABLE_PRIVATE`, `AMIYA_CODEX_ENABLE_DIRECT` | `true` | 是否允许私聊调用。 |
| `allow_users` | `ASTRBOT_AMIYA_CODEX_ALLOW_USERS`, `AMIYA_CODEX_ALLOW_USERS` | 空 | 始终允许调用 Codex 的发送者 ID。 |
| `model` | `ASTRBOT_AMIYA_CODEX_MODEL`, `AMIYA_CODEX_MODEL` | 空 | 可选 Codex 模型覆盖。留空使用 Codex CLI 默认模型。 |
| `soul_file` | `ASTRBOT_AMIYA_CODEX_SOUL_FILE`, `AMIYA_CODEX_SOUL_FILE` | `SOUL-Amiya.md` | 人格文件。相对路径从插件目录解析。 |
| `strip_thinking` | `ASTRBOT_AMIYA_CODEX_STRIP_THINKING`, `AMIYA_CODEX_STRIP_THINKING` | `true` | 回复前移除常见思考标签。 |
| `command_prefixes` | `ASTRBOT_AMIYA_CODEX_COMMAND_PREFIXES`, `AMIYA_CODEX_COMMAND_PREFIXES` | `兔兔,Amiya,阿米娅` | 触发插件的普通文本前缀。 |
| `unmatched_policy` | `ASTRBOT_AMIYA_CODEX_UNMATCHED_POLICY`, `AMIYA_CODEX_UNMATCHED_POLICY` | `pass` | 未命中前缀的非斜杠普通文本如何处理：`pass`、`silent` 或 `codex`。 |
| `log_events` | `ASTRBOT_AMIYA_CODEX_LOG_EVENTS`, `AMIYA_CODEX_LOG_EVENTS` | `true` | 记录隐私安全的插件事件，不包含消息正文、群号或用户号。 |
| `session_enabled` | `ASTRBOT_AMIYA_CODEX_SESSION_ENABLED`, `AMIYA_CODEX_SESSION_ENABLED` | `true` | 使用 Codex 原生 session。关闭后使用 `--ephemeral`。 |
| `session_ttl_minutes` | `ASTRBOT_AMIYA_CODEX_SESSION_TTL_MINUTES`, `AMIYA_CODEX_SESSION_TTL_MINUTES` | `360` | 会话多久未活跃后自动丢弃。 |
| `session_max_turns` | `ASTRBOT_AMIYA_CODEX_SESSION_MAX_TURNS`, `AMIYA_CODEX_SESSION_MAX_TURNS` | `16` | 单个聊天达到多少轮 Codex 调用后自动重置。 |
| `session_max_sessions` | `ASTRBOT_AMIYA_CODEX_SESSION_MAX_SESSIONS`, `AMIYA_CODEX_SESSION_MAX_SESSIONS` | `64` | 最多保留多少个活跃聊天会话。 |
| `session_persist_state` | `ASTRBOT_AMIYA_CODEX_SESSION_PERSIST_STATE`, `AMIYA_CODEX_SESSION_PERSIST_STATE` | `true` | 跨 AstrBot 重启保存哈希后的聊天 key 和 Codex thread id。 |
| `session_cleanup_native_files` | `ASTRBOT_AMIYA_CODEX_SESSION_CLEANUP_NATIVE_FILES`, `AMIYA_CODEX_SESSION_CLEANUP_NATIVE_FILES` | `true` | 会话过期或重置时，尽量删除匹配的 Codex session 文件。 |
| `session_state_file` | `ASTRBOT_AMIYA_CODEX_SESSION_STATE_FILE`, `AMIYA_CODEX_SESSION_STATE_FILE` | 空 | 可选会话索引文件路径。留空时使用 AstrBot `data/plugin_data`。 |

## 命令和前缀

插件永远不会拦截 `/help`、`/reset` 等 AstrBot 原生斜杠命令。未命中
`command_prefixes` 的非斜杠普通文本由 `unmatched_policy` 决定：

| 值 | 行为 |
| --- | --- |
| `pass` | 继续交给 AstrBot 流水线，兼容 AstrBot 原生聊天和其他插件。 |
| `silent` | 静默拦截，不回复。AstrBot 没配 provider 模型、只想用前缀 Codex 聊天时使用。 |
| `codex` | 所有非斜杠普通文本都交给 Codex，权限配置仍然生效。 |

| 消息 | 行为 |
| --- | --- |
| `兔兔 帮助` 或 `兔兔 help` | 查看帮助。 |
| `兔兔 连通测试` 或 `兔兔 ping` | 确认插件在线，不调用 Codex。 |
| `兔兔 状态` 或 `兔兔 status` | 查看运行状态。 |
| `兔兔 人格` 或 `兔兔 soul` | 查看人格文件加载状态。 |
| `兔兔 会话状态` 或 `兔兔 session` | 查看当前聊天的会话状态。 |
| `兔兔 新会话` 或 `兔兔 reset` | 清空当前聊天会话。 |
| `兔兔 <问题>` | 调用 Codex。 |

中文前缀可以直接连正文，例如 `兔兔状态`。ASCII 前缀大小写不敏感，但不会把
`AmiyaBot` 误判成 `Amiya`。

## 人格文件

`soul_file` 会按 UTF-8 文本读取。相对路径从插件目录解析。

加载顺序：

1. 环境变量里的 `soul_file`。
2. AstrBot 插件配置里的 `soul_file`。
3. `SOUL.md`。
4. 内置最小默认人格。

人格文本会在每次请求时发送给 Codex，不要写入密钥、账号 ID 或本机路径。

## 会话记忆

`session_enabled=true` 时，插件使用 Codex 原生 session，并用 thread id 恢复上下文。
本地状态文件只保存 salt、哈希后的聊天 key 和 Codex thread id；不保存群号、用户号
或消息正文。

如果你希望每次都是干净请求：

```text
session_enabled=false
```

此时插件会调用 `codex exec --ephemeral`。

## 安全边界

- 默认 `sandbox=read-only`。
- 插件调用 Codex CLI 时固定传入 `approval_policy="never"`。
- 回复和错误会尽量脱敏本机文件路径。
- 群聊消息被视为不可信输入。
- 公开仓库不要提交真实用户 ID、token、私有路径或本地运行配置。
