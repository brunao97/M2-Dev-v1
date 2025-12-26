# Script para iniciar MySQL de várias formas
Write-Host "==========================================="
Write-Host "   INICIANDO MYSQL"
Write-Host "==========================================="
Write-Host ""

# Método 1: Tentar iniciar MySQL80
Write-Host "Tentando iniciar MySQL80..."
try {
    Start-Service -Name MySQL80 -ErrorAction Stop
    Start-Sleep -Seconds 3
    $portCheck = netstat -ano | Select-String ":3306" | Select-String "LISTENING"
    if ($portCheck) {
        Write-Host "SUCESSO: MySQL80 iniciado na porta 3306!" -ForegroundColor Green
        exit 0
    }
} catch {
    Write-Host "MySQL80 falhou: $($_.Exception.Message)"
}

# Método 2: Tentar iniciar MySQL57 se existir
Write-Host ""
Write-Host "Tentando iniciar MySQL57..."
try {
    Start-Service -Name MySQL57 -ErrorAction Stop
    Start-Sleep -Seconds 3
    $portCheck = netstat -ano | Select-String ":3306" | Select-String "LISTENING"
    if ($portCheck) {
        Write-Host "SUCESSO: MySQL57 iniciado na porta 3306!" -ForegroundColor Green
        exit 0
    }
} catch {
    Write-Host "MySQL57 falhou: $($_.Exception.Message)"
}

# Método 3: Iniciar MySQL 5.7 diretamente
Write-Host ""
Write-Host "Tentando iniciar MySQL 5.7 diretamente..."
$mysql57Path = "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqld.exe"
if (Test-Path $mysql57Path) {
    try {
        # Criar processo MySQL em background
        $process = Start-Process -FilePath $mysql57Path -ArgumentList "--console", "--port=3306", "--basedir=`"C:\Program Files\MySQL\MySQL Server 5.7`"", "--datadir=`"C:\Program Files\MySQL\MySQL Server 5.7\data`"" -NoNewWindow -PassThru
        Start-Sleep -Seconds 5

        $portCheck = netstat -ano | Select-String ":3306" | Select-String "LISTENING"
        if ($portCheck) {
            Write-Host "SUCESSO: MySQL 5.7 iniciado diretamente na porta 3306!" -ForegroundColor Green
            exit 0
        } else {
            Write-Host "Processo iniciado mas porta 3306 não está ouvindo"
            Stop-Process -Id $process.Id -Force 2>$null
        }
    } catch {
        Write-Host "Erro ao iniciar MySQL 5.7 diretamente: $($_.Exception.Message)"
    }
}

# Método 4: Verificar se há MySQL rodando em outra porta
Write-Host ""
Write-Host "Verificando MySQL em outras portas..."
$mysqlPorts = netstat -ano | Select-String ":330[0-9]" | Select-String "LISTENING"
if ($mysqlPorts) {
    Write-Host "Encontrado MySQL nas seguintes portas:"
    foreach ($line in $mysqlPorts) {
        Write-Host "  $line"
    }
    Write-Host ""
    Write-Host "AVISO: MySQL pode estar rodando em porta diferente de 3306!" -ForegroundColor Yellow
    Write-Host "Verifique a configuração do Metin2 em channels/db/conf/db.txt"
}

Write-Host ""
Write-Host "ERRO: Não foi possível iniciar MySQL automaticamente" -ForegroundColor Red
Write-Host ""
Write-Host "Soluções possíveis:"
Write-Host "1. Abra 'services.msc' e inicie o serviço MySQL manualmente"
Write-Host "2. Execute como administrador: net start MySQL80"
Write-Host "3. Verifique se há conflitos de porta (outro programa usando 3306)"
Write-Host "4. Reinicie o computador"
Write-Host ""

exit 1