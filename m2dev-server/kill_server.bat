@echo off
REM Script para matar processos do servidor Metin2
REM Execute como ADMINISTRADOR

echo =====================================
echo   MATANDO PROCESSOS DO SERVIDOR
echo =====================================
echo.

taskkill /F /IM game_auth.exe 2>nul
if %errorlevel% == 0 (
    echo [OK] game_auth.exe finalizado
) else (
    echo [INFO] game_auth.exe nao estava rodando
)

taskkill /F /IM channel1_core1.exe 2>nul
if %errorlevel% == 0 (
    echo [OK] channel1_core1.exe finalizado
) else (
    echo [INFO] channel1_core1.exe nao estava rodando
)

taskkill /F /IM channel1_core2.exe 2>nul
if %errorlevel% == 0 (
    echo [OK] channel1_core2.exe finalizado
) else (
    echo [INFO] channel1_core2.exe nao estava rodando
)

taskkill /F /IM channel1_core3.exe 2>nul
if %errorlevel% == 0 (
    echo [OK] channel1_core3.exe finalizado
) else (
    echo [INFO] channel1_core3.exe nao estava rodando
)

taskkill /F /IM channel99_core1.exe 2>nul
if %errorlevel% == 0 (
    echo [OK] channel99_core1.exe finalizado
) else (
    echo [INFO] channel99_core1.exe nao estava rodando
)

taskkill /F /IM db.exe 2>nul
if %errorlevel% == 0 (
    echo [OK] db.exe finalizado
) else (
    echo [INFO] db.exe nao estava rodando
)

taskkill /F /IM game.exe 2>nul
if %errorlevel% == 0 (
    echo [OK] game.exe finalizado
) else (
    echo [INFO] game.exe nao estava rodando
)

echo.
echo =====================================
echo   PROCESSOS FINALIZADOS
echo =====================================
echo.
pause
