# Gera a interface web (Next.js, exportação estática) e publica o resultado em frontend/.
# Requer Node.js 20.9+ e acesso ao registro npm na primeira execução.
#
# O build roda numa pasta FORA do OneDrive (%LOCALAPPDATA%\dietopt-web-build): o node_modules tem
# centenas de MB e milhares de arquivos, e o Next.js não lida bem com o "Á" de "Área de Trabalho".
# Quem só executa o sistema não precisa do Node: o resultado já fica em frontend/.
#
# Uso (PowerShell, na raiz do projeto):  powershell -ExecutionPolicy Bypass -File scripts\build-web.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$build = Join-Path $env:LOCALAPPDATA "dietopt-web-build"
New-Item -ItemType Directory -Force $build | Out-Null

# Sincroniza as fontes (preserva node_modules entre builds).
robocopy "$root\web" $build /MIR /XD node_modules .next out /XF next-env.d.ts /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy falhou (código $LASTEXITCODE)" }

Push-Location $build
try {
    npm install --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) { throw "npm install falhou" }
    npm run build
    if ($LASTEXITCODE -ne 0) { throw "npm run build falhou" }
}
finally {
    Pop-Location
}

# Publica em frontend/ (a primeira versão da interface, em HTML puro, fica guardada em frontend_legacy/).
$dest = Join-Path $root "frontend"
$legacy = Join-Path $root "frontend_legacy"
if (Test-Path $dest) {
    if (-not (Test-Path $legacy)) { Rename-Item $dest "frontend_legacy" } else { Remove-Item $dest -Recurse -Force }
}
Copy-Item (Join-Path $build "out") $dest -Recurse
Copy-Item (Join-Path $build "package-lock.json") (Join-Path $root "web\package-lock.json") -Force
Write-Host "Interface publicada em $dest"
