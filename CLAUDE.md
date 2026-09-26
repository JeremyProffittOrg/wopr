# CLAUDE.md

Read **[deploy.md](deploy.md)** before any infrastructure, workflow, or credential work —
it defines the only allowed deployment path (GitHub Actions + OIDC, no local deploys, no
static AWS keys) and the credential policy (agents never see secret values; use
`scripts/set-secret.sh`).

Agent configuration is shared with [agents.md](agents.md); keep the two consistent.
Before any local process launch, follow the mandatory Windows console visibility rule
in [agents.md](agents.md). It also applies to delegated work and delivery commands.

- Commit and push directly to `main` (no feature branches or PRs unless asked).
- Pushing to `main` IS the deploy trigger — treat every push as a production deploy.
- No stubs or placeholder implementations; ask when blocked.
- No `Co-Authored-By: Claude` trailers in commit messages.
