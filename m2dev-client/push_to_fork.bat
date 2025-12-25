@echo off
chcp 65001 >nul
title M2-Dev - Push to Fork

echo ========================================
echo     PUSH PARA O FORK
echo ========================================
echo.
echo Este script vai fazer push das alteracoes
echo para o seu fork: brunao97/M2-Dev-v1
echo.

set /p token="Digite seu GitHub Personal Access Token: "

if "%token%"=="" (
    echo.
    echo ❌ Token nao fornecido!
    echo.
    pause
    exit /b 1
)

echo.
echo 🔄 Fazendo push forçado para o fork...
echo.

git push https://brunao97:%token%@github.com/brunao97/M2-Dev-v1 main --force

if %errorlevel% equ 0 (
    echo.
    echo ✅ SUCESSO! Projeto enviado para o fork!
    echo.
    echo 🌐 Verifique em: https://github.com/brunao97/M2-Dev-v1
    echo.
) else (
    echo.
    echo ❌ ERRO ao fazer push!
    echo.
    echo Verifique:
    echo - Token correto
    echo - Conexao com internet
    echo - Permissoes do token
    echo.
)

pause