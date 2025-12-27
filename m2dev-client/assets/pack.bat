@echo off
chcp 65001 >nul
title Metin2 Assets Packer

:menu
cls
echo ========================================
echo        Metin2 Assets Packer
echo ========================================
echo.
echo Digite o nome da pasta para compactar
echo (ou 'exit' para sair):
echo.
set /p folder_name="Pasta: "

if "%folder_name%"=="exit" goto exit
if "%folder_name%"=="" goto menu

echo.
echo ========================================
echo Processando pasta: %folder_name%
echo ========================================
echo.

"C:\Users\bruno\AppData\Local\Python\pythoncore-3.14-64\python.exe" pack.py "%folder_name%"

echo.
echo ========================================
echo Processo concluido!
echo ========================================
echo.
echo Pressione qualquer tecla para continuar...
pause >nul

goto menu

:exit
echo.
echo Ate logo!
timeout /t 2 >nul
exit