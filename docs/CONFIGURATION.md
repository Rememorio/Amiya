# Configuration

Configuration lives in AstrBot's plugin WebUI. Environment variables with the
same meaning can override WebUI values and are useful for private paths or
allow-lists in service deployments.

## Configure These First

| Field | Default | When to change it |
| --- | --- | --- |
| `soul_file` | `SOUL-Amiya.md` | Change when switching persona. Bundled options: `SOUL-Amiya.md`, `SOUL-Eyjafjalla.md`. |
| `command_prefixes` | `兔兔,Amiya,阿米娅` | Change when you want different trigger names. Use commas. @ this bot also triggers the plugin. |
| `unmatched_policy` | `pass` | Use `silent` when AstrBot has no provider model. Use `codex` only when Codex should handle all non-slash plain text. |
| `workdir` | empty | Set a project directory when Codex should inspect or edit that project. |
| `sandbox` | `read-only` | Change to `workspace-write` only when file edits are needed. |
| `require_admin` | `true` | Controls whether group Codex access is limited to admins and allow-listed users. |
| `allow_users` | empty | Add non-admin sender IDs here, comma-separated. |

## Recipes

### Safe Chat

Use this for first setup.

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

### Eyjafjalla Persona

```text
soul_file=SOUL-Eyjafjalla.md
command_prefixes=艾雅法拉,Eyjafjalla,小羊
sandbox=read-only
require_admin=true
```

### Project Assistant

Use this in trusted small groups or private chats. Confirm read-only behavior
first, then consider write access.

```text
workdir=<project directory>
sandbox=read-only
require_admin=true
allow_users=<trusted sender IDs>
```

When Codex should edit workspace files:

```text
sandbox=workspace-write
```

Avoid `danger-full-access` in group chats.

## All Options

| Config key | Environment variables | Default | Description |
| --- | --- | --- | --- |
| `language` | `ASTRBOT_AMIYA_LANGUAGE`, `AMIYA_LANGUAGE` | `zh-CN` | User-facing language: `zh-CN` or `en-US`. |
| `codex_binary` | `ASTRBOT_AMIYA_CODEX_BINARY`, `AMIYA_CODEX_BINARY` | `codex` | Codex executable name or path. Use a full path if AstrBot cannot find Codex. |
| `workdir` | `ASTRBOT_AMIYA_CODEX_WORKDIR`, `AMIYA_CODEX_WORKDIR` | empty | Codex working directory. Empty means AstrBot process directory. |
| `sandbox` | `ASTRBOT_AMIYA_CODEX_SANDBOX`, `AMIYA_CODEX_SANDBOX` | `read-only` | `read-only`, `workspace-write`, or `danger-full-access`. |
| `timeout_seconds` | `ASTRBOT_AMIYA_CODEX_TIMEOUT_SECONDS`, `AMIYA_CODEX_TIMEOUT_SECONDS` | `120` | Per-request timeout. |
| `max_output_chars` | `ASTRBOT_AMIYA_CODEX_MAX_OUTPUT_CHARS`, `AMIYA_CODEX_MAX_OUTPUT_CHARS` | `3500` | Maximum reply length sent back to chat. |
| `require_admin` | `ASTRBOT_AMIYA_CODEX_REQUIRE_ADMIN`, `AMIYA_CODEX_REQUIRE_ADMIN` | `true` | Restrict group Codex access to admins and allow-listed users. |
| `enable_private` | `ASTRBOT_AMIYA_CODEX_ENABLE_PRIVATE`, `AMIYA_CODEX_ENABLE_DIRECT` | `true` | Allow private-chat access. |
| `allow_users` | `ASTRBOT_AMIYA_CODEX_ALLOW_USERS`, `AMIYA_CODEX_ALLOW_USERS` | empty | Sender IDs that can always call Codex. |
| `model` | `ASTRBOT_AMIYA_CODEX_MODEL`, `AMIYA_CODEX_MODEL` | empty | Optional Codex model override. Empty uses the Codex CLI default. |
| `soul_file` | `ASTRBOT_AMIYA_CODEX_SOUL_FILE`, `AMIYA_CODEX_SOUL_FILE` | `SOUL-Amiya.md` | Persona file. Relative paths resolve from the plugin directory. |
| `strip_thinking` | `ASTRBOT_AMIYA_CODEX_STRIP_THINKING`, `AMIYA_CODEX_STRIP_THINKING` | `true` | Remove common thinking tags before replying. |
| `command_prefixes` | `ASTRBOT_AMIYA_CODEX_COMMAND_PREFIXES`, `AMIYA_CODEX_COMMAND_PREFIXES` | `兔兔,Amiya,阿米娅` | Plain text prefixes that trigger the plugin. @ this bot also triggers it. |
| `unmatched_policy` | `ASTRBOT_AMIYA_CODEX_UNMATCHED_POLICY`, `AMIYA_CODEX_UNMATCHED_POLICY` | `pass` | What to do with non-slash plain text that does not match a prefix: `pass`, `silent`, or `codex`. |
| `log_events` | `ASTRBOT_AMIYA_CODEX_LOG_EVENTS`, `AMIYA_CODEX_LOG_EVENTS` | `true` | Log privacy-safe events without message text, group IDs, or user IDs. |
| `session_enabled` | `ASTRBOT_AMIYA_CODEX_SESSION_ENABLED`, `AMIYA_CODEX_SESSION_ENABLED` | `true` | Use Codex native sessions. When disabled, calls use `--ephemeral`. |
| `session_ttl_minutes` | `ASTRBOT_AMIYA_CODEX_SESSION_TTL_MINUTES`, `AMIYA_CODEX_SESSION_TTL_MINUTES` | `360` | Drop inactive sessions after this many minutes. |
| `session_max_turns` | `ASTRBOT_AMIYA_CODEX_SESSION_MAX_TURNS`, `AMIYA_CODEX_SESSION_MAX_TURNS` | `16` | Reset a chat session after this many Codex turns. |
| `session_max_sessions` | `ASTRBOT_AMIYA_CODEX_SESSION_MAX_SESSIONS`, `AMIYA_CODEX_SESSION_MAX_SESSIONS` | `64` | Maximum active chat sessions retained by the plugin. |
| `session_persist_state` | `ASTRBOT_AMIYA_CODEX_SESSION_PERSIST_STATE`, `AMIYA_CODEX_SESSION_PERSIST_STATE` | `true` | Persist hashed chat keys and Codex thread IDs across AstrBot restarts. |
| `session_cleanup_native_files` | `ASTRBOT_AMIYA_CODEX_SESSION_CLEANUP_NATIVE_FILES`, `AMIYA_CODEX_SESSION_CLEANUP_NATIVE_FILES` | `true` | Try to delete matching Codex session files when sessions expire or reset. |
| `session_state_file` | `ASTRBOT_AMIYA_CODEX_SESSION_STATE_FILE`, `AMIYA_CODEX_SESSION_STATE_FILE` | empty | Optional state file path. Empty uses AstrBot `data/plugin_data`. |

