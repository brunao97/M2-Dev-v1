# Script para compilar todas as quests do Metin2
Set-Location "G:\metin2-files-clean-64\M2-Dev\m2dev-server\share\locale\english\quest"

Write-Host "Compilando todas as quests..." -ForegroundColor Green

$questCount = 0
$successCount = 0
$errorCount = 0

Get-Content locale_list | ForEach-Object {
    $quest = $_.Trim()
    if ($quest -and -not $quest.StartsWith('#')) {
        Write-Host "Compilando $quest..." -ForegroundColor Yellow
        $questCount++

        try {
            & '.\qc.exe' $quest | Out-Null
            if ($LASTEXITCODE -eq 0) {
                $successCount++
                Write-Host "  OK Sucesso" -ForegroundColor Green
            } else {
                $errorCount++
                Write-Host "  ERRO Falhou (codigo: $LASTEXITCODE)" -ForegroundColor Red
            }
        } catch {
            $errorCount++
            Write-Host "  ERRO Excecao: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "=================== RESULTADO ====================" -ForegroundColor White
Write-Host "Total de quests processadas: $questCount" -ForegroundColor White
Write-Host "Sucessos: $successCount" -ForegroundColor Green
Write-Host "Erros: $errorCount" -ForegroundColor Red
Write-Host "==================================================" -ForegroundColor White