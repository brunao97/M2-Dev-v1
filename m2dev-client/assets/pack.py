#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
import sys
import argparse
import time
from concurrent.futures import ThreadPoolExecutor

# Configurações
output_folder_path = "../pack"
packmaker_exe = "PackMaker.exe"
IGNORE_FOLDERS = {
    "zz_ignore_old",
    ".git",
    "__pycache__"
}


def pack_folder(folder_path):
    folder_name = os.path.basename(folder_path)

    # Verifica se a pasta existe
    if not os.path.exists(folder_name):
        print(f"ERRO: Pasta '{folder_name}' nao existe")
        return False

    # Verifica se há arquivos na pasta
    try:
        files = os.listdir(folder_name)
        if not files:
            print(f"AVISO: Pasta '{folder_name}' esta vazia, pulando...")
            return False
    except PermissionError:
        print(f"ERRO: Sem permissao para acessar '{folder_name}'")
        return False

    print(f"Empacotando {folder_name}...")

    try:
        start_time = time.time()

        # Executa o PackMaker
        result = subprocess.run([
            packmaker_exe,
            "--input", folder_name,
            "--output", output_folder_path
        ], check=True, capture_output=True, text=True)

        end_time = time.time()
        duration = end_time - start_time

        # Verifica se o arquivo foi criado e obtém o tamanho
        output_file = os.path.join(output_folder_path, f"{folder_name}.pck")
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            size_mb = file_size / (1024 * 1024)
            print(".2f")
        else:
            print(f"OK {folder_name}.pck criado com sucesso (tempo: {duration:.1f}s)")

        return True

    except subprocess.CalledProcessError as e:
        print(f"ERRO: Falha ao empacotar {folder_name}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"ERRO: PackMaker.exe nao encontrado no diretorio atual")
        return False
    except Exception as e:
        print(f"ERRO inesperado ao empacotar {folder_name}: {e}")
        return False

def pack_all_folders():
    # Obtém todas as pastas válidas
    all_folders = []
    for item in os.listdir():
        if os.path.isdir(item) and item not in IGNORE_FOLDERS and not item.startswith('.'):
            all_folders.append(item)

    if not all_folders:
        print("ERRO: Nenhuma pasta encontrada para empacotar!")
        return

    total_folders = len(all_folders)
    print(f"Encontradas {total_folders} pastas para empacotar")
    print("=" * 50)

    # Processa sequencialmente para melhor controle e feedback
    success_count = 0
    total_start_time = time.time()

    for i, folder in enumerate(all_folders, 1):
        print(f"[{i}/{total_folders}] ", end="")
        if pack_folder(folder):
            success_count += 1
        print()

    total_end_time = time.time()
    total_duration = total_end_time - total_start_time

    print("=" * 50)
    print("PROCESSO CONCLUIDO!")
    print(f"Resultado: {success_count}/{total_folders} pacotes criados com sucesso")
    print(".1f")
    # Lista os arquivos criados
    if os.path.exists(output_folder_path):
        pck_files = [f for f in os.listdir(output_folder_path) if f.endswith('.pck')]
        if pck_files:
            total_size = sum(os.path.getsize(os.path.join(output_folder_path, f)) for f in pck_files)
            total_size_mb = total_size / (1024 * 1024)

            print("\nArquivos criados:")
            for pck_file in sorted(pck_files):
                file_path = os.path.join(output_folder_path, pck_file)
                file_size = os.path.getsize(file_path)
                size_mb = file_size / (1024 * 1024)
                print(".2f")

def main():
    print("Metin2 Assets Packer")
    print("=" * 30)

    # Verifica se estamos no diretório correto
    if not os.path.exists("PackMaker.exe"):
        print("ERRO: PackMaker.exe nao encontrado!")
        print("Execute este script dentro da pasta assets/")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Empacota pastas do Metin2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python pack.py --all                    # Empacota todas as pastas
  python pack.py PC                      # Empacota apenas a pasta PC
  python pack.py Monster                 # Empacota apenas a pasta Monster
        """
    )
    parser.add_argument("folder_name", nargs="?", help="Nome da pasta para empacotar")
    parser.add_argument("--all", action="store_true", help="Empacota todas as pastas")

    args = parser.parse_args()

    # Cria a pasta de saída se não existir
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        print(f"📁 Pasta {output_folder_path} criada")

    print()

    if args.all:
        pack_all_folders()
    elif args.folder_name:
        folder_path = os.path.join(os.getcwd(), args.folder_name)
        pack_folder(folder_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
