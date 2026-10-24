# Kommo Engineer 0.4.0-dev — revisão cumulativa em desenvolvimento

## Acesso MCP: atualização de 24/10/2026

- Novo [guia de acesso MCP](../references/integrations/mcp-access-setup.md): integração privada na UI Kommo, token longo no cofre Windows, build do servidor, configuração Codex/Agy/Claude Code, confirmação por camadas e diagnóstico de falhas.
- `scripts/kommo-credential-windows.ps1` recebe token com entrada mascarada por subdomínio e confirma gravação no Gerenciador de Credenciais; `scripts/launch-kommo-mcp-windows.ps1` injeta o segredo apenas no processo local do servidor.
- Removido do guia do conector o exemplo que colocava token literal em JSON. O catálogo de ferramentas continua dependente da versão efetivamente instalada.
- A publicação da skill e a validação estrutural não certificam autenticação de uma conta nem direitos de escrita. Cada cliente precisa de verificação própria de identidade.

## Incluído
- Skill Codex unificada com estratégia comercial, engenharia Kommo e recuperação seletiva de módulos.
- Setup guiado com campos padronizados e CLI de persistência.
- Metas gerais, critérios, eventos, evidências e snapshots documentais.
- Smoke sem rede, verificações estruturais limitadas e diagnósticos.
- Schemas JSON publicados como referência do formato; a CLI ainda não executa validação por schema.
- Cinco procedimentos iniciais documentados com fontes oficiais.
- Conhecimento das quatro fontes Kommo consolidado em referências próprias de CRM, estratégia, automação, IA, integração e projeto; um único ponto de entrada `SKILL.md`. Mapeamento e hashes em `content-integration.json`.
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
- Homologação atual das capturas fornecidas e cobertura completa de todos os nós Salesbot. Os arquivos existentes estão indexados no catálogo visual.
- Cliente HTTP autenticado, disparos ou mutações remotas automáticas.
- Migração de esquemas entre versões, recuperação automática de operações interrompidas.
- Instrumentação confiável de tokens por modelo/ferramenta.
- Homologação no Codex Windows e validação de JSON Schema em runtime.

Os procedimentos documentados não são componentes remotos testados; use a skill como
orquestradora dos módulos estratégicos e técnicos, além de gerenciadora local, e valide os recursos Kommo conforme cada ambiente. Esta revisão não foi homologada numa conta Kommo; nenhuma conta foi acessada ou alterada e o ZIP definitivo não foi gerado.

## Integração de conteúdo em 23/10/2026

Preservados CLI, schemas, templates, procedimentos, recursos visuais e guias anteriores. Acrescentados modelo de decisão entre áreas, referências nativas por assunto, conhecimento do conector MCP e busca textual ampliada. Conteúdo de produto continua versionado: esta manutenção não revalida funcionalidades numa conta Kommo. Veja o [registro de cobertura](content-integration.json).


## Expansão por referências externas — 23/10/2026

Nove repositórios locais foram examinados por documentação e trechos de implementação relevantes. A skill recebeu nove aprofundamentos próprios, um contrato reutilizável e busca ampliada, preservando o conteúdo anterior. A revisão registra o que já existia, o que foi expandido e limitações dos exemplos, inclusive deploy simulado, cache sem isolamento por conta, perda de zero em transformação e cobertura limitada de tracking por navegador. Veja o [relatório desta expansão](external-reference-review.md).
