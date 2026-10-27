"""CampusNotes - a tiny CLI notes organizer for students.

Stores notes as JSON in data/notes.json. Supports add, list, search and
delete of notes keyed by title.
"""

import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "notes.json")


class NotesApp:
    """Manages a collection of notes persisted to a JSON file."""

    def __init__(self, path=DATA_FILE):
        self.path = path
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.notes = json.load(f)
            except json.JSONDecodeError:
                backup = self.path + ".corrupt"
                os.replace(self.path, backup)
                self.notes = {}
                self._log(f"recovered corrupt notes file -> {backup}")
        else:
            self.notes = {}

    @staticmethod
    def _log(message):
        """Append a line to a local runtime log (git-ignored)."""
        log_path = os.path.join(os.path.dirname(__file__), "campusnotes.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.notes, f, indent=2, sort_keys=True)

    def add(self, title, body=""):
        """Add or update a note. Returns the note dict."""
        title = title.strip()
        if not title:
            raise ValueError("title must not be empty")
        self.notes[title] = {"title": title, "body": body}
        self._save()
        return self.notes[title]

    def delete(self, title):
        """Delete a note by title. Returns True if it existed."""
        existed = self.notes.pop(title, None) is not None
        if existed:
            self._save()
        return existed

    def list_all(self):
        """Return all notes sorted by title."""
        return [self.notes[k] for k in sorted(self.notes)]

    def search(self, keyword):
        """Return notes whose title or body contains keyword (case-insensitive)."""
        k = keyword.lower()
        return [n for n in self.list_all() if k in n["title"].lower()
                or k in n["body"].lower()]

    @staticmethod
    def word_count(note):
        """Number of words in a note's body."""
        return len(note.get("body", "").split())

    def export_markdown(self, path):
        """Write all notes to a single Markdown file. Returns note count."""
        lines = ["# CampusNotes export", ""]
        for note in self.list_all():
            lines.append(f"## {note['title']}\n")
            lines.append(note["body"] or "")
            lines.append("")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return len(self.notes)


def _cmd_add(args, app):
    title, body = args[0], " ".join(args[1:])
    app.add(title, body)
    print(f'Added note "{title}"')


def _cmd_list(args, app):
    for note in app.list_all():
        print(f"- {note['title']}  ({NotesApp.word_count(note)} words)")


def _cmd_search(args, app):
    for note in app.search(args[0]):
        print(f"- {note['title']}")


def _cmd_delete(args, app):
    title = args[0]
    if app.delete(title):
        print(f'Deleted note "{title}"')
    else:
        print(f'No note titled "{title}"')


def _cmd_export(args, app):
    count = app.export_markdown(args[0])
    print(f'Exported {count} notes to {args[0]}')


COMMANDS = {
    "add": _cmd_add,
    "list": _cmd_list,
    "search": _cmd_search,
    "delete": _cmd_delete,
    "export": _cmd_export,
}

USAGE = "usage: campusnotes.py <add|list|search|delete|export> ..."


def main(argv):
    if len(argv) < 2 or argv[1] not in COMMANDS:
        print(USAGE)
        return 1
    if argv[1] == "list":
        COMMANDS["list"](None, NotesApp())
        return 0
    if len(argv) < 3:
        print(USAGE)
        return 1
    COMMANDS[argv[1]](argv[2:], NotesApp())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
