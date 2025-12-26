# Script para verificar e adicionar Python ao PATH do usuário
# Execute como Administrador se necessário

Write-Host "==========================================="
Write-Host "   VERIFICANDO PATH DO PYTHON"
Write-Host "==========================================="
Write-Host ""

# Detectar Python
$pythonPath = $null
$pythonDir = $null

# Tentar via py launcher
try {
    $pyOutput = py -c "import sys; print(sys.executable)" 2>&1
    if ($LASTEXITCODE -eq 0 -and $pyOutput) {
        $pythonPath = $pyOutput.Trim()
        $pythonDir = Split-Path -Parent $pythonPath
        Write-Host "Python detectado via py launcher:"
        Write-Host "  Caminho: $pythonPath"
        Write-Host "  Diretorio: $pythonDir"
    }
} catch {
    Write-Host "Nao foi possivel detectar Python via py launcher"
}

# Verificar PATH atual do usuário
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$pathEntries = $userPath -split ';' | Where-Object { $_ -ne '' }

Write-Host ""
Write-Host "PATH atual do usuario contem:"
$pythonInPath = $false
foreach ($entry in $pathEntries) {
    if ($entry -like "*Python*" -or $entry -like "*python*") {
        Write-Host "  OK: $entry"
        $pythonInPath = $true
    }
}

if (-not $pythonInPath) {
    Write-Host "  AVISO: Nenhum diretorio Python encontrado no PATH"
}

# Adicionar ao PATH se necessário
if ($pythonDir -and -not $pythonInPath) {
    Write-Host ""
    Write-Host "Deseja adicionar o Python ao PATH do usuario? (S/N)"
    $response = Read-Host
    
    if ($response -eq 'S' -or $response -eq 's') {
        try {
            $newPath = $userPath
            if (-not $newPath.EndsWith(';')) {
                $newPath += ';'
            }
            $newPath += $pythonDir
            
            [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
            Write-Host "Python adicionado ao PATH do usuario!"
            Write-Host ""
            Write-Host "IMPORTANTE: Feche e reabra o terminal para aplicar as mudancas."
        } catch {
            Write-Host "Erro ao adicionar ao PATH: $_"
            Write-Host ""
            Write-Host "Voce pode adicionar manualmente:"
            Write-Host "1. Abra 'Variaveis de Ambiente' (Win + R, digite: sysdm.cpl)"
            Write-Host "2. Clique em 'Variaveis de Ambiente'"
            Write-Host "3. Em 'Variaveis do usuario', edite 'Path'"
            Write-Host "4. Adicione: $pythonDir"
        }
    }
} elseif ($pythonInPath) {
    Write-Host ""
    Write-Host "Python ja esta no PATH!"
}

Write-Host ""
Write-Host "==========================================="
Write-Host "   TESTE DO PYTHON"
Write-Host "==========================================="
Write-Host ""

# Testar execução
Write-Host "Testando execucao do Python..."
if ($pythonPath) {
    try {
        $testOutput = & $pythonPath --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Python funciona corretamente: $testOutput"
        } else {
            Write-Host "Erro ao executar Python"
        }
    } catch {
        Write-Host "Erro: $_"
    }
} else {
    Write-Host "Python nao foi detectado"
}

Write-Host ""
Write-Host "Caminho completo do Python para uso no codigo:"
if ($pythonPath) {
    Write-Host "  $pythonPath"
} else {
    Write-Host "  Nao detectado"
}
Write-Host ""
