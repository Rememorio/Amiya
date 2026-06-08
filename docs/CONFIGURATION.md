# Configuration

Configuration is managed in AstrBot's plugin WebUI. Environment variables with
the same meaning can override values at process start.

## Options

| Config key | Environment variables | Default | Description |
| --- | --- | --- | --- |
| `language` | `ASTRBOT_AMIYA_LANGUAGE`, `AMIYA_LANGUAGE` | `zh-CN` | User-facing language. Supported values: `zh-CN`, `en-US`. |
| `codex_binary` | `ASTRBOT_AMIYA_CODEX_BINARY`, `AMIYA_CODEX_BINARY` | `codex` | Codex executable name or path. |
| `workdir` | `ASTRBOT_AMIYA_CODEX_WORKDIR`, `AMIYA_CODEX_WORKDIR` | empty | Codex working directory. Empty means AstrBot process directory. |
| `sandbox` | `ASTRBOT_AMIYA_CODEX_SANDBOX`, `AMIYA_CODEX_SANDBOX` | `read-only` | Codex sandbox: `read-only`, `workspace-write`, or `danger-full-access`. |
| `timeout_seconds` | `ASTRBOT_AMIYA_CODEX_TIMEOUT_SECONDS`, `AMIYA_CODEX_TIMEOUT_SECONDS` | `120` | Per-request timeout. |
| `max_output_chars` | `ASTRBOT_AMIYA_CODEX_MAX_OUTPUT_CHARS`, `AMIYA_CODEX_MAX_OUTPUT_CHARS` | `3500` | Maximum reply length sent back to chat. |
| `require_admin` | `ASTRBOT_AMIYA_CODEX_REQUIRE_ADMIN`, `AMIYA_CODEX_REQUIRE_ADMIN` | `true` | Restrict group Codex access to admins and allow-listed users. |
| `enable_private` | `ASTRBOT_AMIYA_CODEX_ENABLE_PRIVATE`, `AMIYA_CODEX_ENABLE_DIRECT` | `true` | Allow private-chat Codex access. |
| `allow_users` | `ASTRBOT_AMIYA_CODEX_ALLOW_USERS`, `AMIYA_CODEX_ALLOW_USERS` | empty | Comma-separated sender IDs that can always call Codex. |
| `model` | `ASTRBOT_AMIYA_CODEX_MODEL`, `AMIYA_CODEX_MODEL` | empty | Optional Codex model override. Empty uses the Codex CLI default. |
| `soul_file` | `ASTRBOT_AMIYA_CODEX_SOUL_FILE`, `AMIYA_CODEX_SOUL_FILE` | `SOUL-Amiya.md` | Persona file. Relative paths resolve from the plugin directory. |
| `strip_thinking` | `ASTRBOT_AMIYA_CODEX_STRIP_THINKING`, `AMIYA_CODEX_STRIP_THINKING` | `true` | Remove common thinking tags before replying. |
| `command_prefixes` | `ASTRBOT_AMIYA_CODEX_COMMAND_PREFIXES`, `AMIYA_CODEX_COMMAND_PREFIXES` | `兔兔,Amiya,阿米娅` | Comma-separated plain-text prefixes that trigger the plugin. |
| `log_events` | `ASTRBOT_AMIYA_CODEX_LOG_EVENTS`, `AMIYA_CODEX_LOG_EVENTS` | `true` | Log privacy-safe plugin events without message text or account IDs. |
| `session_enabled` | `ASTRBOT_AMIYA_CODEX_SESSION_ENABLED`, `AMIYA_CODEX_SESSION_ENABLED` | `true` | Use Codex native sessions and resume by thread id. When disabled, calls use `--ephemeral`. |
| `session_ttl_minutes` | `ASTRBOT_AMIYA_CODEX_SESSION_TTL_MINUTES`, `AMIYA_CODEX_SESSION_TTL_MINUTES` | `360` | Drop inactive native sessions after this many minutes. |
| `session_max_turns` | `ASTRBOT_AMIYA_CODEX_SESSION_MAX_TURNS`, `AMIYA_CODEX_SESSION_MAX_TURNS` | `16` | Reset a chat session after this many Codex turns. |
| `session_max_sessions` | `ASTRBOT_AMIYA_CODEX_SESSION_MAX_SESSIONS`, `AMIYA_CODEX_SESSION_MAX_SESSIONS` | `64` | Maximum active chats before oldest sessions are evicted. |
| `session_persist_state` | `ASTRBOT_AMIYA_CODEX_SESSION_PERSIST_STATE`, `AMIYA_CODEX_SESSION_PERSIST_STATE` | `true` | Persist hashed chat keys and Codex thread ids across AstrBot restarts. |
| `session_cleanup_native_files` | `ASTRBOT_AMIYA_CODEX_SESSION_CLEANUP_NATIVE_FILES`, `AMIYA_CODEX_SESSION_CLEANUP_NATIVE_FILES` | `true` | Delete matching Codex session files when a plugin session expires or resets. |
| `session_state_file` | `ASTRBOT_AMIYA_CODEX_SESSION_STATE_FILE`, `AMIYA_CODEX_SESSION_STATE_FILE` | empty | Optional state file path. Empty uses AstrBot `data/plugin_data`. |

