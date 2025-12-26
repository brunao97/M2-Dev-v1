# Script para verificar e iniciar MySQL 5.7
Write-Host "==========================================="
Write-Host "   VERIFICANDO MYSQL 5.7"
Write-Host "==========================================="
Write-Host ""

# Verificar se porta 3306 está em uso
$port3306 = netstat -ano | Select-String ":3306" | Select-String "LISTENING"
if ($port3306) {
    Write-Host "OK: Porta 3306 está em LISTENING" -ForegroundColor Green
    $pid = ($port3306 -split '\s+')[-1]
    Write-Host "  PID: $pid"
    
    try {
        $process = Get-Process -Id $pid -ErrorAction Stop
        Write-Host "  Processo: $($process.ProcessName)"
        Write-Host "  Caminho: $($process.Path)"
    } catch {
        Write-Host "  Aviso: Não foi possível obter detalhes do processo"
    }
} else {
    Write-Host "ERRO: Porta 3306 não está em LISTENING" -ForegroundColor Red
    Write-Host ""
    
    # Tentar encontrar serviço MySQL
    $mysqlServices = Get-Service | Where-Object { $_.Name -like "*MySQL*" }
    
    if ($mysqlServices) {
        Write-Host "Serviços MySQL encontrados:"
        foreach ($service in $mysqlServices) {
            Write-Host "  - $($service.Name): $($service.Status)"
        }
        Write-Host ""
        
        # Tentar iniciar o primeiro serviço MySQL encontrado
        $mysqlService = $mysqlServices | Select-Object -First 1
        if ($mysqlService.Status -ne 'Running') {
            Write-Host "Tentando iniciar serviço: $($mysqlService.Name)"
            try {
                Start-Service -Name $mysqlService.Name
                Start-Sleep -Seconds 3
                $mysqlService = Get-Service -Name $mysqlService.Name
                if ($mysqlService.Status -eq 'Running') {
                    Write-Host "OK: Serviço iniciado com sucesso!" -ForegroundColor Green
                } else {
                    Write-Host "ERRO: Serviço não iniciou. Status: $($mysqlService.Status)" -ForegroundColor Red
                }
            } catch {
                Write-Host "ERRO: Não foi possível iniciar o serviço: $_" -ForegroundColor Red
                Write-Host ""
                Write-Host "Tente iniciar manualmente:"
                Write-Host "  net start $($mysqlService.Name)"
                Write-Host "  ou"
                Write-Host "  Start-Service -Name $($mysqlService.Name)"
            }
        }
    } else {
        Write-Host "ERRO: Nenhum serviço MySQL encontrado!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Verifique se o MySQL 5.7 está instalado corretamente."
    }
}

Write-Host ""
Write-Host "==========================================="
