# Acessar Kommo por MCP: conexão e operação confirmadas

**Skill ≠ servidor MCP ≠ token ≠ conexão ativa.** A skill orienta; a integração concede escopos; o token carrega a autorização; o servidor implementa ferramentas; o cliente (Codex, Agy ou Claude Code) expõe o catálogo. Confira cada camada. Se já houver um MCP Kommo, comece pela inspeção do servidor e do catálogo; não crie outra integração automaticamente.

Este roteiro usa **Windows + servidor local `runitsolutions/kommo-mcp`** como exemplo completo. O projeto pode usar outro servidor, com leitura ou escrita limitada por allowlist: preserve o contrato de inicialização e os nomes reais das ferramentas. Não substitua o MCP de uma conta por outro sem conferir escopos, manutenção, capacidades e permissões.

## 1. Criar a integração na interface atual do Kommo

1. Entre na **conta correta** em `https://<subdominio>.kommo.com/` com perfil administrador. Anote o subdomínio; ele é a parte antes de `.kommo.com`.
2. Abra **Configurações → Central de integrações → + Criar integração** (em inglês, **Settings → Integrations → Create integration**). Se a UI mudar, procure a área de integrações da conta.
3. Escolha uma **integração privada**, dê um nome que identifique seu uso e, em **Permitir acesso (Allow access)**, selecione somente os escopos necessários. A interface pode vir com todos os escopos marcados por padrão; remova os que não forem necessários. Para criar ou atualizar registros, habilite o escopo de CRM/API de CRM exibido pela interface; a API também respeita os direitos do usuário e do endpoint. Não habilite conversas, envio de mensagens, arquivos ou exclusão de arquivos sem necessidade concreta. Para token de longa duração, deixe **URL de redirecionamento** vazia. Salve.
4. Abra a integração criada e a aba **Chaves e escopos** (**Keys and scopes**). Clique em **Gerar token de longa duração**, escolha a expiração e copie o token uma única vez para o armazenamento seguro. A documentação atual permite validade de **1 dia a 5 anos**; esse token não tem `refresh_token`.
5. Se o token foi colado em chat, arquivo versionado, log ou captura compartilhada, gere um substituto e revogue o exposto antes de usar a conexão.

