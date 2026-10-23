# PROC-KOMMO-002 — Conexão segura à API Kommo

**Estado:** documentado por fonte pública; não homologado em conta Kommo.
**Revisão:** 2026-10-23.
**Aplicabilidade:** validar plano, idioma, permissões, canal, versão e interface na conta atual.


## Objetivo
Validar a conexão HTTP por leitura e confirmar que a credencial aponta para a conta autorizada.
## Pré-requisitos
Integração e permissões pertinentes, subdomínio exato, gerenciador de credenciais, HTTPS.
## Escolha de autenticação
- OAuth 2.0: para integração com autorização e renovação conforme contrato oficial.
- Token de longa duração: apropriado apenas para integração privada compatível; não possui refresh token.
Não armazene credenciais em Markdown, Git, log, argumentos de CLI ou screenshots.
## Procedimento
1. Defina a finalidade e escopo mínimo da integração.
2. Configure credencial no mecanismo seguro da ferramenta executora.
3. Efetue GET `https://{subdomain}.kommo.com/api/v4/account`.
4. Confira status HTTP, tipo de resposta, ID/nome e subdomínio.
5. Se 401/403, pare; se 429, respeite limite atual; não tente escrita para "testar" a autenticação.
6. Registre somente conta identificada, método, data, resultado e evidência sanitizada.
## Aceite
GET válido e identidade correspondente. Não inferir autorização para escrita.
## Fontes
- https://developers.kommo.com/reference/account-parameters
- https://developers.kommo.com/docs/long-lived-token
- https://developers.kommo.com/docs/private-integration
- https://developers.kommo.com/docs/limitations

