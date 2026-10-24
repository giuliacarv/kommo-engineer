# Schemas JSON em runtime

Os registros project, state, goal, acceptance, event e manifestos de snapshot são validados na leitura/escrita pela CLI no subconjunto de JSON Schema de scripts/schema_runtime.py. `project validate` também confere identidade, setup, planos e snapshots. Registro antigo fora do contrato é erro explícito, nunca correção silenciosa.

O validador usa biblioteca padrão e suporta apenas: type, required, properties, additionalProperties (booleano), items, enum, const, minimum, minItems, minLength, pattern; metadados $schema/title/description. Keywords de asserção desconhecidas são recusadas quando avaliadas. Não é implementação geral de Draft 2020-12 e não resolve $ref/composição/formats. Os schemas do pacote limitam-se a esse subconjunto.

setup-fields.json permanece contrato independente dos 18 campos; propostas, confirmações e adiamentos são distintos. IDs, evidências semânticas, permissão de conta e resultado de CRM não são provados por JSON Schema. [Workflow e migração](../references/operational-workflow.md).
