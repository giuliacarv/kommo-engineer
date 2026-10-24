# Sincronização Kommo e Google Sheets

Use para exportação, importação ou sincronização entre CRM e planilha, principalmente quando ambos podem editar o mesmo registro. Aprofunda [workflow](../strategy/workflow-architecture.md), [modelo de CRM](../crm/crm-design.md) e [extração](../data/extraction-and-modeling.md).

## Definir o contrato antes do mecanismo

Registre planilha e aba por identidade estável, conta Kommo, entidade, chave de vínculo, colunas, tipo/enum e permissão por direção. Defina quais campos são apenas visualização, entrada humana, fórmula ou escrita exclusiva de um sistema. Exportar CRM para Sheets e permitir criação a partir de uma linha são operações com efeitos diferentes.

Número da linha muda com ordenação/inserção; não é identidade de negócio. Use uma chave persistente ou mapa externo e confirme o ID da entidade. Nomes, telefone formatado e e-mail isolado podem gerar múltiplas correspondências; retenha ambíguos para revisão. Não transporte o modelo de agenda clínica da fonte para outro negócio.

Use o [modelo de contrato](../../assets/templates/integration-contract.json) para registrar fonte por campo, direção, conflitos, cursor e aceites. Ele documenta uma proposta e não conecta os sistemas.

## Comparar com a última versão reconciliada

Para sincronização bilateral, mantenha baseline por chave/campo ou versão equivalente. Compare o valor de cada lado com esse baseline:

| CRM mudou | Sheets mudou | Tratamento |
|---|---|---|
| Não | Não | Nenhuma escrita |
| Sim | Não | Propagar apenas os campos cuja direção permite |
| Não | Sim | Validar intenção e propagar somente a escrita autorizada |
| Sim | Sim, mesmo resultado normalizado | Reconciliar sem duplicar efeitos |
| Sim | Sim, valores diferentes | Aplicar regra de precedência acordada ou enviar à fila de conflito |

“Último timestamp vence” só é aceitável quando semântica, relógio e política o sustentam. Uma leitura pode ficar obsoleta durante o ciclo; revalide precondições antes da escrita. Atualização feita pela própria integração não deve gerar ping-pong: use versão, hash dos campos relevantes e origem do efeito.

## Preservar semântica da planilha

Não sobrescreva fórmula com valor calculado nem valide apenas a aparência da célula. Preserve IDs com zeros iniciais, formatação necessária, validação e colunas gerenciadas pela equipe. Defina locale, fuso e unidade de datas/valores. Texto vazio, célula ausente, zero, false e pedido de limpar campo são estados distintos.

Escrita por intervalo deve usar identidade relida, evitando deslocamento de linha. Verifique uma amostra e contagens antes/depois; para lote sensível, guarde a versão e o diff necessário à recuperação. Planilha não deve guardar token de CRM ou segredo de service account.

## Cursor, criação e falha parcial

Defina janela de leitura, ordenação e watermark suportados pela API atual. Use sobreposição controlada e deduplicação quando necessário. Avance o checkpoint somente depois de persistir/reconciliar os resultados correspondentes. Somar segundos ao maior `updated_at` pode pular eventos; itens com o mesmo timestamp e registros tardios precisam de tratamento explícito.

Na criação, persista chave da linha → ID retornado antes de qualquer repetição. Se o POST tiver timeout, procure o efeito por journal/chave confiável antes de criar novamente. Não limpe o mapa de IDs para “reiniciar” uma sincronização já aplicada.

Se um lado falhar depois de o outro gravar, registre pendência com lado, campo e versão. Reprocesse apenas a etapa afetada. A fila de erro precisa separar validação, identidade, conflito, credencial, quota e resultado incerto; retry infinito não resolve erro de contrato.

Exclusão ou desaparecimento de linha não autoriza apagar CRM. Defina arquivamento, tombstone, desvínculo ou revisão humana antes de propagar exclusões. Trate restauração e reutilização de chave como novos casos de reconciliação.

## Aceite

Verifique criação única, mudança em cada direção, edição simultânea, reordenação de linhas, fórmula preservada, valor vazio/zero, data/fuso, página extra, expiração de credencial e interrupção após escrita. Reconcilie totais e campos em ambos os lados. O ciclo em background funcionar não prova consistência nem cobertura.

Origem metodológica: [EXT-005](../external-sources.md#ext-005). O padrão bilateral foi aprofundado com controles próprios; código, credenciais e campos específicos do projeto de origem não foram copiados.
