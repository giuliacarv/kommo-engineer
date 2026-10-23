import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class TestPackageIntegrity(unittest.TestCase):
    def test_manifest(self):
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "kommo-engineer")
        self.assertEqual(manifest["version"], "0.4.0-dev")
        actual = {
            str(p.relative_to(ROOT)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in ROOT.rglob("*") if p.is_file()
            and p.name != "manifest.json"
            and "__pycache__" not in p.parts
            and p.suffix != ".pyc"
        }
        self.assertEqual(actual, manifest["files"])
    def test_catalog_paths(self):
        cat = json.loads((ROOT/"references"/"knowledge"/"catalog.json").read_text(encoding="utf-8"))
        for item in cat["procedures"]:
            self.assertTrue((ROOT / item["path"]).is_file(), item["path"])
    def test_yaml_header(self):
        raw = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(raw.startswith("---\n"))
        front = raw.split("---", 2)[1]
        self.assertIn("name: kommo-engineer", front)
        self.assertIn("description:", front)
if __name__ == "__main__": unittest.main()
