# Templates GitHub em Português — issues, PRs e documentos de comunidade prontos para usar

Um repositório bem cuidado tem formulários de issue que pedem as informações certas, um modelo de pull request, guia de contribuição, código de conduta e política de segurança. Escrever tudo isso do zero dá trabalho, e quase todo material pronto está em inglês.

Este projeto reúne esses arquivos em português, prontos para copiar para o seu repositório, com um instalador opcional que já preenche o nome do projeto, o e-mail de contato e a URL do repositório.

## O que vem no pacote

| Arquivo | Para que serve |
| --- | --- |
| `.github/ISSUE_TEMPLATE/relatar-bug.yml` | Formulário de bug: o que aconteceu, passos para reproduzir, comportamento esperado, versão, sistema operacional e logs. |
| `.github/ISSUE_TEMPLATE/sugerir-melhoria.yml` | Formulário de sugestão: problema, solução proposta, alternativas e importância. |
| `.github/ISSUE_TEMPLATE/duvida.yml` | Formulário para dúvidas de uso. |
| `.github/ISSUE_TEMPLATE/config.yml` | Desativa issues em branco e mostra atalhos para as Discussões e para o relato privado de vulnerabilidades. |
| `.github/PULL_REQUEST_TEMPLATE.md` | Modelo de descrição de pull request, com tipo de mudança e checklist. |
| `CONTRIBUTING.md` | Guia de contribuição: ambiente, branches, mensagens de commit (Conventional Commits), pull requests e revisão. |
| `CODE_OF_CONDUCT.md` | Código de conduta escrito em português para este projeto, com canal de denúncia por e-mail. |
| `SECURITY.md` | Como relatar vulnerabilidades em sigilo: relato privado do GitHub ou e-mail. |
| `SUPPORT.md` | Onde pedir ajuda e como fazer uma boa pergunta. |
| `.github/FUNDING.yml` | Exemplo comentado do botão **Sponsor** (GitHub Sponsors, Ko-fi, um link para a sua chave Pix etc.). |
| `.github/dependabot.yml` | Exemplo de atualização automática de dependências para npm, pip e GitHub Actions. |

Os textos usam três marcadores, trocados pelo instalador:

| Marcador | Exemplo |
| --- | --- |
| `{{NOME_DO_PROJETO}}` | `Meu Projeto` |
| `{{EMAIL_DE_CONTATO}}` | `contato@example.com` |
| `{{URL_DO_REPOSITORIO}}` | `https://github.com/usuario/meu-projeto` |

## Como usar

### Opção 1: instalador

Precisa só do Python 3.9 ou mais recente, sem dependências.

```bash
git clone https://github.com/micdog22/templates-github-ptbr
cd templates-github-ptbr
python3 instalar.py /caminho/do/meu-projeto --nome "Meu Projeto" \
    --email contato@example.com --url https://github.com/usuario/meu-projeto
```

```
Arquivos em /caminho/do/meu-projeto:
  criado                .github/ISSUE_TEMPLATE/relatar-bug.yml
  criado                .github/ISSUE_TEMPLATE/sugerir-melhoria.yml
  ...
  mantido (já existia)  CONTRIBUTING.md
  criado                SUPPORT.md
Resumo: 10 criados, 0 substituídos, 1 mantido.
```

- Se um arquivo já existir, o instalador pergunta antes de substituir. Sem terminal interativo (em um script, por exemplo), arquivos existentes são mantidos.
- `--forcar` substitui os arquivos existentes sem perguntar.
- `--simular` mostra o que seria feito, sem gravar nada.

### Opção 2: copiar à mão

Copie os arquivos para o seu repositório, mantendo as pastas, e procure por `{{` para trocar os marcadores. Nos arquivos `.yml`, os marcadores ficam entre aspas duplas: se o nome do projeto tiver aspas ou barra invertida, escreva `\"` e `\\`.

### Opção 3: "Use this template"

Clique em **Use this template** no topo desta página para criar um repositório novo já com os arquivos. Depois, no repositório criado, preencha os marcadores com o próprio instalador e apague o que for só deste projeto (`instalar.py`, `tests/` e este README):

```bash
python3 instalar.py . --nome "Meu Projeto" --email contato@example.com \
    --url https://github.com/usuario/meu-projeto --forcar
```

### Depois de instalar

- Ative o relato privado de vulnerabilidades: em **Settings**, na seção **Security**, ligue a opção **Private vulnerability reporting**. É para ela que apontam o `SECURITY.md` e o atalho do `config.yml`.
- Se as Discussões não estiverem ativadas, ative-as ou remova o link "Discussões" do `config.yml` e do `SUPPORT.md`.
- No `dependabot.yml`, deixe só os ecossistemas que o projeto usa.
- Os formulários usam as etiquetas `bug`, `enhancement` e `question`, que o GitHub cria por padrão em repositórios novos. Se você apagou alguma, crie de novo ou ajuste o campo `labels`.
- Os textos tratam o nome do projeto no masculino ("o Meu Projeto", "do Meu Projeto"). Ajuste se preferir outra forma.

## Dica: padrões para todos os seus repositórios

Crie um repositório **público** chamado `.github` na sua conta ou organização e coloque nele os arquivos de comunidade, nas mesmas pastas usadas aqui (`CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `.github/FUNDING.yml`, `.github/ISSUE_TEMPLATE/` e `.github/PULL_REQUEST_TEMPLATE.md`). O GitHub passa a usar esses arquivos em todos os seus repositórios que não tiverem a própria versão de cada um.

Algumas observações:

- O `dependabot.yml` não é herdado: ele precisa estar em cada repositório.
- Para textos genéricos, rode o instalador com `--nome projeto` ("Código de Conduta do projeto", "Como contribuir com o projeto").
- Os links montados com a URL do repositório (Discussões e relato de vulnerabilidade) apontariam para o próprio `.github`. Nos padrões compartilhados, troque esses links por instruções gerais, como "use a aba **Security** do repositório".

## Testes

```bash
python3 -m unittest discover -s tests -v
```

Os testes cobrem o instalador (cópia, troca dos marcadores, escape nos `.yml`, confirmação antes de substituir e simulação) e verificam a estrutura dos formulários: chaves obrigatórias, tipos de campo válidos, `id` únicos e sem `validations` em blocos de texto.

## Contribuindo

Issues e pull requests são bem-vindos, inclusive com sugestões de texto.

## Licença

MIT — veja [LICENSE](LICENSE).
