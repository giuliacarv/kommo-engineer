# Diagnóstico local, sem instalação de dependências ou uso de rede.
$ErrorActionPreference = "Continue"
$candidates = @("py", "python")
$valid = $false
foreach ($name in $candidates) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if (-not $cmd) { continue }
    $arg = if ($name -eq "py") { @("-3", "-c", "import sys; print(sys.version_info[:3]); raise SystemExit(sys.version_info < (3,11))") } else { @("-c", "import sys; print(sys.version_info[:3]); raise SystemExit(sys.version_info < (3,11))") }
    & $name @arg
    if ($LASTEXITCODE -eq 0) { $valid = $true; Write-Output "Python compatível via $name"; break }
}
if (-not $valid) { Write-Error "Python 3.11+ não encontrado. Instale pela fonte oficial e repita."; exit 2 }
exit 0
