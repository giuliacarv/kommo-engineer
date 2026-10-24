# Verificação do candidato 0.5.0-rc.1

Ambiente executado: Windows, Python 3.13.14, Node instalado no computador. `PYTHONUTF8=1` em subprocessos.

- Baseline anterior: 39 testes Python, 4 falhas Windows reproduzidas.
- Candidato: `python -X utf8 -m unittest discover -s kommo-engineer/tests`: **67 testes passaram**. Cobrem CLI anterior, integridade, snapshots, seleção de metas, migração, conflitos, dependências, observações, relatórios e API com transporte falso.
- `node --test kommo-engineer/scripts/connection-doctor.test.mjs`: **7 testes passaram**, rede simulada.
- `validate_knowledge.py`: links válidos, 39 imagens documentadas, 26 hashes únicos, 83 entradas recuperáveis.
- `quick_validate.py`: skill válida; checagem de gramática Python 3.11 em teste local, runtime 3.11 não executado.

Acesso de leitura pelo navegador à conta indicada foi observado. Isso não é teste do novo cliente HTTP nem autorização de mutação. Nenhum campo/funil/bot/mensagem foi alterado para homologar este candidato. Dados operacionais lidos não foram adicionados ao pacote público.

Pendente: integração HTTP autenticada, criação/readback controlados de campo/funil, importação e execução de bot, fluxo externo, retomada em duas conversas por plataforma, usabilidade do playbook e métricas reais. Sem alegação de CI remoto ou homologação de outras plataformas.
