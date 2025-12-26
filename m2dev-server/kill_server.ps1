# Script para matar todos os processos do servidor Metin2
# Execute como ADMINISTRADOR

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  MATANDO PROCESSOS DO SERVIDOR" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Lista de processos para matar
$processes = @("game_auth", "channel1_core1", "channel1_core2", "channel1_core3", "channel99_core1", "db", "game")

$killed = 0
$notFound = 0

foreach ($proc in $processes) {
    try {
        $running = Get-Process -Name $proc -ErrorAction SilentlyContinue
        
        if ($running) {
            Write-Host "[MATANDO] $proc (PID: $($running.Id))..." -ForegroundColor Yellow
            Stop-Process -Name $proc -Force -ErrorAction Stop
            $killed++
            Write-Host "  ✓ Processo $proc finalizado com sucesso" -ForegroundColor Green
        } else {
            Write-Host "[INFO] $proc não está em execução" -ForegroundColor Gray
            $notFound++
        }
    } catch {
        Write-Host "  ✗ Erro ao matar $proc : $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Processos finalizados: $killed" -ForegroundColor Green
Write-Host "Processos não encontrados: $notFound" -ForegroundColor Gray
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pressione qualquer tecla para sair..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
