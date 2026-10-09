#!/usr/bin/env python3
"""Copia os modelos de comunidade do GitHub em português para um projeto.

Uso:
    python3 instalar.py /caminho/do/projeto --nome "Meu Projeto" \\
        --email contato@example.com --url https://github.com/usuario/projeto
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Tuple

__version__ = "1.0.0"

TEMPLATE_DIR = Path(__file__).resolve().parent
FILES = (
    ".github/ISSUE_TEMPLATE/relatar-bug.yml",
    ".github/ISSUE_TEMPLATE/sugerir-melhoria.yml",
    ".github/ISSUE_TEMPLATE/duvida.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/FUNDING.yml",
    ".github/dependabot.yml",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "SUPPORT.md",
)
PLACEHOLDERS = ("{{NOME_DO_PROJETO}}", "{{EMAIL_DE_CONTATO}}", "{{URL_DO_REPOSITORIO}}")

CREATED = "criado"
REPLACED = "substituído"
KEPT = "mantido"
WOULD_ASK = "perguntar"

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_URL = re.compile(r"^https?://[^\s/]+(?:/\S*)?$")

_TRANSLATIONS = (
    ("the following arguments are required", "os seguintes argumentos são obrigatórios"),
    ("unrecognized arguments", "argumentos não reconhecidos"),
    ("expected one argument", "esperava um valor"),
    ("ambiguous option", "opção ambígua"),
    ("could match", "pode ser"),
    ("argument ", "argumento "),
)


def make_values(name: str, email: str, url: str) -> Dict[str, str]:
    """Valida os dados do projeto e devolve o mapa placeholder -> valor."""
    name = name.strip()
    email = email.strip()
    url = url.strip().rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    if not name or any(ord(c) < 32 for c in name):
        raise ValueError("informe um nome de projeto (uma linha, sem caracteres de controle)")
    if not _EMAIL.match(email):
        raise ValueError(f"e-mail inválido: {email!r}")
    if not _URL.match(url):
        raise ValueError(f"URL inválida: {url!r} (use algo como https://github.com/usuario/projeto)")
    return dict(zip(PLACEHOLDERS, (name, email, url)))


def yaml_escape(value: str) -> str:
    """Escapa um valor para dentro de uma string YAML entre aspas duplas."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def render(text: str, values: Dict[str, str], yaml: bool = False) -> str:
    """Troca os placeholders pelos valores (nos .yml, eles ficam sempre entre aspas duplas)."""
    for placeholder, value in values.items():
        text = text.replace(placeholder, yaml_escape(value) if yaml else value)
    return text


