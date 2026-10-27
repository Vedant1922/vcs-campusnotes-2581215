# Shared git hooks

These scripts live in the repo so the whole team can use the same hooks.
They are **not** auto-activated on clone — hooks in `.git/hooks/` are local
to each machine and are not shared by `git push`.

To activate them here:

```bash
git config core.hooksPath .githooks
```

After that, `pre-commit` and `commit-msg` run on every `git commit`.
Re-run the command on each cloned machine (or put it in the onboarding docs).

Hooks:
- `pre-commit` — blocks a commit if a staged file contains TODO or FIXME.
- `commit-msg` — blocks messages under 10 chars or without a Conventional
  Commits prefix (feat:, fix:, docs:, refactor:, chore:).