Fontes Kommo: [integração privada](https://developers.kommo.com/docs/private-integration) e [token de longa duração](https://developers.kommo.com/docs/long-lived-token). O token longo da integração privada atua com direitos administrativos. A allowlist do MCP reduz as operações chamáveis pelo agente, mas não reduz o poder do segredo se ele vazar. Se editar escopos de uma integração já autorizada, a Kommo informa que usuários existentes precisam conceder o novo acesso novamente; confira a autorização efetiva antes de substituir a credencial. Não gere novo token só porque mudou o servidor, o catálogo ou a allowlist.

## 2. Guardar o token no Windows, sem colocá-lo no cliente MCP

Abra o PowerShell **na sua própria máquina** e execute o arquivo instalado desta skill, substituindo apenas o subdomínio. A entrada aparece mascarada. O script salva em **Gerenciador de Credenciais do Windows** como `Kommo:<subdominio>.kommo.com` e confirma por leitura sem imprimir o valor:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\SEU_USUARIO\.codex\skills\kommo-engineer\scripts\kommo-credential-windows.ps1" -Mode Install -Subdomain SUA_CONTA
```

`SEU_USUARIO` e `SUA_CONTA` são marcadores; substitua pelo caminho local real e pelo subdomínio, sem `< >`. Digite **somente o comando** no prompt `PS ...>`; cole o token **somente quando aparecer** `Cole o token ... (a entrada ficará mascarada)`. Um prompt PowerShell vazio não significa que a instalação foi executada. Se aparecer erro, o token não foi confirmado; repita após identificar a causa. Não use `$env:KOMMO_ACCESS_TOKEN` como armazenamento duradouro, `setx`, `cmdkey` com segredo no argumento, `env` nos arquivos MCP, nem cole o valor no chat.

O helper é para **token privado de longa duração no Windows**. Seu modo `Read` é de uso interno do launcher; executá-lo isoladamente escreveria o segredo na saída do terminal. Outro sistema operacional precisa de cofre e launcher equivalentes. O arquivo de configuração do cliente guarda somente caminhos e subdomínio.

## 3. Preparar o servidor MCP local

O exemplo `runitsolutions/kommo-mcp` aceita `KOMMO_SUBDOMAIN` e `KOMMO_ACCESS_TOKEN` no processo e usa `dist/index.js` após o build. Confira a origem, versão, dependências e ferramentas antes de executá-lo; ele inclui ferramentas com capacidade de escrita. Com Git e Node 20+ instalados:

```powershell
New-Item -ItemType Directory -Path C:\Tools -Force | Out-Null
git clone https://github.com/runitsolutions/kommo-mcp.git C:\Tools\kommo-mcp
Set-Location C:\Tools\kommo-mcp
npm install
npm run build
Test-Path -LiteralPath C:\Tools\kommo-mcp\dist\index.js
```

Exija `True` no último comando. Em uma instalação já existente, use o diretório real; não clone por cima. A [fonte do servidor](https://github.com/runitsolutions/kommo-mcp) declara Node 20+, `npm run build` e `dist/index.js`; verifique novamente antes de atualizar. O launcher da skill lê o token do cofre ao iniciar e o entrega **somente ao processo filho** por variável de ambiente. Ele não imprime o token e deixa stdout livre para o protocolo MCP. A variável é transitória, mas o servidor filho tem acesso a ela; revise o código que vai executar.

## 4. Registrar no cliente desejado

Use **caminhos absolutos reais** em todos os exemplos. Troque `SEU_USUARIO`, `SUA_CONTA` e `C:/Tools/kommo-mcp` pelo seu ambiente. O comando executado pelos clientes é `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <launcher> -Subdomain <conta> -ServerPath <dist/index.js>`. O launcher já está em `scripts/launch-kommo-mcp-windows.ps1` desta skill. Não inclua token nas configurações.

### Codex (app ou CLI)

Edite `C:\Users\SEU_USUARIO\.codex\config.toml`, preservando as entradas existentes:

```toml
[mcp_servers.kommo_conta]
command = "powershell.exe"
args = ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "C:/Users/SEU_USUARIO/.codex/skills/kommo-engineer/scripts/launch-kommo-mcp-windows.ps1", "-Subdomain", "SUA_CONTA", "-ServerPath", "C:/Tools/kommo-mcp/dist/index.js"]
startup_timeout_sec = 30
tool_timeout_sec = 30
```

Salve, **reinicie o Codex** e confira o servidor e as ferramentas na nova sessão (`codex mcp list` no CLI, quando disponível). Se usar `enabled_tools`, preencha **somente nomes observados** no catálogo do servidor. Quando a tarefa pede edição, inclua os nomes exatos das ferramentas de criação/atualização que o servidor oferece, junto às leituras necessárias; uma allowlist só de GET continuará impedindo edição mesmo com token autorizado. Não use curinga para contornar a inspeção. Após alterar a configuração, reinicie o Codex e confirme o catálogo. Uma entrada TOML válida não prova autenticação nem escopo.

### Agy (Google Antigravity)

No IDE, abra painel do agente **… → MCP Servers → Manage MCP Servers → View raw config**. O arquivo global documentado é `~/.gemini/config/mcp_config.json`; no workspace, `.agents/mcp_config.json`. Adicione uma entrada ao objeto `mcpServers` existente:

```json
{
  "mcpServers": {
    "kommo_conta": {
      "command": "powershell.exe",
      "args": ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "C:/Users/SEU_USUARIO/.codex/skills/kommo-engineer/scripts/launch-kommo-mcp-windows.ps1", "-Subdomain", "SUA_CONTA", "-ServerPath", "C:/Tools/kommo-mcp/dist/index.js"]
    }
  }
}
```

Se o arquivo já tem outros servidores, preserve-os e insira apenas `kommo_conta`. Recarregue o cliente e confira status/ferramentas no painel MCP ou em `/mcp` no CLI `agy`. A [documentação do Agy](https://antigravity.google/docs/mcp) define esses caminhos e o formato `mcpServers`.

### Claude Code

Para escopo local, execute **sem token na linha de comando**:

```powershell
claude mcp add --transport stdio kommo_conta -- powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\SEU_USUARIO\.codex\skills\kommo-engineer\scripts\launch-kommo-mcp-windows.ps1" -Subdomain SUA_CONTA -ServerPath "C:\Tools\kommo-mcp\dist\index.js"
claude mcp list
claude mcp get kommo_conta
```

Em uma sessão Claude Code, use `/mcp` para status e aprovação quando solicitada. `claude mcp add` apenas salva a definição; `Connected` indica transporte, e ainda falta confirmar a conta. Para escopo de projeto, `--scope project` escreve `.mcp.json`: confira o arquivo antes de versionar, mesmo que ele só tenha caminhos. [Documentação Claude Code MCP](https://code.claude.com/docs/en/mcp).

## 5. Verificar o acesso, em camadas

1. **Configuração:** o cliente mostra `kommo_conta` sem erro de arquivo/caminho.
2. **Transporte:** o servidor inicia e o cliente lista ferramentas MCP reais. Um nome de skill instalado não comprova esta etapa.
3. **Autenticação e identidade:** chame a ferramenta de conta realmente exposta, por exemplo `kommo_account_get` se ela existir, ou faça um único `GET https://<subdominio>.kommo.com/api/v4/account` com o token no processo local. Compare `id`, `name` e `subdomain` ao alvo; divergência interrompe o trabalho.
4. **Capacidade necessária:** leia um único recurso autorizado para a tarefa. A leitura da conta não prova acesso a leads, conversas, arquivos ou escrita. Para configuração, não faça registro de teste; aguarde uma tarefa concreta e autorizada antes de chamar uma ferramenta de escrita.

