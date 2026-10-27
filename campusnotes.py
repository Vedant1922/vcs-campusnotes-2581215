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
            with open(self.path, "r", encoding="utf-8") as f:
                self.notes = json.load(f)
        else:
            self.notes = {}

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


def main(argv):
    app = NotesApp()
    if len(argv) >= 3 and argv[1] == "add":
        title, body = argv[2], " ".join(argv[3:])
        app.add(title, body)
        print(f'Added note "{title}"')
    elif len(argv) >= 2 and argv[1] == "list":
        for note in app.list_all():
            wc = NotesApp.word_count(note)
            print(f"- {note['title']}  ({wc} words)")
    elif len(argv) >= 3 and argv[1] == "search":
        for note in app.search(argv[2]):
            print(f"- {note['title']}")
    elif len(argv) >= 3 and argv[1] == "delete":
        if app.delete(argv[2]):
            print(f'Deleted note "{argv[2]}"')
        else:
            print(f'No note titled "{argv[2]}"')
    elif len(argv) >= 3 and argv[1] == "export":
        count = app.export_markdown(argv[2])
        print(f'Exported {count} notes to {argv[2]}')
    else:
        print("usage: campusnotes.py <add|list|search|delete|export> ...")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
