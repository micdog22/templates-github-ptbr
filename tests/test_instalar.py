import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import instalar  # noqa: E402

VALUES = instalar.make_values("Meu Projeto", "contato@example.com", "https://github.com/usuario/meu-projeto/")


class MakeValuesTest(unittest.TestCase):
    def test_normalizes_url(self):
        values = instalar.make_values(" Projeto ", "a@example.com", "https://github.com/u/p.git")
        self.assertEqual(values["{{NOME_DO_PROJETO}}"], "Projeto")
        self.assertEqual(values["{{URL_DO_REPOSITORIO}}"], "https://github.com/u/p")
        self.assertEqual(VALUES["{{URL_DO_REPOSITORIO}}"], "https://github.com/usuario/meu-projeto")

    def test_rejects_invalid_input(self):
        for args in (
            ("", "a@example.com", "https://github.com/u/p"),
            ("Nome\ncom quebra", "a@example.com", "https://github.com/u/p"),
            ("Projeto", "sem-arroba", "https://github.com/u/p"),
            ("Projeto", "a@example.com", "github.com/u/p"),
            ("Projeto", "a@example.com", "ftp://example.com/p"),
        ):
            with self.assertRaises(ValueError, msg=args):
                instalar.make_values(*args)


class RenderTest(unittest.TestCase):
    def test_markdown_gets_raw_values(self):
        text = "{{NOME_DO_PROJETO}} <{{EMAIL_DE_CONTATO}}> {{URL_DO_REPOSITORIO}}/issues"
        self.assertEqual(
            instalar.render(text, VALUES),
            "Meu Projeto <contato@example.com> https://github.com/usuario/meu-projeto/issues",
        )

    def test_yaml_values_are_escaped_for_double_quotes(self):
        values = instalar.make_values('Projeto "X" \\ beta', "a@example.com", "https://github.com/u/p")
        rendered = instalar.render('description: "Bugs no {{NOME_DO_PROJETO}}"', values, yaml=True)
        self.assertEqual(rendered, 'description: "Bugs no Projeto \\"X\\" \\\\ beta"')
        self.assertEqual(instalar.render("{{NOME_DO_PROJETO}}", values), 'Projeto "X" \\ beta')


class InstallTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.target = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_copies_every_file_with_placeholders_replaced(self):
        results = instalar.install(self.target, VALUES)
        self.assertEqual(results, [(relative, instalar.CREATED) for relative in instalar.FILES])
        for relative in instalar.FILES:
            text = (self.target / relative).read_text(encoding="utf-8")
            self.assertNotIn("{{", text, relative)
        security = (self.target / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("contato@example.com", security)
        self.assertIn("https://github.com/usuario/meu-projeto/security/advisories/new", security)
        bug = (self.target / ".github/ISSUE_TEMPLATE/relatar-bug.yml").read_text(encoding="utf-8")
        self.assertIn('description: "Algo não funciona como deveria no Meu Projeto"', bug)

    def test_does_not_overwrite_without_permission(self):
        existing = self.target / "CONTRIBUTING.md"
        existing.write_text("meu guia\n", encoding="utf-8")
        asked = []

        def refuse(relative):
            asked.append(relative)
            return False

        results = dict(instalar.install(self.target, VALUES, ask=refuse))
        self.assertEqual(asked, ["CONTRIBUTING.md"])
        self.assertEqual(results["CONTRIBUTING.md"], instalar.KEPT)
        self.assertEqual(existing.read_text(encoding="utf-8"), "meu guia\n")

        results = dict(instalar.install(self.target, VALUES))
        self.assertEqual(results["CONTRIBUTING.md"], instalar.KEPT)
        self.assertEqual(existing.read_text(encoding="utf-8"), "meu guia\n")

    def test_overwrites_when_confirmed_or_forced(self):
        existing = self.target / "SUPPORT.md"
        existing.write_text("antigo\n", encoding="utf-8")
        results = dict(instalar.install(self.target, VALUES, ask=lambda relative: True))
        self.assertEqual(results["SUPPORT.md"], instalar.REPLACED)
        self.assertIn("Meu Projeto", existing.read_text(encoding="utf-8"))

        existing.write_text("antigo\n", encoding="utf-8")

        def must_not_ask(relative):
            raise AssertionError("não deveria perguntar com force=True")

        results = dict(instalar.install(self.target, VALUES, force=True, ask=must_not_ask))
        self.assertEqual(results["SUPPORT.md"], instalar.REPLACED)
        self.assertIn("Meu Projeto", existing.read_text(encoding="utf-8"))

    def test_dry_run_writes_nothing(self):
        (self.target / "SECURITY.md").write_text("original\n", encoding="utf-8")
        results = dict(instalar.install(self.target, VALUES, dry_run=True))
        self.assertEqual(results["SECURITY.md"], instalar.WOULD_ASK)
        self.assertEqual(results["CONTRIBUTING.md"], instalar.CREATED)
        self.assertEqual([p.name for p in self.target.iterdir()], ["SECURITY.md"])
        self.assertEqual((self.target / "SECURITY.md").read_text(encoding="utf-8"), "original\n")


class MainTest(unittest.TestCase):
    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            try:
                code = instalar.main(list(args))
            except SystemExit as exit_:
                code = exit_.code
        return code, out.getvalue(), err.getvalue()

    def test_install_and_simulate(self):
        with tempfile.TemporaryDirectory() as folder:
            base = [folder, "--nome", "Meu Projeto", "--email", "contato@example.com", "--url", "https://github.com/u/p"]
            code, out, _ = self.run_main(*base, "--simular")
            self.assertEqual(code, 0)
            self.assertIn("Simulação: nada foi gravado.", out)
            self.assertFalse(any(Path(folder).iterdir()))
            code, out, _ = self.run_main(*base)
            self.assertEqual(code, 0)
            self.assertIn("Resumo: 11 criados, 0 substituídos, 0 mantidos.", out)
            self.assertTrue((Path(folder) / ".github" / "dependabot.yml").is_file())

    def test_usage_errors(self):
        with tempfile.TemporaryDirectory() as folder:
            code, _, err = self.run_main(folder, "--nome", "X", "--email", "invalido", "--url", "https://github.com/u/p")
            self.assertEqual(code, 2)
            self.assertIn("e-mail inválido", err)
            missing = str(Path(folder) / "nao-existe")
            code, _, err = self.run_main(missing, "--nome", "X", "--email", "a@example.com", "--url", "https://github.com/u/p")
            self.assertEqual(code, 2)
            self.assertIn("não existe", err)
            code, _, err = self.run_main(folder)
            self.assertEqual(code, 2)
            self.assertIn("obrigatórios", err)


if __name__ == "__main__":
    unittest.main()
