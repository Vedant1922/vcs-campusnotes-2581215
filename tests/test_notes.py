import json
import os
import tempfile
import unittest

import campusnotes


class NotesAppTest(unittest.TestCase):
    def setUp(self):
        self.fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(self.fd)
        os.unlink(self.path)  # start empty
        self.app = campusnotes.NotesApp(path=self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_add_and_list(self):
        self.app.add("Git", "version control")
        self.assertEqual(len(self.app.list_all()), 1)

    def test_search_is_case_insensitive(self):
        self.app.add("git hooks", "run before commit")
        hits = self.app.search("GIT")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["title"], "git hooks")

    def test_delete(self):
        self.app.add("temp", "x")
        self.assertTrue(self.app.delete("temp"))
        self.assertFalse(self.app.delete("temp"))

    def test_add_rejects_empty_title(self):
        with self.assertRaises(ValueError):
            self.app.add("   ")

    def test_persistence(self):
        self.app.add("notes", "persist me")
        reloaded = campusnotes.NotesApp(path=self.path)
        self.assertIn("notes", reloaded.notes)


if __name__ == "__main__":
    unittest.main()
