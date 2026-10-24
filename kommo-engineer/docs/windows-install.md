# Kommo Engineer — instalar no Codex Windows

Versão `0.4.0-dev`; **homologação Windows ainda não executada**. O ZIP definitivo desta revisão ainda não foi gerado.

## 1. Instalar a pasta da skill
A pasta `kommo-engineer/` contém `SKILL.md` diretamente dentro dela e todas as referências necessárias.
Selecione somente UM escopo de instalação:
- Global neste ambiente Codex: `%USERPROFILE%\.codex\skills\kommo-engineer\`
- Projeto: `<PROJETO>\.agents\skills\kommo-engineer\`

No PowerShell (exemplo global), adapte a pasta fonte:
```powershell
$skillSource = "C:\caminho\kommo-engineer"
$skillDestination = Join-Path $env:USERPROFILE ".codex\skills\kommo-engineer"
if (Test-Path -LiteralPath $skillDestination) { throw "Destino existente: compare a instalação antes de atualizar." }
if (-not (Test-Path -LiteralPath (Join-Path $skillSource "SKILL.md"))) { throw "Fonte de skill inválida." }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $skillDestination) | Out-Null
Copy-Item -LiteralPath $skillSource -Destination $skillDestination -Recurse
Test-Path -LiteralPath (Join-Path $skillDestination "SKILL.md")
```
O pacote é autocontido; não é necessário copiar a pasta externa `legado`.
Se a skill não aparecer no seletor, abra um novo chat ou reinicie o Codex. Evite duas cópias com o mesmo nome.

## 2. Python
Os recursos de gerenciamento de projeto exigem **Python 3.11+**, somente biblioteca padrão. Nos exemplos abaixo, se `py` não estiver instalado, substitua `py -3` por `python -X utf8`.
Valide no PowerShell:
```powershell
Get-Command py, python -ErrorAction SilentlyContinue
python -X utf8 --version
# Ou, quando o launcher estiver instalado:
py -3 --version
```
Um alias da Microsoft Store sem runtime funcional não serve. Se ausente, consulte
https://www.python.org/downloads/windows/ e siga as políticas do seu computador.
Não desative ExecutionPolicy global nem sandbox do Codex.

## 3. Diagnóstico
```powershell
& "$env:USERPROFILE\.codex\skills\kommo-engineer\scripts\doctor.ps1"
py -3 "$env:USERPROFILE\.codex\skills\kommo-engineer\scripts\ke.py" doctor
```
Se a política local impedir o `.ps1`, realize as sondas manuais indicadas acima.

## 4. Smoke offline SEM Kommo
A pasta de teste deve estar ausente:
```powershell
$cli = "$env:USERPROFILE\.codex\skills\kommo-engineer\scripts\ke.py"
$teste = Join-Path $env:TEMP ("ke-test-" + [guid]::NewGuid().ToString("N"))
py -3 $cli smoke prepare --project $teste --offline
py -3 $cli smoke verify --project $teste --offline
py -3 $cli project status --project $teste
```
No Codex, abra um projeto próprio e invoque `$kommo-engineer`.
Peça para retomar os dados do projeto de teste em um **novo chat**.

## 5. Uso normal
Na raiz de um projeto de cliente, invoque `$kommo-engineer`.
O primeiro setup exige coleta guiada pelo agente. Em pasta de projeto já existente, use `project init --use-existing-dir` somente após autorização explícita para anexar o contexto local; o comando preserva os arquivos existentes e não reinicializa uma pasta que já tenha dados Kommo Engineer.
Para retomar um projeto, use `project resume --project PATH`; para avançar o setup, consulte `setup status` e registre respostas com `setup update`. Campos podem ser propostos ou adiados com justificativa.
Nunca forneça token de Kommo ao chat nem ao CLI.
Se Python estiver ausente: modo orientação limitada, sem snapshot ou setup gerenciado.

## 6. Limites desta candidata
- O relatório recebido para esta revisão registra testes em ambiente Linux; isso não homologa o Codex Windows.
- O pacote não inclui acesso Kommo, navegador, Playwright ou n8n.
- Documentação dos procedimentos não equivale a homologação numa conta.
- ZIP não é atualização automática da skill anterior.
- Snapshots documentais não são backups restauráveis de CRM.

Documentação técnica de skills: https://learn.chatgpt.com/docs/build-skills
