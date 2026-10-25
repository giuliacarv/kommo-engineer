# Habilitar escrita controlada em MCP Kommo

Use este guia quando a tarefa precisar criar ou editar registros Kommo pelo Codex, Agy/Antigravity, Claude Code ou outro cliente MCP.

## Não misture as camadas

- **Integração Kommo:** escopos concedidos em Permitir acesso. O escopo CRM permite usar a API de CRM conforme direitos da conta.
- **Token:** autentica a integração e a conta. Um token válido não implementa nem publica ferramentas.
- **Servidor MCP:** precisa implementar a operação, método HTTP e schema da tool.
- **Cliente:** precisa carregar o servidor e deixar visíveis as ferramentas necessárias.
- **Pedido humano:** define quais registros e mudanças estão autorizados. Habilitar uma tool não autoriza alterar dados.

Uma conexão que lista apenas GET é somente leitura, mesmo que a integração Kommo tenha escopo CRM. Quando a pessoa pede edição, não deixe a configuração em leitura por padrão: habilite ferramentas pontuais de criação/atualização que o servidor implementa. Não habilite ferramentas não solicitadas como exclusão, mensagens, automação ou lote.

## Corrigir ou criar a integração

1. Confirme a conta e use perfil administrador.
2. Na interface atual, abra **Configurações → Central de integrações**. Para integração nova, clique **+ Criar integração**, selecione privada e, em **Permitir acesso / Allow access**, habilite os escopos necessários.
3. Para trabalhar com leads, contatos e empresas, permita acesso ao CRM. Confirme a etiqueta exata exibida na interface; outras capacidades, como arquivos, notificações ou conversas, são escopos separados e não devem ser marcadas sem necessidade.
4. Para uma integração existente, abra sua configuração e use **Editar**; reveja **Chaves e escopos**. Não crie outra integração apenas porque o catálogo do MCP está sem tools de escrita.
5. A Kommo informa que uma mudança de escopos pode exigir que usuários já autorizados concedam acesso novamente. Confira a autorização efetiva. Um token longo é criado na aba **Chaves e escopos**, usa os direitos administrativos e não tem refresh token. Gere substituto somente quando a autorização existente não tiver o escopo necessário, estiver revogada/expirada ou a conta/token estiver incorreto. Instale no cofre local com entrada mascarada; não peça nem registre o segredo no chat.

Fontes oficiais: [integração privada](https://developers.kommo.com/docs/private-integration), [permissões](https://developers.kommo.com/docs/permissions) e [token de longa duração](https://developers.kommo.com/docs/long-lived-token).

## Descobrir e expor as tools certas

1. Inspecione a configuração instalada e o catálogo real do servidor; leia schemas, descrições, anotações, método HTTP, endpoint, campos aceitos, limites e comportamento de erro. Não deduza tool de escrita pela documentação ou nome do pacote.
2. Confirme que o servidor implementa as operações pedidas. Se não implementar, escolha um servidor compatível ou implemente a capacidade com allowlist de entidades, rotas, métodos e campos. Não contorne o servidor chamando API arbitrária sem rever segurança e recuperação.
3. No cliente, inclua apenas os nomes reais das tools necessários. O Codex aceita uma allowlist enabled_tools na configuração local. Para o MCP Metha deste projeto, os nomes observados são:

       kommo_account_get
       kommo_pipelines_list
       kommo_custom_fields_list
       kommo_records_search
       kommo_record_get
       kommo_record_create
       kommo_record_update

   Exemplo de linha TOML para esse servidor:

       enabled_tools = ["kommo_account_get", "kommo_pipelines_list", "kommo_custom_fields_list", "kommo_records_search", "kommo_record_get", "kommo_record_create", "kommo_record_update"]

Estes nomes são específicos desse servidor; confira o catálogo antes de copiá-los a outro projeto. Reinicie ou recarregue o cliente depois de alterar configuração. Não use allowlist curinga para esconder uma configuração sem inspeção.
4. Agy e Claude Code recebem as capacidades anunciadas pelo servidor conectado. A configuração de transporte apenas registra o servidor; se a interface oferecer allowlist, use nomes confirmados no catálogo. Confirmação de uso da ferramenta na interface não limita o poder do token se o servidor ou segredo for comprometido.
5. Confirme por leitura a identidade da conta antes de consultar registros. Anote servidor/versão, transporte, subdomínio e tools observadas, sem guardar o token ou dados pessoais desnecessários.

## Executar uma alteração autorizada

- **Atualização:** leia o registro pelo ID, valide vínculos e valores, compare a versão/timestamp se a tool oferecer controle de concorrência, envie apenas os campos pedidos e faça readback.
- **Criação:** valide os dados e procure possíveis duplicidades antes do POST. Se o resultado do POST for incerto, reconcilie a conta antes de tentar novamente.
- **Escopo:** uma operação por registro quando o usuário pediu edição pontual. Não transforme em lote nem inclua outros registros por inferência.
- **Resultado incerto:** não repita POST/PATCH cegamente. Releia o ID ou pesquise o efeito esperado e só então determine se aplicar de novo é seguro.
- **Configuração sem tarefa de CRM:** conferir a conexão e catálogo é suficiente; não crie registro real de teste.

Um pedido concreto como “atualize o lead 123 para o estágio X” autoriza essa alteração delimitada. “Habilite acesso de edição” autoriza configurar o caminho técnico, mas não escolher um lead e alterá-lo.

## Diagnóstico sem pedir token em loop

| Sinal | Causa provável e próxima checagem |
|---|---|
| Catálogo tem só GET | O servidor ou allowlist do cliente está em leitura. Corrija tools/código/configuração; token novo não cria tools. |
| Tool de escrita não aparece no Codex | Confira enabled_tools, nomes exatos do catálogo e reinicie o Codex. |
| Leitura de conta funciona, escrita retorna 403 | Confirme escopo CRM, reautorização após mudança de escopos, direito do usuário e endpoint. Não trate 403 como token inválido. |
| HTTP 401 | Confirme conta, expiração e revogação; só então substitua a credencial no cofre. |
| PowerShell pede token em cada chamada | Descubra se o servidor está relendo o cofre corretamente ou se uma instância antiga cacheou credencial. Não gere tokens repetidos antes de localizar a causa. |
| Tool lista, mas operação falha | Revise schema, campos obrigatórios, vínculos, permissões, resposta HTTP e readback. Não repita payload inválido nem exponha resposta com dados pessoais. |

A criação ou edição documentada aqui é capacidade configurada, não prova de que uma escrita foi autorizada ou executada na conta. Relate separadamente catálogo, autenticação, escopos e alteração observada.
