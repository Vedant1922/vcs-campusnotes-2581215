# CampusNotes

A tiny command-line notes organizer for students. Notes are stored as JSON
in `data/notes.json` and managed through `campusnotes.py`.

## Usage

```bash
python campusnotes.py add "VCS Assignment 2" "Due session 30, submit PDF on LMS"
python campusnotes.py list
python campusnotes.py search "vcs"
python campusnotes.py delete "VCS Assignment 2"
python campusnotes.py export notes.md
```

## Features
- Add / update notes by title
- List all notes (sorted), with per-note word count
- Case-insensitive keyword search across title and body
- Delete notes by title
- Export all notes to a single Markdown file

## CLI reference

| Command | Effect |
| --- | --- |
| `add <title> [body...]` | Create or update a note |
| `list` | Print every note with its word count |
| `search <keyword>` | Case-insensitive match on title + body |
| `delete <title>` | Remove a note |
| `export <file.md>` | Write all notes to a Markdown file |

## Data & durability
Notes live in `data/notes.json`. If that file is corrupt, the app backs it
up to `data/notes.json.corrupt`, starts from an empty store, and writes a
line to the local (git-ignored) `campusnotes.log`.

## Tests
```bash
python -m unittest
```