Registre só resultado saneado: nome da conta, ID, subdomínio, data, nome do servidor, ferramentas observadas e escopo efetivamente testado. Nunca registre o token, resposta de cliente com dados pessoais ou cabeçalho `Authorization`.

| Sintoma | Checagem direta |
|---|---|
| Só apareceu `PS ...>` | O comando ainda não foi executado; cole o comando completo e pressione Enter. |
| Entrada mascarada, depois falha ao salvar | O cofre não confirmou a gravação; repita o helper e não declare instalado. |
| MCP listado, mas sem ferramentas | Confira `dist/index.js`, Node, caminhos, stderr, aprovação e reinício do cliente. |
| Ferramenta existe, mas diz credencial ausente | Confira o alvo `Kommo:<subdominio>.kommo.com`, usuário Windows que iniciou o cliente. Reinicie somente se o servidor lê a credencial no startup ou se a configuração mudou; não peça token novo sem evidência de ausência, expiração ou revogação. |
| HTTP 401 | Confira subdomínio, expiração e revogação. Substitua no cofre somente se expiração, revogação ou incompatibilidade de conta estiver confirmada. Token longo não faz refresh OAuth. |
| HTTP 403 ou 429 | Confira escopo CRM, autorização após mudança de escopos e direitos do usuário. 403 não prova token inválido e não justifica rotação automática; 429 é limite de chamadas. |
| Conta diferente | Pare as consultas e selecione perfil MCP isolado para a conta correta. |

Um token de longa duração previamente exposto precisa ser substituído. Não tente recuperá-lo do chat, do histórico do PowerShell ou de logs.

