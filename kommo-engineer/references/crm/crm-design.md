# Arquitetura, auditoria e qualidade do CRM

## Diagnóstico comercial que muda a configuração

Recupere dos dados/documentos o que já estiver disponível: oferta, comprador, canais, volume, ciclo, equipe, horários, distribuição e resultado desejado. Pergunte apenas as lacunas decisivas. Descubra onde o processo quebra e como isso afeta receita, margem, tempo ou experiência; não prescreva campos/bots antes disso.

Faça inventário proporcional ao pedido: conta, usuários/equipes/permissões, funis/etapas, entidades/vínculos, campos/grupos/enums, tags, tarefas, origens, canais e consumidores. Inclua plano/recurso quando necessário, sem inferi-lo só pelo menu visível. Documente cobertura: amostra, população, filtros, paginação, período, timezone, recursos inacessíveis e divergências durante a coleta. Endpoint inacessível ou formato inesperado não significa coleção vazia.

Cruze estrutura com amostra operacional autorizada: leads sem responsável, próxima ação vencida, campos pouco preenchidos, automações sobrepostas, etapas sem critério, gargalos por origem/equipe e possíveis duplicatas. Metadados de bot não provam sua lógica; `updated_at` não prova contato. Não extrapole dez leads para a conta inteira.

## Modelar com utilidade comercial

| Elemento | Uso | Erro que evitar |
|---|---|---|
| Lead/oportunidade | Demanda específica, qualificação, valor, etapa, decisão | Usar a pessoa inteira como um único negócio eterno |
| Contato | Pessoa, nome e canais nativos, papel na compra | Duplicar nome/telefone/e-mail em personalizados |
| Empresa | Organização e fatos estáveis compartilhados | Repetir cadastro do escritório em cada oportunidade |
| Etapa | Marco verificável da jornada de compra | Coluna para cada mensagem, emoção ou data |
| Campo | Informação filtrável que apoia decisão/integração | Tornar todo texto de conversa um campo obrigatório |
| Tag | Segmento/rota com uso definido | Substituir estágio ou banco de estados sem governança |
| Tarefa | Próxima ação, pessoa responsável e prazo | Guardar compromisso só em nota ou tag |
| Nota | Contexto e evidência não estruturada | Esconder dado essencial de filtro/automação |

Uma pessoa pode ter várias oportunidades legítimas. Diferencie canal de aquisição, origem técnica da linha/importação e referência comercial. Preserve first touch e last touch com definição; não sobrescreva atribuição histórica com a última sincronização.

## Funil e dicionário

Para cada etapa, definir: objetivo, evidência de entrada/saída, responsável, dado necessário naquele momento, próxima ação/SLA e gatilho/efeitos. Quantidade de etapas segue a jornada real; o exemplo de 5–7 de um playbook não é teto universal. Ganho/perda precisam de significado operacional e motivos verificáveis.

Para cada campo proposto ou existente, registrar:

`entidade | field_id | nome | grupo | tipo | enum_id/opção | finalidade | fonte | obrigatório quando | quem preenche | consumidores | decisão`

Decisão pode ser manter, renomear, reorganizar, criar, migrar, consolidar ou retirar. Prefira reutilizar semântica existente; nomes iguais não provam equivalência. Faça obrigatório no momento útil, evitando bloquear entrada com informação ainda desconhecida. Desconhecido é nulo/pendente, nunca zero ou classificação inventada. Campos derivados precisam de fórmula, origem e proprietário; evite versões manuais concorrentes.

## Migração e retirada de legado

1. Identificar entidade/ID/tipo/opções e preenchimento, incluindo múltiplos valores e amostras de exceção privadas.
2. Mapear consumidores por ID/enum: bots, gatilhos, filtros, formulários, integrações, relatórios, importadores e scripts. Registrar consumidores não inspecionados.
3. Preparar mapa origem → destino, tratamento de vazio/conflito e contagens antes/depois. Não presumir que o Kommo converte o tipo diretamente.
4. Preferir migração aditiva: criar/reutilizar destino, copiar sem perda, atualizar consumidores, reconciliar e observar. Manter legado como consulta enquanto faltar cobertura.
5. Separar retirada final num lote cuja autorização cubra exclusão e impacto. Recriar um campo removido não recupera seus valores ou dependências. Snapshot estrutural não é backup integral.

Se a retirada for prematura, entregue destino/mapa/piloto e indique a lacuna específica; não declare conclusão da migração porque o campo novo existe.

## Importação, sincronização e duplicatas

- Definir fonte de verdade por atributo e direção da sincronização; resolver conflito e exclusão lógica. Guardar chave estável de origem, lote e vínculo externo → IDs Kommo.
- Validar CSV/schema, normalização conservadora de telefone/e-mail/domínio, tipos, enums, encoding e vínculos. Não completar dados reais por adivinhação.
- Procurar correspondência exata por identificadores fortes e vínculos. Nome parecido gera candidato; telefone compartilhado pode ser recepção, não pessoa idêntica. Preservar casos ambíguos para revisão.
- Diferenciar deduplicação na entrada de fusão de registros existentes. `/api/v4/leads/complex` não é um comando genérico de merge. Confirmar método público atual; se não houver suporte, usar fluxo nativo com autorização e evidência.
- Dry-run com número de linhas válidas/rejeitadas/conflitantes; piloto representativo, retorno de IDs, leitura posterior e reexecução sem duplicar. Expandir somente após aceite e no lote autorizado.
- Volume vai para processamento determinístico local e API em lote, com paginação, cache de metadados e limites verificados. Não enviar base inteira ao modelo ou escrever célula por célula sem necessidade.

Entregue o dicionário/diff e um backlog em que cada item tenha evidência, impacto, dependência, esforço aproximado e aceite. Contagens históricas são referência; revalidar os alvos antes de aplicar.


## Exportação tabular e reconciliação entre sistemas

Para BI ou migração, preserve o grão das entidades, relações e valores multivalorados; uma junção pode duplicar o mesmo negócio. Consulte [extração e modelos](../data/extraction-and-modeling.md). Quando planilha e CRM editarem o mesmo fato, use baseline, fonte por campo e fila de conflito conforme [sincronização com Sheets](../integrations/google-sheets-sync.md), mantendo a semântica de fórmulas, vazio e pedido de limpeza.
