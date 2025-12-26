# Script completo para configurar MySQL 5.7 para Metin2
# Execute como Administrador

$ErrorActionPreference = "Stop"

Write-Host "==========================================="
Write-Host "   CONFIGURANDO MYSQL 5.7 PARA METIN2"
Write-Host "==========================================="
Write-Host ""

# Encontrar MySQL
$mysqlPath = "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe"
if (-not (Test-Path $mysqlPath)) {
    Write-Host "ERRO: MySQL não encontrado em $mysqlPath"
    Write-Host "Por favor, verifique a instalação do MySQL 5.7"
    exit 1
}

Write-Host "MySQL encontrado: $mysqlPath"

# Encontrar serviço MySQL
$mysqlService = Get-Service -Name "MySQL57" -ErrorAction SilentlyContinue
if (-not $mysqlService) {
    $mysqlService = Get-Service | Where-Object { $_.Name -like "*MySQL*" -and $_.Status -eq 'Running' } | Select-Object -First 1
}

if (-not $mysqlService) {
    Write-Host "ERRO: Serviço MySQL não encontrado!"
    exit 1
}

Write-Host "Serviço MySQL: $($mysqlService.Name) - Status: $($mysqlService.Status)"
Write-Host ""

# Verificar se MySQL está rodando
if ($mysqlService.Status -ne 'Running') {
    Write-Host "Iniciando serviço MySQL..."
    Start-Service -Name $mysqlService.Name
    Start-Sleep -Seconds 5
}

# Solicitar senha root
Write-Host "Por favor, informe a senha do usuário root do MySQL:"
$rootPassword = Read-Host -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($rootPassword)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Executar setup SQL
Write-Host ""
Write-Host "Criando bancos de dados e usuário..."
$setupScript = Join-Path $PSScriptRoot "setup_mysql57.sql"
$setupArgs = "-u", "root", "-p$plainPassword", "-e", "source $setupScript"

try {
    & $mysqlPath $setupArgs
    Write-Host "✓ Bancos de dados e usuário criados com sucesso!"
} catch {
    Write-Host "ERRO ao executar setup: $_"
    exit 1
}

# Importar estruturas SQL
Write-Host ""
Write-Host "Importando estruturas SQL..."
$sqlFiles = @(
    "sql\account.sql",
    "sql\common.sql",
    "sql\player.sql",
    "sql\log.sql"
)

foreach ($sqlFile in $sqlFiles) {
    $fullPath = Join-Path $PSScriptRoot $sqlFile
    if (Test-Path $fullPath) {
        Write-Host "  Importando: $sqlFile"
        $importArgs = "-u", "root", "-p$plainPassword", "-e", "source $fullPath"
        try {
            & $mysqlPath $importArgs 2>&1 | Out-Null
            Write-Host "    ✓ $sqlFile importado"
        } catch {
            Write-Host "    ⚠ Aviso ao importar $sqlFile: $_"
        }
    }
}

Write-Host ""
Write-Host "==========================================="
Write-Host "   CONFIGURAÇÃO CONCLUÍDA"
Write-Host "==========================================="
Write-Host ""
Write-Host "Próximos passos:"
Write-Host "1. Se você tem dados no backup (C:\MySQL\data_backup), execute:"
Write-Host "   .\import_backup.ps1"
Write-Host "2. Compile o servidor:"
Write-Host "   cd ..\m2dev-server-src\build"
Write-Host "   cmake --build . --target game --config Release"
Write-Host "3. Reinicie o servidor"
Write-Host ""