## Commands And Prefixes

The plugin never intercepts AstrBot native slash commands such as `/help` or
`/reset`. Non-slash messages that mention this bot anywhere in the AstrBot
message chain are treated like configured-prefix messages. Other non-slash
messages that do not match `command_prefixes` follow `unmatched_policy`:

| Value | Behavior |
| --- | --- |
| `pass` | Continue the AstrBot pipeline. This preserves native AstrBot chat and other plugins. |
| `silent` | Stop the message without replying. Use this when AstrBot has no provider model and you only want prefixed Codex chat. |
| `codex` | Send all non-slash plain text to Codex. Permission settings still apply. |

| Message | Behavior |
| --- | --- |
| `兔兔 帮助` or `兔兔 help` | Show help. |
| `兔兔 连通测试` or `兔兔 ping` | Confirm the plugin is online. Does not call Codex. |
| `兔兔 状态` or `兔兔 status` | Show runtime status. |
| `兔兔 人格` or `兔兔 soul` | Show persona file loading status. |
| `兔兔 会话状态` or `兔兔 session` | Show current session status. |
| `兔兔 新会话` or `兔兔 reset` | Clear the current chat session. |
| `兔兔 <prompt>` | Call Codex. |
| `@Amiya <prompt>` | Call Codex when the platform delivers an AstrBot mention for this bot. |

Chinese prefixes may be attached directly to the prompt, such as `兔兔状态`.
ASCII prefixes are case-insensitive, but `AmiyaBot` is not treated as the
`Amiya` prefix. `@all` and mentions of other users do not count as mentioning
this bot.

## Persona Files

`soul_file` is read as UTF-8 text. Relative paths resolve from the plugin
directory.

Loading order:

1. Environment-variable `soul_file`.
2. AstrBot plugin WebUI `soul_file`.
3. `SOUL.md`.
4. Built-in minimal fallback persona.

Persona text is sent to Codex on every request. Do not put credentials, account
IDs, or local machine paths in persona files.

## Session Memory

When `session_enabled=true`, the plugin uses Codex native sessions and resumes
them by thread ID. Local state stores only a salt, hashed chat keys, and Codex
thread IDs; it does not store group IDs, user IDs, or message text.

For a clean request every time:

```text
session_enabled=false
```

The plugin then calls `codex exec --ephemeral`.

## Security Boundaries

- Default `sandbox=read-only`.
- The plugin always passes `approval_policy="never"` to Codex CLI.
- Replies and errors redact local filesystem paths where practical.
- Group chat messages are treated as untrusted input.
- Do not commit real user IDs, tokens, private paths, or local runtime config to
  this public repository.
