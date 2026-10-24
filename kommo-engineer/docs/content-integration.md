# Integração de conteúdo — Kommo Engineer

Revisão local em 23/10/2026. Fonte do projeto e instalação global passam a oferecer uma única skill, `$kommo-engineer`, com conhecimento organizado por assunto. As quatro skills de origem permanecem preservadas e não são dependências para usar o conteúdo incorporado.

## Conteúdo absorvido

| Origem | Conhecimento incorporado |
|---|---|
| kommo-crm | Conexão por conta, identidade/permissões, modelo de dados, operações, automações/canais, investigação webapp, execução/recuperação, fontes e adaptador Metha; diagnóstico de conexão e seus testes |
| kommo-mcp | Transporte, autenticação, variáveis, recursos, prompts, famílias de ferramentas, consultas, escrita, paginação, erros e padrões do servidor específico |
| kommo-strategic-automation-architect | Discovery, contexto, workflow, RevOps, análise comercial, forecast, pós-venda, governança, propostas, documentação e contrato entre desenho e execução |
| kommo-strategic-automation-architect-agentes-ia | Orientação de uso e limites da especialidade de IA, ligada à referência detalhada única de agentes, fontes, persona, ações, canais, voz, agendamento, Copilot, créditos e supervisão |

A referência detalhada de IA era compartilhada pelas duas fontes estratégicas e continua única. Conteúdo de produto mantém as datas e fontes de consulta originais; esta integração não revalida plano, limites ou comportamento numa conta.

## Expansão aplicada

- [Modelo de decisão](../references/decision-model.md) conectando sintoma, hipóteses, evidência discriminante, modelo de dados, escolha de mecanismo, implantação e aceite.
- Referências próprias em `references/crm`, `strategy`, `automation`, `ai`, `integrations` e `projects`, acessíveis diretamente pela entrada principal.
- Contratos explícitos entre IA, Salesbot, pipeline e atendimento humano; comparação entre configuração, execução, persistência e entrega.
- Tratamento distinto de OAuth e token de longa duração, do formato Cursor e do cliente Codex, e do envelope normalizado MCP e HAL bruto.
- Busca ampliada de 5 para 16 entradas. Catálogo visual atualizado com as 39 imagens já fornecidas, com hashes e estado de recurso não homologado.

## Preservação

Todos os 114 arquivos anteriores foram contabilizados. Foram mantidos idênticos em bytes 75 arquivos protegidos: utilitários existentes, testes, schemas, templates, procedimentos, contratos, imagens e guias locais essenciais. O adaptador Metha anterior também permanece idêntico no novo caminho.

Os 27 arquivos de conhecimento/código das quatro fontes têm destino registrado. Metadados de interface das fontes ficam registrados como proveniência; a interface única da Kommo Engineer é preservada. Handoffs para skills separadas foram convertidos em referências internas. Todos os exemplos de código importados foram preservados; a instrução de instalar a antiga skill MCP ficou registrada como histórico de distribuição.

Backup integral da fonte e da instalação anteriores: `C:\Users\Usuário\Documents\Codex\Skill_KommoEngineer\legado\backup-kommo-engineer-20261023-183130`. O [registro detalhado](content-integration.json) contém hashes de origem, mapeamento de caminhos e diferenças editoriais, permitindo revisar o que mudou.

## Verificação e limites

- `quick_validate.py`: aprovado. Um único `SKILL.md`, 168 links locais resolvidos e 27 fontes de conteúdo contabilizadas.
- Integridade Python: 3/3; diagnóstico Node: 7/7 com rede simulada; buscas por assunto: 7/7.
- Suíte Python Windows: 35/39. As mesmas quatro falhas foram reproduzidas na fonte original em fechamento/retomada de metas, smoke e snapshots. Houve divergência entre caminho temporário 8.3 e canônico; a execução com caminho canônico também encontrou `Snapshot não verificou`. A causa completa está pendente. O código desses utilitários foi preservado.
- Nenhuma conta Kommo foi acessada ou alterada. Invocação comportamental da skill em um novo chat e homologação operacional permanecem sem avaliação nesta manutenção.
