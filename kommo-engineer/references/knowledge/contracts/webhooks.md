# Webhooks gerais Kommo
https://developers.kommo.com/docs/webhooks-general
Formato documentado: `x-www-form-urlencoded`, não presuma JSON. Normalize payload no receptor.
Defina evento, entidade, mapeamento, segurança, resposta, retry, concorrência, idempotência e observabilidade.
Não trate callbacks de Chats API, webhooks gerais e outros eventos como contrato único.
Se a integração externa alterar o lead e disparar novo webhook, preveja prevenção de loop.
