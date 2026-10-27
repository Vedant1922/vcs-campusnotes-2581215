# Git hooks

This repository enforces two commit-time checks, installed under `.git/hooks/`
(tracked, shareable copies live in `.githooks/`):

## pre-commit
Blocks a commit while any **staged** file still carries an unresolved task
marker. The exact marker spellings are defined by the grep expression in the
hook source (`.githooks/pre-commit`), so this document does not restate them.
The hook inspects the staged blob, so working-tree edits that were not staged
do not count.

## commit-msg
Blocks commit messages that are shorter than 10 characters or that do not
start with a Conventional Commits type: `feat:`, `fix:`, `docs:`,
`refactor:` or `chore:`.

## Enabling on a fresh clone
`.git/hooks/` is local to each machine and is never shared by `git push`, so
on a new clone run:

```bash
git config core.hooksPath .githooks
```

## Bypassing
`git commit --no-verify` skips all commit-time hooks. It defeats the
enforcement these guards provide, so use it only for genuine emergencies and
never as a habit.
