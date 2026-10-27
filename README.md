# CampusNotes

A tiny command-line notes organizer for students. Notes are stored as JSON
in `data/notes.json` and managed through `campusnotes.py`.

## Usage

```bash
python campusnotes.py add "VCS Assignment 2" "Due session 30, submit PDF on LMS"
python campusnotes.py list
python campusnotes.py search "vcs"
python campusnotes.py delete "VCS Assignment 2"
```

## Features
- Add / update notes by title
- List all notes (sorted)
- Case-insensitive keyword search across title and body
- Delete notes by title

## Tests
```bash
python -m unittest
```
