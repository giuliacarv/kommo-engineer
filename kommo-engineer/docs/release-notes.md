# Kommo Engineer 0.4.0-dev — revisão cumulativa em desenvolvimento

## Incluído
- Skill Codex unificada com estratégia comercial, engenharia Kommo e recuperação seletiva de módulos.
- Setup guiado com campos padronizados e CLI de persistência.
- Metas gerais, critérios, eventos, evidências e snapshots documentais.
- Smoke sem rede, verificações estruturais limitadas e diagnósticos.
- Schemas JSON publicados como referência do formato; a CLI ainda não executa validação por schema.
- Cinco procedimentos iniciais documentados com fontes oficiais.
- Conteúdo das skills `kommo-crm`, `kommo-strategic-automation-architect` e `kommo-strategic-automation-architect-agentes-ia` transferido para módulos internos; `kommo-mcp` permanece como guia legado específico de um servidor.
- Biblioteca de busca textual de procedimentos e lacuna visual explícita.
- Relatório, treinamento e Playbook derivados de entregas registradas.
- Guia de instalação Windows e scripts PowerShell/Python.
- Setup adaptativo com contrato de 18 campos, estados de resposta e status de planejamento.
- Retomada compacta de projeto e suporte explícito a diretório existente preservando arquivos e instruções anteriores.
- Validação estrutural do setup, idempotência de atualizações e verificações ampliadas dos snapshots.

## Evidência e homologação

O relatório de revisão recebido junto a esta atualização registra 42/42 testes locais aprovados em Linux e validação independente de um documento de projeto contra Draft 2020-12. Esses resultados são declarações daquele relatório; não foram reexecutados nesta integração. A homologação no Codex Windows e a validação de JSON Schema em runtime continuam pendentes.

## Não incluído / ainda pendente
- Migração dos 19 arquivos da v0.2.0 do Work: não fornecidos.
- Homologação da instalação, ativação e PowerShell no Windows.
- Homologação de API, Salesbot ou n8n numa conta real autorizada.
- Capturas reais da interface e mapa completo de todos os nós Salesbot.
- Cliente HTTP autenticado, disparos ou mutações remotas automáticas.
- Migração de esquemas entre versões, recuperação automática de operações interrompidas.
- Instrumentação confiável de tokens por modelo/ferramenta.
- Homologação no Codex Windows e validação de JSON Schema em runtime.

Os procedimentos documentados não são componentes remotos testados; use a skill como
orquestradora dos módulos estratégicos e técnicos, além de gerenciadora local, e valide os recursos Kommo conforme cada ambiente. Esta revisão não foi homologada numa conta Kommo; nenhuma conta foi acessada ou alterada e o ZIP definitivo não foi gerado.
