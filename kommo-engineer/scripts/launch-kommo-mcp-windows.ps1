param(
    [Parameter(Mandatory)]
    [ValidatePattern('^[a-z0-9][a-z0-9-]{0,62}$')]
    [string]$Subdomain,
    [Parameter(Mandatory)]
    [string]$ServerPath
)

$ErrorActionPreference = 'Stop'
$credentialScript = Join-Path $PSScriptRoot 'kommo-credential-windows.ps1'

try {
    $entry = (Resolve-Path -LiteralPath $ServerPath -ErrorAction Stop).Path
    if (-not [System.IO.Path]::IsPathRooted($entry) -or
        [System.IO.Path]::GetFileName($entry) -ne 'index.js') {
        throw 'Informe o caminho absoluto do dist/index.js do servidor MCP revisado.'
    }

    $token = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $credentialScript -Mode Read -Subdomain $Subdomain
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($token)) {
        throw 'Credencial indisponível para a conta informada.'
    }

    $env:KOMMO_SUBDOMAIN = $Subdomain
    $env:KOMMO_ACCESS_TOKEN = $token
    $token = $null

    # STDOUT pertence ao protocolo MCP. Erros locais ficam em STDERR.
    & node $entry
    exit $LASTEXITCODE
}
catch {
    [Console]::Error.WriteLine('Kommo MCP: não foi possível iniciar. Confira o servidor, o Node e a credencial da conta.')
    exit 1
}
finally {
    Remove-Item Env:\KOMMO_ACCESS_TOKEN -ErrorAction SilentlyContinue
    Remove-Item Env:\KOMMO_SUBDOMAIN -ErrorAction SilentlyContinue
}