Environment variables are useful for private runtime settings. Do not commit
real account IDs or sensitive local paths to this repository.

## Commands

The plugin observes non-`/` plain text messages and only handles messages whose
prefix matches `command_prefixes`. Messages without a configured prefix are
passed back to AstrBot's later pipeline stages, and native AstrBot slash commands
such as `/help` or `/reset` are not intercepted. The examples assume `兔兔`.

| Message | Behavior |
| --- | --- |
| `兔兔 帮助` or `兔兔 help` | Show help. |
| `兔兔 连通测试` or `兔兔 ping` | Confirm the plugin is loaded. Does not call Codex. |
| `兔兔 状态` or `兔兔 status` | Show safe runtime status. |
| `兔兔 人格` or `兔兔 soul` | Show persona file loading status. |
| `兔兔 会话状态` or `兔兔 session` | Show current chat session memory status. |
| `兔兔 新会话` or `兔兔 reset` | Clear current chat session memory. |
| `兔兔 <prompt>` | Send the prompt to Codex and reply with the final answer. |

`help` and `ping` are intentionally lightweight. `status`, `soul`, session
status, session reset, and Codex chat respect the access-control settings.

`command_prefixes` takes effect at runtime. Chinese prefixes may be attached
directly to the prompt, such as `兔兔状态`. ASCII prefixes are case-insensitive,
but the parser avoids treating `AmiyaBot` as the `Amiya` prefix. When using the
`SOUL-Eyjafjalla.md` persona, a prefix setting such as
`艾雅法拉,Eyjafjalla,小羊` works well.

## Persona Files

The configured `soul_file` is read as UTF-8 text and prepended to each Codex
request. AstrBot's configuration schema defaults to `SOUL-Amiya.md`, and the
repository also bundles `SOUL-Eyjafjalla.md`. The code-level fallback without a
configuration object is `SOUL.md`. If the configured file cannot be loaded, the
plugin tries `SOUL.md`; if neither exists, it uses a small built-in fallback
persona.

Keep persona files free of secrets. Persona text is sent to Codex on every
request.

## Session Memory

When `session_enabled` is true, the plugin creates Codex native sessions and
resumes them with `codex exec resume <thread_id>`. The local state file stores a
salt and hashed chat keys, plus Codex thread ids; it does not store group IDs,
user IDs, or message text.

The limits are intentionally conservative. `session_ttl_minutes` removes stale
sessions, `session_max_turns` resets very long chats, and
`session_max_sessions` evicts the oldest active chats when the process has too
many sessions. When `session_cleanup_native_files` is true, the plugin also
tries to delete matching Codex session files for sessions it evicts or resets.

When `session_enabled` is false, the plugin falls back to
`codex exec --ephemeral` and does not persist Codex native sessions.

## Safety Model

- The default sandbox is `read-only`.
- The plugin passes `approval_policy="never"` to Codex CLI.
- Replies and status messages redact local filesystem paths where practical.
- Chat group IDs and user IDs are not included in the prompt sent to Codex.
- Plugin event logs avoid message text, group IDs, and user IDs.
- Native Codex sessions are bounded by TTL, turn count, and active-chat limits.
- Disabling session memory restores fully ephemeral Codex calls.

Use `workspace-write` only for trusted groups and operators. Use
`danger-full-access` only in a controlled environment where that risk is
intentional.

## Troubleshooting

- `Codex CLI was not found`: configure `codex_binary` or fix AstrBot's process
  environment.
- Timeout: increase `timeout_seconds` or ask a smaller question.
- Permission denied: add a trusted user to `allow_users`, disable
  `require_admin`, or run the command as a group admin.
- No response in chat: verify the platform adapter connection, plugin status,
  and AstrBot logs.
