# Adaptador do projeto Metha

Aplicar somente quando a conta/tarefa alvo for a Metha ou o pedido tratar explicitamente deste módulo. A skill é reutilizável; não transportar ICP, fontes, IDs, executores ou autorizações daqui para outra conta.

## Retomar o módulo

A partir da pasta da skill, `../../..` resolve a raiz do checkout. Ler `kommo-crm/README.md`, `kommo-crm/PLANO_TATICO.md`, `kommo-crm/execution/STATE.json` e `kommo-crm/AGENTS.md`; consultar `RULES.md`, `SOURCES.md` e documentos do lote quando necessários. O cursor único é `STATE.json`; `CHECKPOINT.md` explica evidência e próxima ação. Não reiniciar etapa concluída nem criar plano concorrente.

```powershell
node kommo-crm/scripts/cli.mjs validate
node kommo-crm/scripts/cli.mjs status
node kommo-crm/scripts/cli.mjs doctor
```

`doctor` do módulo é offline; sucesso não prova conexão. Para verificar o MCP existente, usar as ferramentas disponíveis no chat ou `node kommo-crm/scripts/smoke-mcp.mjs` quando pertinente e autorizado. Não renovar credencial só para editar esta skill.

## Separar capacidades atuais

Inspeção local em 16/10/2026, a revalidar antes do uso:

- CLI/MCP de bootstrap continuam READ. O MCP expõe identidade, pipelines, campos, usuários, tags, metadados de bots/webhooks e fontes da integração; isso não certifica acesso de escrita.
- Existem executores separados de escrita gerenciada. `apply-structural-plan.mjs` trata o plano tipado de campos/grupos; `apply-empty-group-plan.mjs` trata somente grupos personalizados vazios com preservação do inventário. Usam os controles do módulo, não equivalem a Writer universal.
- `import-pilot.mjs` possui journal por chave do piloto existente. Não usar o manifesto antigo para outro lote nem reimportar piloto já confirmado.
- O E07 completo e exclusão de campos têm pendências próprias conforme o cursor. Não ampliar allowlist para contornar ausência de executor homologado.

README/AGENTS/código/cursor podem conter snapshots de momentos diferentes. Compare evidência mais recente e capacidade real antes de agir; a frase histórica “Writer não implementado” não descreve os executores específicos que já existem.

## Regras do contexto

- Comercial da Metha trata de escritórios/advogados; registros pessoais, outros negócios e testes não entram na fila por simples nome.
- Oportunidade/qualificação no lead; dados estáveis do escritório na empresa; pessoa/canais nativos no contato. Usar “tag” e, em orientação operacional, “REGISTRAR AS INFORMAÇÕES DO LEAD NO CRM”.
- `config/` guarda proposta até reconciliação; versão no nome do arquivo não prova aprovação. Reconciliar `SOURCES.md` e a fonte comercial vigente por assunto. A skill de direção comercial pode conter referência antiga a Lawria/Kommo desativado; isso não revoga autorização humana posterior para este módulo, nem autoriza sincronização extra.
- Snapshots/journals/dados privados ficam em `kommo-crm/private/`; o Git recebe código/configuração e evidência saneada. Esta pasta é ignorada pelo Git, o que não significa protegida de sincronização do Drive.
- Scripts de credencial do módulo têm destino específico. Não executá-los para outra conta; não ler/imprimir token. Usar o contrato local existente sem copiar o segredo para o bundle da skill.
- Para formulário, provar vínculo ao lead original antes de cancelar continuidade. Para Salesbot, ler `AUTOMATIONS.md`, `SALESBOTS.md` e QA no lote pertinente; salvar/preview não prova entrega ou tarefa.
- Registrar alterações da própria skill como manutenção local, sem alterar cursor de implantação do CRM, autorizações, próxima ação comercial ou status de homologação da conta.

Respeitar autorização Git vigente: edição local não implica commit, push, PR ou publicação. O pedido de melhorar a skill autoriza os arquivos da skill e o registro local de execução; não é lote de configuração da conta.
