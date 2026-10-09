"""Verificações estruturais dos modelos (sem depender de um leitor de YAML)."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import instalar  # noqa: E402

ISSUE_FORMS = ("relatar-bug.yml", "sugerir-melhoria.yml", "duvida.yml")
FORM_TYPES = {"markdown", "input", "textarea", "dropdown", "checkboxes"}
PLACEHOLDER = re.compile(r"\{\{([A-Z_]+)\}\}")


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


def form_items(text):
    """Separa os itens de body de um formulário de issue."""
    items = []
    current = None
    for line in text.splitlines():
        match = re.match(r"^  - type: (\S+)\s*$", line)
        if match:
            current = {"type": match.group(1), "id": None, "attributes": False, "validations": False,
                       "label": False, "value": False, "options": False}
            items.append(current)
            continue
        if current is None:
            continue
        if line.startswith("    id: "):
            current["id"] = line.split(":", 1)[1].strip()
        elif line.startswith("    attributes:"):
            current["attributes"] = True
        elif line.startswith("    validations:"):
            current["validations"] = True
        elif line.startswith("      label: "):
            current["label"] = True
        elif line.startswith("      value: "):
            current["value"] = True
        elif line.startswith("      options:"):
            current["options"] = True
    return items


class FilesTest(unittest.TestCase):
    def test_all_files_exist(self):
        for relative in instalar.FILES:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_only_known_placeholders(self):
        known = {p.strip("{}") for p in instalar.PLACEHOLDERS}
        used = set()
        for relative in instalar.FILES:
            used |= set(PLACEHOLDER.findall(read(relative)))
        self.assertEqual(used, known)

    def test_yaml_placeholders_are_inside_double_quotes(self):
        for relative in instalar.FILES:
            if not relative.endswith(".yml"):
                continue
            for number, line in enumerate(read(relative).splitlines(), start=1):
                if "{{" in line:
                    self.assertRegex(line, r':\s+"[^"]*\{\{[A-Z_]+\}\}[^"]*"\s*$', f"{relative}:{number}")


class IssueFormsTest(unittest.TestCase):
    def test_top_level_keys(self):
        for name in ISSUE_FORMS:
            text = read(f".github/ISSUE_TEMPLATE/{name}")
            for key in ("name", "description", "title", "labels", "body"):
                self.assertRegex(text, rf"(?m)^{key}:", f"{name}: falta {key}")

    def test_body_items(self):
        for name in ISSUE_FORMS:
            items = form_items(read(f".github/ISSUE_TEMPLATE/{name}"))
            self.assertGreaterEqual(len(items), 3, name)
            ids = [item["id"] for item in items if item["id"]]
            self.assertEqual(len(ids), len(set(ids)), f"{name}: ids repetidos")
            for item in items:
                self.assertIn(item["type"], FORM_TYPES, name)
                self.assertTrue(item["attributes"], f"{name}: item sem attributes")
                if item["type"] == "markdown":
                    self.assertTrue(item["value"], f"{name}: markdown sem value")
                    self.assertFalse(item["validations"], f"{name}: markdown não aceita validations")
                    self.assertIsNone(item["id"])
                else:
                    self.assertRegex(item["id"] or "", r"^[A-Za-z0-9_-]+$", name)
                    self.assertTrue(item["label"], f"{name}: {item['id']} sem label")
                if item["type"] in ("dropdown", "checkboxes"):
                    self.assertTrue(item["options"], f"{name}: {item['id']} sem options")

    def test_required_fields_on_bug_form(self):
        text = read(".github/ISSUE_TEMPLATE/relatar-bug.yml")
        self.assertIn("required: true", text)
        self.assertIn('labels: ["bug"]', text)
        self.assertIn("render: shell", text)

    def test_config(self):
        text = read(".github/ISSUE_TEMPLATE/config.yml")
        self.assertRegex(text, r"(?m)^blank_issues_enabled: (true|false)$")
        self.assertRegex(text, r"(?m)^contact_links:$")
        self.assertEqual(len(re.findall(r"(?m)^  - name: ", text)), 2)
        self.assertEqual(len(re.findall(r"(?m)^    url: ", text)), 2)
        self.assertEqual(len(re.findall(r"(?m)^    about: ", text)), 2)
        self.assertIn("/security/advisories/new", text)


class OtherConfigTest(unittest.TestCase):
    def test_dependabot(self):
        text = read(".github/dependabot.yml")
        self.assertRegex(text, r"(?m)^version: 2$")
        self.assertRegex(text, r"(?m)^updates:$")
        ecosystems = re.findall(r'(?m)^  - package-ecosystem: "([^"]+)"$', text)
        self.assertEqual(ecosystems, ["npm", "pip", "github-actions"])
        self.assertEqual(len(re.findall(r'(?m)^    directory: "/"$', text)), 3)
        intervals = re.findall(r'(?m)^      interval: "([^"]+)"$', text)
        self.assertEqual(len(intervals), 3)
        self.assertTrue(set(intervals) <= {"daily", "weekly", "monthly"})

    def test_funding_is_fully_commented(self):
        lines = read(".github/FUNDING.yml").splitlines()
        self.assertTrue(lines)
        for line in lines:
            self.assertTrue(not line.strip() or line.lstrip().startswith("#"), line)
        self.assertIn("# github:", "\n".join(lines))
        self.assertIn("# custom:", "\n".join(lines))


class DocumentsTest(unittest.TestCase):
    def test_community_documents(self):
        conduct = read("CODE_OF_CONDUCT.md")
        self.assertIn("{{EMAIL_DE_CONTATO}}", conduct)
        self.assertNotIn("Covenant", conduct)
        security = read("SECURITY.md")
        self.assertIn("Report a vulnerability", security)
        self.assertIn("{{URL_DO_REPOSITORIO}}/security/advisories/new", security)
        contributing = read("CONTRIBUTING.md")
        for section in ("## Preparando o ambiente", "## Mensagens de commit", "## Abrindo o pull request", "## Revisão"):
            self.assertIn(section, contributing)
        self.assertIn("Closes #123", read(".github/PULL_REQUEST_TEMPLATE.md"))
        self.assertIn("SECURITY.md", read("SUPPORT.md"))


if __name__ == "__main__":
    unittest.main()
