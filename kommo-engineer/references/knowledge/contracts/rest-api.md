# Contrato: REST API v4
Origem: https://developers.kommo.com/
- Base: `https://{subdomain}.kommo.com/api/v4`.
- Conta: `GET /account` (somente leitura).
- Campos: `GET /{entity_type}/custom_fields`, `POST /{entity_type}/custom_fields`.
- Pipelines: `GET /leads/pipelines`, `POST /leads/pipelines`.
- Etapas: `GET /leads/pipelines/{pipeline_id}/statuses`, `POST /leads/pipelines/{pipeline_id}/statuses`.
- Escritas relevantes requerem permissões de administrador conforme método.
- Tokens ficam no gerenciador seguro; não copiar para CLI ou logs.
Verifique parâmetros reais, campos de tipo, limites, erros e re-leitura posterior.
Não interprete resposta HTTP bem-sucedida como alcance do objetivo comercial sem aceite.
