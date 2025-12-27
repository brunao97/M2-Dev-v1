# Script para verificar qual processo está usando uma porta específica
param([int]$Port = 8080)

Write-Host "==========================================="
Write-Host "   VERIFICANDO PROCESSO NA PORTA $Port"
Write-Host "==========================================="
Write-Host ""

# Obter informações da porta
$netstat = netstat -ano | Select-String ":$Port" | Select-String "LISTENING"

if ($netstat) {
    Write-Host "Conexões encontradas na porta $Port`:"
    $netstat | ForEach-Object {
        $line = $_.Line
        # Extrair PID (último campo)
        $fields = $line -split '\s+'
        $pid = $fields[$fields.Length - 1]

        Write-Host "Linha: $line"
        Write-Host "PID identificado: $pid"

        # Obter informações do processo
        try {
            $process = Get-Process -Id $pid -ErrorAction Stop
            Write-Host "Processo: $($process.ProcessName)"
            Write-Host "ID: $($process.Id)"
            Write-Host "Caminho: $($process.Path)"
            Write-Host "Tempo de início: $($process.StartTime)"
            Write-Host ""
        } catch {
            Write-Host "Não foi possível obter informações do processo PID $pid"
            Write-Host ""
        }
    }
} else {
    Write-Host "Nenhuma conexão LISTENING encontrada na porta $Port"
    Write-Host ""
}

# Verificar também conexões estabelecidas
$established = netstat -ano | Select-String ":$Port" | Select-String "ESTABLISHED"
if ($established) {
    Write-Host "Conexões estabelecidas na porta $Port`:"
    $established | Select-Object -First 3 | ForEach-Object {
        Write-Host "  $($_.Line)"
    }
    Write-Host ""
}

Write-Host "Para liberar a porta, execute:"
Write-Host "Stop-Process -Id <PID> -Force"
Write-Host ""
Read-Host "Pressione Enter para continuar"