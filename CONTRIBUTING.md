# Como contribuir com o {{NOME_DO_PROJETO}}

Que bom ter você por aqui! Toda ajuda é bem-vinda: corrigir um erro de digitação, melhorar a documentação, relatar um bug, sugerir uma ideia ou escrever código. Este guia explica o caminho mais curto entre a sua ideia e uma contribuição aceita.

Ao participar, você concorda em seguir o nosso [Código de Conduta](CODE_OF_CONDUCT.md).

## Formas de contribuir

- **Relatar bugs:** abra uma issue usando o formulário "Relatar bug". Passos para reproduzir e mensagens de erro ajudam muito.
- **Sugerir melhorias:** use o formulário "Sugerir melhoria" e conte qual problema a ideia resolve.
- **Melhorar a documentação:** textos confusos, exemplos que não funcionam e erros de português também são bugs.
- **Escrever código:** procure issues com as etiquetas `good first issue` (boas para começar) ou `help wanted` (onde precisamos de ajuda).
- **Revisar pull requests:** testar e comentar os pull requests de outras pessoas também é contribuir.

Encontrou uma falha de segurança? **Não abra uma issue pública.** Siga as instruções da [política de segurança](SECURITY.md).

## Antes de começar

Para mudanças pequenas (correções, ajustes de texto), pode mandar o pull request direto. Para mudanças maiores, abra uma issue antes e conte o que pretende fazer: assim a gente conversa sobre a abordagem e ninguém perde tempo com um trabalho que não vai ser aceito.

Se for trabalhar em uma issue existente, comente nela avisando, para evitar que duas pessoas façam a mesma coisa.

## Preparando o ambiente

1. Faça um fork do repositório pelo botão **Fork** no GitHub.
2. Clone o seu fork:

   ```bash
   git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
   cd NOME-DO-REPOSITORIO
   ```

3. Adicione o repositório original como `upstream`, para manter o seu fork atualizado:

   ```bash
   git remote add upstream {{URL_DO_REPOSITORIO}}.git
   git fetch upstream
   ```

4. Instale as dependências e rode o projeto seguindo as instruções do README.
5. Rode os testes antes de mudar qualquer coisa, para ter certeza de que tudo funciona na sua máquina.

## Fazendo a sua mudança

1. Atualize o seu fork e crie uma branch a partir da branch principal, com um nome que descreva a mudança:

   ```bash
   git switch main
   git pull upstream main
   git switch -c fix/erro-ao-salvar
   ```

   Sugestões de prefixo: `feat/` para novidades, `fix/` para correções, `docs/` para documentação.

2. Faça a mudança em passos pequenos, com commits que façam sentido sozinhos.
3. Adicione ou atualize testes que cubram o que você mudou.
4. Rode os testes e o verificador de estilo do projeto, se houver.
5. Atualize a documentação quando a mudança afetar quem usa o projeto.

## Mensagens de commit

Usamos o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/). Cada mensagem começa com um tipo, seguido de uma descrição curta no imperativo:

```
<tipo>(escopo opcional): descrição curta
```

| Tipo | Quando usar |
| --- | --- |
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Só documentação |
| `test` | Adição ou ajuste de testes |
| `refactor` | Mudança de código que não altera o comportamento |
| `style` | Formatação, espaços, ponto e vírgula (sem mudar o código) |
| `perf` | Melhoria de desempenho |
| `chore` | Manutenção, dependências, configuração |

Exemplos:

```
feat: adiciona exportação em CSV
fix(login): corrige erro ao entrar com e-mail em maiúsculas
docs: explica como configurar as variáveis de ambiente
```

Se a mudança quebra compatibilidade, adicione `!` depois do tipo (`feat!: remove suporte à versão 1 da API`) e explique no corpo do commit o que muda para quem usa.

## Abrindo o pull request

1. Envie a branch para o seu fork: `git push origin fix/erro-ao-salvar`.
2. No GitHub, clique em **Compare & pull request**.
3. Preencha o modelo de descrição: o que muda, por quê e como foi testado.
4. Se o pull request resolve uma issue, escreva `Closes #123` na descrição para que ela seja fechada automaticamente.
5. Pull requests pequenos e focados em um assunto são revisados muito mais rápido. Se a mudança cresceu, considere dividir em partes.

Pode abrir o pull request como **rascunho** (draft) se quiser opinião antes de terminar.

## Revisão

- Uma pessoa mantenedora vai revisar o seu pull request assim que possível. Se demorar, fique à vontade para comentar no pull request lembrando.
- Os comentários da revisão são sobre o código, nunca sobre você. Se não concordar com alguma sugestão, explique o seu ponto: a conversa faz parte do processo.
- Para atender aos pedidos de ajuste, faça novos commits na mesma branch; o pull request é atualizado sozinho.
- Os testes automáticos precisam passar antes da aprovação.
- Depois de aprovado, o pull request é incorporado à branch principal, e a sua contribuição passa a fazer parte do projeto. Obrigado!

## Licença

Ao contribuir, você concorda que a sua contribuição será distribuída sob a mesma licença do projeto.

## Dúvidas

Se algo neste guia não ficou claro, abra uma issue usando o formulário "Dúvida" ou veja outras formas de ajuda em [SUPPORT.md](SUPPORT.md).
