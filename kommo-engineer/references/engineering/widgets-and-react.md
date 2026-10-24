# Widgets Kommo, React, callbacks e pacote

Use para criar ou revisar uma interface embutida, integração privada com UI, pacote importável ou serviço de apoio a widget. Aprofunda [integrações e widgets](../crm/automation-integrations.md); não transforma componente web genérico em widget instalável.

## Separar artefatos e contratos

Mantenha explícitos: manifest e metadados; script do widget; estilos/imagens/i18n; callbacks e contexto do SDK; componente React; backend e armazenamento; autenticação; pacote de produção. Escolha somente os componentes necessários ao pedido. Um gerador pode criar pastas e instalar dependências; executá-lo é uma ação de desenvolvimento distinta de consultar o template.

Registre release/commit do gerador e versões compatíveis do runtime/SDK. Evite `@latest` como requisito permanente de uma implementação que precisa ser reproduzível. Use o gerador atual apenas quando solicitado e disponível, conferindo o diretório de saída antes de criar arquivos.

## Manifest e callbacks

Confira locais de instalação, idioma, versão, parâmetros, nomes de tradução e arquivos referenciados pelo contrato atual da Kommo. Não habilite `everywhere` por conveniência quando apenas uma tela precisa do widget. Chave de i18n ausente, script no lugar errado ou callback não registrado podem deixar um pacote importável e inutilizável.

A fonte usa um wrapper `Integration.addCallback`. Nele, callbacks aninhados podem usar ponto, enquanto a documentação do SDK apresenta outra notação. Esse mapeamento pertence ao wrapper e à versão observada; não transponha sua sintaxe diretamente para qualquer SDK.

| Momento | Responsabilidade a verificar |
|---|---|
| Renderização/inicialização | Contexto correto e contêiner único; não duplicar montagem ao reabrir |
| Ligação de ações | Handler instalado uma vez; tratar requisição pendente, erro e clique repetido |
| Configurações/salvamento | Validar parâmetros e diferenciar proposta de valor persistido |
| Seleção/navegação | Reavaliar entidade, conta e permissão; não reutilizar estado de outro lead |
| Destruição | Desmontar raiz React, listeners, timers, observers e requisições quando apropriado |

Um callback de destruição vazio no template não prova limpeza. Isole CSS e identidade do contêiner para evitar colisão com a aplicação hospedeira. Considere tema, idioma, listas vazias e mudança de cartão somente quando afetarem o fluxo.

## Frontend e backend

Mantenha segredo privilegiado no backend. Variável de ambiente incorporada pelo bundler pode acabar no JavaScript público; o nome `.env` não torna seu conteúdo secreto. Inspecione o pacote de saída, não apenas o código fonte.

Defina rotas e credenciais por conta. Para OAuth, registre contexto da autorização, validação do retorno e armazenamento protegido dos tokens. Um JSON local no servidor de demonstração não define uma política de produção; a rotação deve persistir o novo par de tokens com controle de concorrência.

Quando o contrato envolver JWT e `return_url`, valide assinatura e claims pertinentes, conta, prazo e destino autorizado conforme a documentação vigente. Não envie Bearer para qualquer URL recebida; valide host, esquema e redirecionamentos antes da chamada. CORS aberto não autentica um webhook. Evite logs de body bruto, token decodificado e resposta contendo dados pessoais.

ACK de webhook e chamada de retorno são etapas diferentes. Se a continuidade precisar sobreviver a reinício, registre a operação antes do ACK e reconcilie timeout/retorno duplicado. Não trate status 200 do seu servidor como conclusão do Salesbot.

## Pacote e aceite

Conferir o ZIP de produção: caminhos esperados, manifest válido para o produto, traduções e imagens presentes, script compatível e ausência de segredos, arquivos de desenvolvimento ou dependência acidental do servidor local. Um build que desativa lint não equivale ao build revisado; declare quais verificações rodaram.

Prove instalação/configuração em conta autorizada, renderização, ação principal, erro e reabertura. Verifique que destruir/reabrir não duplica listeners ou escritas. Teste o backend separadamente e leia de volta o efeito no CRM. Guarde versão anterior e procedimento de desativação; ZIP gerado não prova instalação.

Origem metodológica: [EXT-002](../external-sources.md#ext-002). Síntese própria; o código do gerador e do template não foi redistribuído. A fonte possui licença customizada com condições adicionais para reutilização de seu software.