def install(
    target: Path,
    values: Dict[str, str],
    *,
    force: bool = False,
    dry_run: bool = False,
    ask: Optional[Callable[[str], bool]] = None,
    source: Path = TEMPLATE_DIR,
) -> List[Tuple[str, str]]:
    """Copia os arquivos para ``target`` e devolve a lista (arquivo, ação).

    Arquivos existentes só são substituídos com ``force`` ou quando ``ask``
    devolve True. Com ``dry_run``, nada é gravado.
    """
    results: List[Tuple[str, str]] = []
    for relative in FILES:
        content = render((source / relative).read_text(encoding="utf-8"), values, yaml=relative.endswith(".yml"))
        destination = target / relative
        if not destination.exists():
            action = CREATED
        elif force:
            action = REPLACED
        elif dry_run:
            action = WOULD_ASK
        elif ask is not None and ask(relative):
            action = REPLACED
        else:
            action = KEPT
        if action in (CREATED, REPLACED) and not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with open(destination, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
        results.append((relative, action))
    return results


def _ask_terminal(relative: str) -> bool:
    try:
        answer = input(f"{relative} já existe. Substituir? [s/N] ")
    except EOFError:
        return False
    return answer.strip().lower() in ("s", "sim", "y", "yes")


class _Formatter(argparse.RawDescriptionHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        return super().add_usage(usage, actions, groups, "uso: " if prefix is None else prefix)


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:  # type: ignore[override]
        for english, portuguese in _TRANSLATIONS:
            message = message.replace(english, portuguese)
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: erro: {message}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(
        prog="instalar.py",
        description=(
            "Copia os modelos de issues, pull request e documentos de comunidade para o seu projeto,\n"
            "já com nome, e-mail e URL preenchidos."
        ),
        epilog=(
            "exemplo:\n"
            '  python3 instalar.py ../meu-projeto --nome "Meu Projeto" \\\n'
            "      --email contato@example.com --url https://github.com/usuario/meu-projeto"
        ),
        formatter_class=_Formatter,
        add_help=False,
    )
    parser._positionals.title = "argumentos"
    parser._optionals.title = "opções"
    parser.add_argument("destino", help="pasta do projeto que vai receber os arquivos")
    parser.add_argument("-h", "--help", action="help", help="mostra esta ajuda e sai")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}", help="mostra a versão e sai")
    parser.add_argument("--nome", required=True, help='nome do projeto, ex.: "Meu Projeto"')
    parser.add_argument("--email", required=True, help="e-mail para relatos de conduta e de segurança")
    parser.add_argument("--url", required=True, help="URL do repositório, ex.: https://github.com/usuario/projeto")
    parser.add_argument("--forcar", action="store_true", help="substitui arquivos existentes sem perguntar")
    parser.add_argument("--simular", action="store_true", help="mostra o que seria feito, sem gravar nada")
    return parser


def _plural(count: int, singular: str, plural: str) -> str:
    return f"{count} {singular if count == 1 else plural}"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        values = make_values(args.nome, args.email, args.url)
    except ValueError as error:
        parser.error(str(error))
    target = Path(args.destino)
    if not target.is_dir():
        parser.error(f"a pasta de destino não existe: {args.destino}")

    ask = _ask_terminal if sys.stdin.isatty() else None
    try:
        results = install(target, values, force=args.forcar, dry_run=args.simular, ask=ask)
    except OSError as error:
        print(f"instalar.py: erro ao gravar: {error}", file=sys.stderr)
        return 1

    labels = {CREATED: "criado", REPLACED: "substituído", KEPT: "mantido (já existia)"}
    if args.simular:
        print("Simulação: nada foi gravado.")
        labels = {
            CREATED: "seria criado",
            REPLACED: "seria substituído",
            WOULD_ASK: "já existe (você seria perguntado)",
        }
    print(f"Arquivos em {target}:")
    width = max(len(label) for label in labels.values())
    for relative, action in results:
        print(f"  {labels[action].ljust(width)}  {relative}")

    counts = {action: sum(1 for _, a in results if a == action) for action in (CREATED, REPLACED, KEPT, WOULD_ASK)}
    if args.simular:
        summary = [
            _plural(counts[CREATED], "seria criado", "seriam criados"),
            _plural(counts[REPLACED], "seria substituído", "seriam substituídos"),
            _plural(counts[WOULD_ASK], "já existe", "já existem"),
        ]
    else:
        summary = [
            _plural(counts[CREATED], "criado", "criados"),
            _plural(counts[REPLACED], "substituído", "substituídos"),
            _plural(counts[KEPT], "mantido", "mantidos"),
        ]
    print("Resumo: " + ", ".join(summary) + ".")
    if counts[KEPT] and ask is None and not args.simular:
        print("Arquivos existentes não foram alterados. Use --forcar para substituí-los.")
    if not args.simular:
        print(
            "\nPróximos passos:\n"
            "  - Revise os arquivos e apague o que não fizer sentido para o projeto\n"
            "    (por exemplo, FUNDING.yml ou ecossistemas do dependabot.yml que você não usa).\n"
            "  - Ative o relato privado de vulnerabilidades: em Settings, na seção Security,\n"
            "    ligue a opção Private vulnerability reporting."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
