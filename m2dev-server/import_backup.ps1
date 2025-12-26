# Script para importar dados do backup MariaDB para MySQL 5.7
# Execute como Administrador

$mysqlPath = "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe"
$backupPath = "C:\MySQL\data_backup"
$mysqlDataPath = "C:\ProgramData\MySQL\MySQL Server 5.7\Data"

Write-Host "==========================================="
Write-Host "   IMPORTANDO DADOS DO BACKUP"
Write-Host "==========================================="
Write-Host ""

# Verificar se o MySQL está rodando
$mysqlService = Get-Service -Name "MySQL57" -ErrorAction SilentlyContinue
if (-not $mysqlService) {
    $mysqlService = Get-Service | Where-Object { $_.Name -like "*MySQL*" } | Select-Object -First 1
}

if ($mysqlService) {
    Write-Host "Serviço MySQL encontrado: $($mysqlService.Name)"
    if ($mysqlService.Status -ne 'Running') {
        Write-Host "Iniciando serviço MySQL..."
        Start-Service -Name $mysqlService.Name
        Start-Sleep -Seconds 5
    }
} else {
    Write-Host "ERRO: Serviço MySQL não encontrado!"
    exit 1
}

# Verificar se o backup existe
if (-not (Test-Path $backupPath)) {
    Write-Host "ERRO: Backup não encontrado em $backupPath"
    Write-Host "Por favor, verifique o caminho do backup."
    exit 1
}

Write-Host "Backup encontrado em: $backupPath"
Write-Host ""

# Parar o MySQL para copiar os dados
Write-Host "Parando serviço MySQL..."
Stop-Service -Name $mysqlService.Name -Force
Start-Sleep -Seconds 3

# Copiar dados do backup
Write-Host "Copiando dados do backup..."
Write-Host "Origem: $backupPath"
Write-Host "Destino: $mysqlDataPath"

if (Test-Path $mysqlDataPath) {
    # Fazer backup do data atual (caso exista)
    $backupCurrent = "$mysqlDataPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Write-Host "Fazendo backup do data atual para: $backupCurrent"
    Copy-Item -Path $mysqlDataPath -Destination $backupCurrent -Recurse -Force
}

# Copiar bancos de dados do backup
$databases = @("account", "common", "log", "player")
foreach ($db in $databases) {
    $sourceDb = Join-Path $backupPath $db
    $destDb = Join-Path $mysqlDataPath $db
    
    if (Test-Path $sourceDb) {
        Write-Host "Copiando banco: $db"
        Copy-Item -Path $sourceDb -Destination $destDb -Recurse -Force
    } else {
        Write-Host "Aviso: Banco $db não encontrado no backup"
    }
}

# Iniciar MySQL novamente
Write-Host ""
Write-Host "Iniciando serviço MySQL..."
Start-Service -Name $mysqlService.Name
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "==========================================="
Write-Host "   IMPORTAÇÃO CONCLUÍDA"
Write-Host "==========================================="
Write-Host ""
Write-Host "Próximos passos:"
Write-Host "1. Execute: mysql -u root -p < setup_mysql57.sql"
Write-Host "2. Verifique se os dados foram importados corretamente"
Write-Host "3. Compile o servidor novamente"
Write-Host ""
