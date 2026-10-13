# Prepara o ambiente: venv com Python 3.12, dependências do RuFaS e o clone do RuFaS v1.0.6.
# Uso (PowerShell, na raiz do projeto):  powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

$py = (& py -3.12 -c "import sys; print(sys.executable)" 2>$null)
if (-not $py) { throw "Python 3.12 nao encontrado. Instale com: winget install Python.Python.3.12" }

if (-not (Test-Path vendor\RuFaS)) {
    git -c core.longpaths=true clone --depth 1 --branch v1.0.6 https://github.com/RuminantFarmSystems/RuFaS vendor/RuFaS
}
if (-not (Test-Path .venv)) { & $py -m venv .venv }

# Tenta o pip normal; se o TLS do Python falhar com files.pythonhosted.org, baixa os pacotes com curl.
& .venv\Scripts\python -m pip install -r requirements-rufas.txt 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "pip falhou; baixando os pacotes com curl..."
    $reqs = Get-Content requirements-rufas.txt | Where-Object { $_ -and -not $_.StartsWith("#") }
    & $py scripts\fetch_wheels.py wheelhouse @reqs
    & .venv\Scripts\python -m pip install --no-index --find-links wheelhouse -r requirements-rufas.txt
}
Write-Host "Pronto. Inicie com iniciar.bat"
