# Arquitetura Kommo: decisão em duas camadas

## 1. Arquitetura da solução
Compare nativo/Digital Pipeline, Salesbot visual, Salesbot código, Marketplace,
n8n/webhooks/API e customizado. Busque a solução mais simples que atenda requisitos,
segurança, observabilidade, capacidade de recuperação e necessidade de operação comercial.

## 2. Método de implantação
Para cada componente já escolhido, compare API oficial, navegador, execução assistida,
integração instalada e scripts. Uma automação nativa pode ser implantada via interface.

## Preflight obrigatório para alterar conta
- Conta, subdomínio e ambiente confirmados; IDs provenientes da conta correta.
- Plano, canal, permissões, integração instalada e endpoint verificados.
- Pré-requisitos e dependências previstos.
- Efeito esperado, reversibilidade e aprovações definidos.
- Evidência de leitura antes/depois disponível.
- Retries seguros; após timeout de criação, **não repetir POST** sem pesquisar o destino.

## Escolha econômica
Menor custo total por tarefa aceita, não apenas menos tokens nesta tentativa.
Registre recomendação + alternativa quando trade-off importante. Não invente pesos numéricos.
