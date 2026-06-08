# Security Policy

## Supported Versions

Security fixes target the current `main` branch.

## Reporting a Vulnerability

If you find a vulnerability, please use the repository owner's private security
contact or GitHub's private vulnerability reporting when available. Do not post
tokens, account IDs, private paths, or exploitable details in a public issue.

## Operational Guidance

- Keep `sandbox` set to `read-only` unless write access is required.
- Keep `require_admin` enabled for group chats.
- Use `allow_users` only for trusted operators.
- Treat chat messages as untrusted input.
- Do not store credentials in `SOUL` files, docs, examples, or plugin config
  committed to this repository.
- Review AstrBot and Codex CLI logs before sharing them publicly.
