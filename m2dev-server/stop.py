import os
import sys
import time
import json
import subprocess
import signal
import traceback

GAMEDIR = os.getcwd()
PIDS_FILE = os.path.join(GAMEDIR, "pids.json")

def print_green(text):
	print("\033[1;32m" + text + "\033[0m")

def stop_pid(pid, name):
	try:
		if os.name == "nt":
			subprocess.call(["taskkill", "/F", "/PID", str(pid)],
			stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		else:
			os.kill(pid, signal.SIGTERM)
	except ProcessLookupError:
		print(f"> Process {pid} ({name}) not found, skipping.")
	except Exception as e:
		print(f"> Error stopping {name} (PID {pid}): {e}")
		traceback.print_exc()

def kill_by_name(name):
	try:
		if os.name == "nt":
			subprocess.call(["taskkill", "/F", "/IM", f"{name}.exe"],
			stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		else:
			subprocess.call(["pkill", "-1", name],
			stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	except Exception as e:
		print(f"> Error killing {name} by name: {e}")
		traceback.print_exc()

def force_kill_all():
	"""Força a finalização de todos os processos do servidor usando WMIC"""
	print_green("> Forçando finalização de todos os processos...")
	processes = ["game_auth", "channel1_core1", "channel1_core2", "channel1_core3", 
	             "channel99_core1", "db", "game"]
	
	if os.name == "nt":
		# Usar WMIC que tem mais privilégios
		where_clause = " or ".join([f"name='{p}.exe'" for p in processes])
		cmd = f'wmic process where "{where_clause}" delete'
		try:
			result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
			if result.returncode == 0:
				print_green("> Processos finalizados com sucesso via WMIC")
			else:
				print(f"> WMIC retornou código {result.returncode}")
		except Exception as e:
			print(f"> Erro ao usar WMIC: {e}")
	else:
		# Unix/FreeBSD
		for proc in processes:
			subprocess.call(["pkill", "-9", proc], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
	try:
		with open(PIDS_FILE, "r") as f:
			entries = json.load(f)
	except Exception as e:
		print(f"> Could not read PID file: {e}")
		print("> Tentando forçar finalização por nome de processo...")
		force_kill_all()
		sys.exit(0)
		
	for entry in entries.get("channel", []):
		name = entry.get("name")
		pid  = entry.get("pid")
		print_green(f"> Stopping {name} (PID {pid})...")
		stop_pid(pid, name)
		time.sleep(0.2)
		
	auth = entries.get("auth")
	if auth:
		print_green(f"> Stopping {auth.get('name')} (PID {auth.get('pid')})...")
		stop_pid(auth.get('pid'), auth.get('name'))
		time.sleep(1)
		
	db = entries.get("db")
	if db:
		print_green(f"> Stopping {db.get('name')} (PID {db.get('pid')})...")
		stop_pid(db.get('pid'), db.get('name'))
		
	print_green("> All requested processes signaled.")

if __name__ == "__main__":
	main()