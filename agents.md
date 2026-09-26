# agents.md

Instructions for ALL coding agents (Claude Code, Copilot, Codex, Cursor, etc.) working in
this repo. Claude-specific notes live in [CLAUDE.md](CLAUDE.md); this file and that one
reference each other and must stay consistent.

## Non-negotiables

### Windows console visibility — mandatory

User-confirmed 2026-09-26. This rule applies to every agent and delegated task in this repository.

- Run command-line work without opening, flashing, focusing, or raising a console or application window on the user's desktop. Foreground execution requires an explicit user request for that exact visible application.
- Prefer file-access and connector tools that launch no local processes.
- Before launching, account for the entire process chain: the tool host, shell, wrappers, application, and child processes. This includes PowerShell, cmd, terminal hosts, Python, Git, gh, AWS CLI, and OpenSCAD.
- Use only a launch path already verified to keep the entire process chain off the interactive desktop. Captured output, non-TTY mode, CREATE_NO_WINDOW, WindowStyle Hidden, pythonw, or a separate desktop alone is not proof that the parent tool host stays hidden.
- Do not test an uncertain launcher on the user's desktop. If a window appears, stop that batch and do not reuse the launch path. Hiding or minimizing it afterward does not satisfy this rule.
- If hidden execution cannot be guaranteed, stop the process-dependent steps. Continue through file-only tools where possible and report the limit. Commit, push, build, deployment, and email requirements do not override this rule.
- Include this rule in every delegated task that could launch local processes. The parent agent remains responsible.

### Repository delivery and credentials

1. **Read [deploy.md](deploy.md) first.** It is the authoritative guide for deployment
   (GitHub Actions + OIDC via `vars.AWS_DEPLOY_ROLE_ARN`), stack standards (tags, arm64,
   no secrets managers, no DynamoDB Scan on serving paths), and verification.
2. **Never deploy from a local machine.** Deploys happen only by pushing to `main`.
3. **Never handle credential values.** Do not ask the user to paste a secret into the
   conversation, do not print/echo/commit one. To add or update a secret, run
   `./scripts/set-secret.sh NAME` — the user types the value into a hidden terminal
   prompt and the script pushes it to GitHub. Non-secret config goes in GitHub
   variables (`gh variable set`).
4. **Never add static AWS keys** (`aws-access-key-id`, `AWS_ACCESS_KEY_ID` env, IAM user
   keys) anywhere. OIDC only.
5. Work on `main`, push after committing, and watch the triggered run to confirm the
   deploy is green before declaring success.
