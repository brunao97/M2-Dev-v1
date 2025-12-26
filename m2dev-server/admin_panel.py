import os
import sys
import time
import json
import subprocess
import signal

# Configurações de cores para Windows
C_GREEN = "\033[1;32m"
C_RED = "\033[1;31m"
C_YELLOW = "\033[1;33m"
C_CYAN = "\033[1;36m"
C_MAGENTA = "\033[1;35m"
C_WHITE = "\033[1;37m"
C_RESET = "\033[0m"

# Caminho do servidor (ajuste conforme necessário)
GAMEDIR = os.getcwd()

def print_color(text, color=C_GREEN):
    print(f"{color}{text}{C_RESET}")

def banner():
    art = f"""{C_MAGENTA}
      _   _   __  __ _____ ____ ____
     | | / \ |  \/  | ____/ ___|___ \
  _  | |/ _ \| |\/| |  _| \___ \ __) |
 | |_| / ___ \ |  | | |___ ___) / __/
  \___/_/   \_\_|  |_|_____|____/_____|

    {C_CYAN}      >>> PAINEL DE CONTROLE <<<{C_RESET}
    """
    print(art)

def run_command(cmd, cwd=GAMEDIR):
    try:
        subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print_color(f"ERRO ao executar: {cmd}\n{e}", C_RED)

def check_status():
    print_color("\n📊 --- STATUS DO SERVIDOR --- 📊", C_CYAN)
    processes = {
        "Database (DB)": 9000,
        "Auth Server": 11000,
        "CH1 Core 1": 11001,
        "CH1 Core 2": 11002,
        "CH1 Core 3": 11003,
        "CH99 Core 1": 11099
    }

    # Verifica portas ativas no Windows
    try:
        output = subprocess.getoutput("netstat -ano | findstr LISTENING")
    except:
        output = ""

    # Verifica processos em execução
    try:
        tasklist = subprocess.getoutput("tasklist /fi \"imagename eq db.exe\" /nh")
        has_db = "db.exe" in tasklist

        tasklist = subprocess.getoutput("tasklist /fi \"imagename eq game_auth.exe\" /nh")
        has_auth = "game_auth.exe" in tasklist

        tasklist = subprocess.getoutput("tasklist /fi \"imagename eq channel*.exe\" /nh")
        has_channels = "channel" in tasklist
    except:
        has_db = has_auth = has_channels = False

    found_online = 0
    for name, port in processes.items():
        port_active = f":{port} " in output
        process_active = False

        if "Database" in name and has_db:
            process_active = True
        elif "Auth" in name and has_auth:
            process_active = True
        elif "CH" in name and has_channels:
            process_active = True

        if port_active and process_active:
            print(f"  {C_GREEN}✅ ONLINE  {C_WHITE}>> {C_CYAN}{name.ljust(15)}{C_WHITE} (Porta {port}){C_RESET}")
            found_online += 1
        elif port_active or process_active:
            print(f"  {C_YELLOW}⚠️  PARCIAL {C_WHITE}>> {C_YELLOW}{name.ljust(15)}{C_WHITE} (Porta {port}){C_RESET}")
        else:
            print(f"  {C_RED}❌ OFFLINE {C_WHITE}>> {C_RED}{name.ljust(15)}{C_WHITE} (Porta {port}){C_RESET}")

    if found_online == 0:
        print_color("\n⚠️  Nenhum processo do servidor detectado.", C_YELLOW)
    elif found_online == len(processes):
        print_color("\n💎 Todos os sistemas estão operacionais!", C_GREEN)
    else:
        print_color(f"\n⚡ {found_online}/{len(processes)} sistemas online.", C_YELLOW)

def start_server():
    print_color("\n🚀 --- INICIAR SERVIDOR --- 🚀", C_CYAN)
    try:
        canas = input(f"{C_WHITE}Quantos canais deseja iniciar? (1-4) [{C_GREEN}Padrão: 1{C_WHITE}]: {C_RESET}")
        if not canas:
            canas = "1"

        print_color(f"⏳ Iniciando {canas} canal(is)...", C_YELLOW)
        # Chamando o start.py original com o argumento
        subprocess.run(f"py start.py {canas}", shell=True, cwd=GAMEDIR)

        print_color("📡 Aguardando estabilização dos processos...", C_YELLOW)
        for i in range(5, 0, -1):
            print(f"  {i}...", end="\r")
            time.sleep(1)

        check_status()
    except KeyboardInterrupt:
        print_color("\n⚠️ Operação cancelada.", C_RED)

def stop_server():
    print_color("\n🛑 --- PARAR SERVIDOR --- 🛑", C_CYAN)
    print_color("⏳ Encerrando processos...", C_YELLOW)

    # Tenta pelo script oficial primeiro
    run_command("py stop.py")

    # Garante o encerramento no Windows (Força Bruta)
    run_command("taskkill /f /im db.exe")
    run_command("taskkill /f /im game_auth.exe")
    run_command("taskkill /f /im channel*.exe")

    print_color("✅ Todos os processos foram finalizados.", C_GREEN)

def clear_logs():
    print_color("\n🧹 --- LIMPAR LOGS --- 🧹", C_CYAN)
    run_command("py clear.py")
    # Limpa arquivos temporários do Windows
    run_command("del /q channels\\*\\*.log 2>nul")
    run_command("del /q channels\\*\\*.core 2>nul")
    run_command("del /q *.core 2>nul")
    print_color("✨ Logs e arquivos temporários limpos!", C_GREEN)

def main_menu():
    while True:
        os.system("cls")
        banner()
        print(f" {C_WHITE}1){C_RESET} 🚀 Iniciar Servidor")
        print(f" {C_WHITE}2){C_RESET} 🛑 Parar Servidor")
        print(f" {C_WHITE}3){C_RESET} 🔄 Reiniciar (Stop + Clear + Start)")
        print(f" {C_WHITE}4){C_RESET} 🧹 Limpar Logs")
        print(f" {C_WHITE}5){C_RESET} 📊 Status do Servidor")
        print(f" {C_WHITE}0){C_RESET} 🚪 Sair")
        print_color("\n====================================", C_CYAN)

        try:
            choice = input(f"{C_MAGENTA}👉 Escolha uma opção: {C_RESET}")

            if choice == "1":
                start_server()
                input(f"\n{C_WHITE}Pressione {C_GREEN}Enter{C_WHITE} para voltar...{C_RESET}")
            elif choice == "2":
                stop_server()
                input(f"\n{C_WHITE}Pressione {C_GREEN}Enter{C_WHITE} para voltar...{C_RESET}")
            elif choice == "3":
                stop_server()
                clear_logs()
                start_server()
                input(f"\n{C_WHITE}Pressione {C_GREEN}Enter{C_WHITE} para voltar...{C_RESET}")
            elif choice == "4":
                clear_logs()
                input(f"\n{C_WHITE}Pressione {C_GREEN}Enter{C_WHITE} para voltar...{C_RESET}")
            elif choice == "5":
                check_status()
                input(f"\n{C_WHITE}Pressione {C_GREEN}Enter{C_WHITE} para voltar...{C_RESET}")
            elif choice == "0":
                print_color("👋 Saindo do painel Metin2. Até logo!", C_MAGENTA)
                break
            else:
                print_color("❌ Opção inválida!", C_RED)
                time.sleep(1)
        except KeyboardInterrupt:
            print_color("\n👋 Saindo...", C_MAGENTA)
            break

if __name__ == "__main__":
    main_menu()