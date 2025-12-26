# Script rápido para testar se MySQL está funcionando
Write-Host "==========================================="
Write-Host "   TESTE RÁPIDO DO MYSQL"
Write-Host "==========================================="
Write-Host ""

# Teste 1: Porta 3306
Write-Host "1. Verificando porta 3306..."
$portCheck = netstat -ano | Select-String ":3306" | Select-String "LISTENING"
if ($portCheck) {
    Write-Host "   ✅ Porta 3306 está ouvindo" -ForegroundColor Green
} else {
    Write-Host "   ❌ Porta 3306 não está ouvindo" -ForegroundColor Red
}

# Teste 2: Processo mysqld
Write-Host ""
Write-Host "2. Verificando processo mysqld..."
$mysqldProcess = Get-Process -Name "mysqld" -ErrorAction SilentlyContinue
if ($mysqldProcess) {
    Write-Host "   ✅ Processo mysqld encontrado (PID: $($mysqldProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "   ❌ Processo mysqld não encontrado" -ForegroundColor Red
}

# Teste 3: Conexão MySQL
Write-Host ""
Write-Host "3. Testando conexão MySQL..."
$mysqlPaths = @(
    "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe",
    "mysql.exe"
)

$mysqlWorking = $false
foreach ($mysqlPath in $mysqlPaths) {
    if (Test-Path $mysqlPath) {
        try {
            # Tentar conectar sem senha primeiro (MySQL 5.7 padrão)
            $testCmd = "& '$mysqlPath' -u root -e 'SELECT 1;' 2>$null"
            $result = Invoke-Expression $testCmd
            if ($LASTEXITCODE -eq 0) {
                Write-Host "   ✅ Conexão MySQL funcionando ($mysqlPath)" -ForegroundColor Green
                $mysqlWorking = $true
                break
            }
        } catch {
            # Ignorar erros
        }
    }
}

if (-not $mysqlWorking) {
    Write-Host "   ❌ Não foi possível conectar ao MySQL" -ForegroundColor Red
}

Write-Host ""
Write-Host "==========================================="

if ($portCheck -and $mysqldProcess -and $mysqlWorking) {
    Write-Host "✅ MySQL está funcionando corretamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Agora você pode executar:"
    Write-Host "  python start.py 1"
    Write-Host ""
    Write-Host "Ou importar os dados do backup:"
    Write-Host "  powershell -ExecutionPolicy Bypass -File import_backup.ps1"
} else {
    Write-Host "❌ MySQL ainda tem problemas" -ForegroundColor Red
    Write-Host ""
    Write-Host "Consulte o GUIA_MYSQL.md para soluções"
}

Write-Host ""
