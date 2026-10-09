# Política de segurança do {{NOME_DO_PROJETO}}

Levamos a segurança a sério e agradecemos a quem ajuda a manter o projeto seguro.

## Versões com suporte

As correções de segurança são feitas na versão mais recente. Se você usa uma versão antiga, atualize antes de relatar para conferir se o problema continua.

<!-- Se o projeto mantém mais de uma versão, troque o parágrafo acima por uma tabela, por exemplo:

| Versão | Recebe correções de segurança |
| --- | --- |
| 2.x | Sim |
| 1.x | Não |
-->

## Como relatar uma vulnerabilidade

**Não abra uma issue pública e não comente sobre o problema em pull requests ou discussões.** Publicar os detalhes antes da correção coloca em risco todo mundo que usa o projeto.

Use um destes canais privados:

1. **Relato privado de vulnerabilidades do GitHub (recomendado):** na aba **Security** do repositório, clique em **Report a vulnerability**, ou acesse direto {{URL_DO_REPOSITORIO}}/security/advisories/new. Só você e a equipe de manutenção veem o relato, e a conversa sobre a correção acontece ali mesmo.
2. **E-mail:** escreva para **{{EMAIL_DE_CONTATO}}** com o assunto "Vulnerabilidade de segurança".

## O que incluir no relato

- O tipo de problema (por exemplo: injeção de SQL, XSS, exposição de dados, execução remota de código).
- A versão afetada e os arquivos ou trechos de código envolvidos, se souber.
- Um passo a passo para reproduzir, de preferência com uma prova de conceito.
- O impacto: o que alguém mal-intencionado conseguiria fazer.
- Uma sugestão de correção, se tiver.

## O que acontece depois

1. Confirmamos o recebimento do relato assim que possível.
2. Investigamos o problema e mantemos você informado sobre o andamento.
3. Preparamos a correção e, quando ela estiver disponível, publicamos um aviso de segurança (security advisory) descrevendo o problema e as versões corrigidas.
4. Se você quiser, colocamos o seu nome nos créditos do aviso.

Pedimos que a vulnerabilidade não seja divulgada antes de a correção ser publicada. A data da divulgação é combinada com você.

## Fora do escopo

- Vulnerabilidades em bibliotecas de terceiros: relate a quem mantém a biblioteca. Se o {{NOME_DO_PROJETO}} usa uma versão vulnerável, aí sim avise a gente.
- Testes que prejudiquem outras pessoas, como ataques de negação de serviço, spam ou engenharia social.
