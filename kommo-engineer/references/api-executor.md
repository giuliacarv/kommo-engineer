# Executor API — experimental, sem homologação remota

Dependência: Python 3.11+, somente biblioteca padrão. Credencial no ambiente `KOMMO_ACCESS_TOKEN`, fornecida fora do chat pelo operador/cofre; nunca como argumento ou arquivo de projeto. O cliente aceita apenas subdomínio simples, HTTPS Kommo, endpoints allowlist e bloqueia redirects. Não extrai sessão do navegador nem lê cofres por inferência.

Comandos: `api doctor --subdomain SUB`; demais exigem `--account-id ID`. Doctor lê identidade; plano/permissão ficam desconhecidos se não observados. `api read --resource leads|contacts|companies|fields-leads|fields-contacts|fields-companies|pipelines|statuses|bots`; statuses exige --pipeline-id. Saída é projeção reduzida; não é exportação de registros completos. Listagem paginada limitada a 20 páginas, falha explícita em truncamento.

`api bind --project PATH` vincula identidade lida ao projeto; não concede autorização. `api inventory --project PATH` conserva metadados por account_id e data, sem cadastros de pessoas. Cache documental é invalidado pela nova leitura antes de qualquer escrita. Não copie IDs entre contas.

## Escrita limitada, desativada por padrão

1. Dentro do projeto, prepare spec JSON: {"kind":"field","action":"create","entity":"leads","values":{"name":"Campo de teste","type":"text"}}. Outros tipos permitidos pelo executor: numeric, checkbox, date, url, textarea, date_time. Listas/enums e exclusão ficam fora desta fatia. Pipeline/stage: name e sort; atualização também id, stage também pipeline_id. Alterar tipo e etapas sistêmicas fica fora do executor.
2. `api plan --project PATH --subdomain SUB --account-id ID --file spec.json` lê identidade, estado e conflitos; gera plano imutável e digest. Revise o diff. Nenhuma alteração de CRM é aplicada aqui.
3. Escopo autorizado explícito em arquivo privado: approved=true, plan_digest exato, subdomain, account_id, authorization_ref e administrator_confirmed=true. Isso registra autorização humana; arquivo não descobre nem concede permissão. Confirmar primeiro ambiente e recursos de teste.
4. Só com autorização específica, `KOMMO_ENABLE_WRITES=true` no ambiente e `api apply --file plano.json --scope autorizacao.json ...` permite a fatia publicada. O padrão continua desligado. Checa novamente conta, estado e duplicidade, grava operation_id antes de transmitir e exige pós-leitura de valores esperados.
5. Timeout ou retorno ambíguo bloqueia novas escritas: `api reconcile --operation-id OP-ID --conclusion observed_pass|not_applied --reason TEXTO ...` sempre relê destino e só aceita conclusão compatível. Nunca repete POST automaticamente. Identidade confirmada não é permissão para aplicar.

401/403 não repetem. GET em 429/5xx/timeout tem no máximo 3 tentativas e backoff 1/2s. Escrita tem uma tentativa; resposta desconhecida/erro de readback gera journal ambíguo. Respostas HTTP completas, credenciais e dados pessoais não entram no journal. Logs de plano incluem nomes de recursos e ficam privados no projeto.

Contratos oficiais e limites: [matriz](knowledge/contracts/capabilities.json). Testes desta versão usam transporte falso; precisam de homologação real antes de anúncio operacional.
