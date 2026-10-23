# Conexão por conta e diagnóstico de acesso

## Descobrir antes de pedir credencial

Confirme URL/subdomínio alvo e ferramentas realmente expostas. Com MCP já conectado, use a ferramenta de identidade da conta e compare com o alvo. Liste capacidades pelo schema/descrição e pelo resultado observado; não presuma escrita porque o servidor se chama Kommo.

Se apontar para outra conta, não consulte os registros nem troque silenciosamente a credencial existente. Prepare um perfil isolado para a conta solicitada. Mantenha separados host, account_id, integração, ambiente, mapeamentos de IDs e diretório privado. Nunca reutilize IDs ou planos de uma conta em outra.

Registro mínimo sem segredo: `profile`, `subdomain`, `account_id`, `environment`, `credential_reference`, `transport`, capacidades observadas, escopo autorizado, cobertura e data da verificação. `credential_reference` é o nome/caminho no cofre, não o valor do token. Dados da conta e evidência ficam fora do bundle reutilizável da skill.

## Quando faltar acesso

Solicitação sugerida, adaptada ao que já se sabe:

> Para trabalhar na conta, preciso da URL/subdomínio e de uma conexão API/MCP para ela. Se ainda não houver conexão, um administrador pode criar uma integração privada e gerar o token de longa duração. Guarde-o no cofre ou ambiente local indicado; não cole o token aqui. Depois de configurar, diga apenas que está pronto para eu validar por leitura.

Passos da integração privada, conferidos em 16/10/2026:

1. Entrar **na conta correta**, como administrador, em Configurações → Integrações → Criar integração.
2. Nomear/descrever a finalidade e conferir os acessos da integração. Para o fluxo com token de longa duração, deixar a URL de redirecionamento vazia.
3. Salvar, abrir a aba de chaves/escopos e gerar token de longa duração. Os rótulos podem variar por idioma/UI.
4. Escolher a validade necessária e guardar o segredo assim que for exibido. A documentação permite de 1 dia a 5 anos; esse token não tem `refresh_token`. Revogação/expiração exige substituição, não refresh OAuth.
5. Provisionar no processo/servidor de destino. Validar a conta por GET antes de qualquer leitura adicional ou escrita.

Fontes: [integração privada](https://developers.kommo.com/docs/private-integration), [token de longa duração](https://developers.kommo.com/docs/long-lived-token). O token opera com direitos administrativos; limitar ferramentas/métodos no MCP não reduz os direitos do segredo. Para uma integração pública distribuída entre contas, avaliar OAuth 2.0 e seu ciclo de tokens conforme a documentação, em vez de distribuir um token privado.

## Provisionamento local e MCP

- Preferir cofre/segredo de processo; em Windows, cofre do sistema ou proteção DPAPI quando disponível. `.env` pode ser usado quando adequado, fora de pasta compartilhada/sincronizada e ignorado pelo Git, com permissões locais restritas. `.gitignore` sozinho não impede sincronização pelo Drive.
- Convenção do diagnóstico desta skill: `KOMMO_SUBDOMAIN`, `KOMMO_TOKEN`, opcional `KOMMO_EXPECTED_ACCOUNT_ID`. Adaptar ao cliente existente sem criar aliases de segredo desnecessários.
- Nunca inserir token em chat, prompt, argumento CLI, URL/query string, código versionado, metadata da skill, log ou backup. Não ler `.env` para exibir seu conteúdo. Exibir apenas presença e resultado saneado.
- A skill descreve o trabalho; **não instala nem conecta um MCP sozinha**. Para um MCP novo, usar a configuração suportada pelo cliente e um servidor revisado, com identidade, allowlist de operações e credencial no processo/cofre. Não inventar endereço de servidor. Recarregar a sessão se necessário e verificar a ferramenta exposta em nova leitura.
- API direta é alternativa quando disponível e autorizada; não requer MCP. Conexão inicial usa somente GET `/api/v4/account`, em HTTPS no host exato, `Authorization: Bearer` e sem seguir redirecionamentos.
- Rotação: validar o destino e o novo acesso sem imprimir segredo; substituir a referência local de forma segura e revogar o anterior quando apropriado. Não usar script com host/ID fixo de outro cliente.

## Diagnóstico executável desta skill

`scripts/connection-doctor.mjs` usa Node 22+, não depende de pacotes e não grava arquivos. Sem `--live`, confere somente formato/presença. Com `--live`, faz **um GET de conta**, timeout de 15 s, sem retries/redirecionamentos e sem imprimir corpo bruto ou erros da rede. Não cria nem gira credenciais.

Com as variáveis já fornecidas de forma segura ao processo, a partir da raiz da skill:

```powershell
node scripts/connection-doctor.mjs
node scripts/connection-doctor.mjs --live --expected-subdomain conta-alvo
node scripts/connection-doctor.mjs --live --expected-subdomain conta-alvo --expected-account-id 123456
```

`conta-alvo` e `123456` são exemplos de parâmetros não secretos. Se usar `node --env-file=<caminho-privado>`, conferir o arquivo no destino sem mostrá-lo. Não adicionar o token ao comando. O parâmetro de subdomínio esperado é obrigatório na leitura live e deve corresponder ao que o usuário indicou, independentemente da variável de ambiente.

Sem account_id previamente conhecido, o resultado é `identity_observed`: registrar a identidade obtida para conciliação, sem alegar que um ID esperado foi comparado. Com ID esperado e coincidente, `identity_verified`. Ambos provam só a leitura básica da conta, sem certificar outros recursos ou privilégios de escrita.

## Interpretar falhas

| Sinal | Próximo passo |
|---|---|
| Token ausente | Solicitar provisionamento; continuar preparação offline |
| Subdomínio/ID diverge | Parar operações dessa conexão; selecionar perfil correto |
| 401 | Interromper chamadas autenticadas; conferir validade/revogação e credencial |
| 403 | Investigar recurso/permissão e eventual bloqueio por limite; não concluir automaticamente token inválido |
| 429 | Reduzir carga e respeitar espera; coordenar consumidores da integração |
| 3xx, TLS, timeout, resposta inválida | Conferir host/rede; não encaminhar segredo para destino alternativo |
| MCP só READ | Usar leitura; preparar Writer revisado quando a implementação exigir |

Uma ferramenta que falha ou não existe é limitação deste chat. Informar exatamente qual acesso falta e concluir o restante possível.
