import sys
sys.dont_write_bytecode = True

import os
import time
import json
import subprocess
import traceback
import socket
import channels

GAMEDIR = os.getcwd()
PIDS_FILE = os.path.join(GAMEDIR, "pids.json")
IS_WINDOWS = (os.name == "nt")

def print_green(text):
	print("\033[1;32m" + text + "\033[0m")

def print_magenta_prompt():
	print("\033[0;35m> ", end="", flush=True)

def run_powershell(script_name):
	"""Runs a PowerShell script located in the current directory."""
	script_path = os.path.join(GAMEDIR, script_name)
	if not os.path.exists(script_path):
		print(f"> ERROR: Script not found: {script_path}")
		return False
	
	try:
		cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path]
		# Redirect stdout/stderr to pass them through or capture them
		result = subprocess.run(cmd, check=False)
		return result.returncode == 0
	except Exception as e:
		print(f"> Failed to run {script_name}: {e}")
		return False

def check_mysql_port(host='127.0.0.1', port=3306, timeout=1):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(timeout)
		result = sock.connect_ex((host, port))
		sock.close()
		return result == 0
	except:
		return False

def check_db_data_exists_win():
	"""
	Heuristic check for Windows: Check if the 'account' folder exists 
	in the standard MySQL 5.7 data directory.
	"""
	# Common paths for MySQL 5.7 Data on Windows
	possible_paths = [
		r"C:\ProgramData\MySQL\MySQL Server 5.7\Data\account",
		r"C:\Program Files\MySQL\MySQL Server 5.7\data\account"
	]
	
	for path in possible_paths:
		if os.path.exists(path):
			return True
	return False

def manage_mysql_windows():
	print_green("> Checking MySQL status (Windows)...")
	
	# 1. Check if Data exists (Heuristic)
	# If we can't find the data directory, we assume it might be missing or custom location.
	# But if we DO find the path and it's missing 'account', we definitely need to restore.
	data_exists = check_db_data_exists_win()
	
	if not data_exists:
		print("> WARNING: 'account' database not found in standard locations.")
		print("> Attempting to restore backup...")
		if run_powershell("import_backup.ps1"):
			print_green("> Backup restore script finished.")
			data_exists = True # Assume success
		else:
			print("> ERROR: Backup restore failed.")
	else:
		print_green("> Database data found.")

	# 2. Check if running
	if check_mysql_port():
		print_green("> MySQL is online.")
		return True
	
	print("> MySQL is offline. Attempting to start...")
	if run_powershell("start_mysql.ps1"):
		print_green("> MySQL start script finished.")
	
	# Final check
	if check_mysql_port():
		print_green("> MySQL is now online.")
		return True
	else:
		print("> ERROR: MySQL still offline after start attempt.")
		return False

def start_process(exe):
	return subprocess.Popen([exe], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def try_start(name, cd, exe, pids, key=None):
	try:
		original_dir = os.getcwd()
		
		if not os.path.exists(cd):
			print(f"> ERROR: Directory not found: {cd}")
			return False
		
		os.chdir(cd)

		exe_path = exe
		if IS_WINDOWS and not exe_path.endswith('.exe'):
			exe_path = exe + ".exe"

		if not os.path.exists(exe_path):
			print(f"> ERROR: Executable not found: {exe_path}")
			os.chdir(original_dir)
			return False

		abs_exe_path = os.path.abspath(exe_path)
		proc = start_process(abs_exe_path)

		time.sleep(1.0)
		if proc.poll() is not None:
			try:
				stderr_output = proc.stderr.read().decode('utf-8', errors='ignore') if proc.stderr else "No stderr available"
				print(f"> ERROR: Process {name} exited immediately with code: {proc.returncode}")
				if stderr_output:
					print(f"> Error output: {stderr_output[:200]}")
			except:
				pass
			return False

		entry = {"name": name, "pid": proc.pid}

		if key:
			pids.setdefault(key, []).append(entry)
		else:
			pids[name] = entry

		os.chdir(original_dir)
		return True
	except Exception as e:
		print(f"> Failed to start {name}: {e}")
		traceback.print_exc()
		try:
			os.chdir(original_dir)
		except:
			pass
		return False

def main():
	# --- System Initialization ---
	if IS_WINDOWS:
		if not manage_mysql_windows():
			print("> CRITICAL: Could not ensure MySQL is running. Server start aborted.")
			sys.exit(1)
	else:
		# FreeBSD / Linux Placeholder
		print("> Checking MySQL (Unix)...")
		if not check_mysql_port():
			print("> WARNING: MySQL port 3306 is closed. Please start MySQL service.")
			# On FreeBSD: os.system("service mysql-server start")
		else:
			print_green("> MySQL is online.")

	# --- Channel Selection ---
	if len(sys.argv) == 1:
		print_green("> How many channels to start?")
		print_magenta_prompt()
		try:
			user_input = int(input())
		except ValueError:
			print("> Invalid number.")
			sys.exit(1)
	else:
		try:
			user_input = int(sys.argv[1])
		except ValueError:
			print("> Invalid argument.")
			sys.exit(1)

	pids = {}

	try:
		print_green("> Starting database...")
		db_started = try_start(
			"db",
			os.path.join(GAMEDIR, "channels", "db"),
			"./db",
			pids
		)
		if not db_started:
			print("> WARNING: Database may not have started correctly")
		time.sleep(2)

		print_green("> Starting auth...")
		auth_started = try_start(
			"auth",
			os.path.join(GAMEDIR, "channels", "auth"),
			"./game_auth",
			pids
		)
		if not auth_started:
			print("> ERROR: Auth failed to start! Check syserr.log in channels/auth/")
		time.sleep(2)

		int_channel_map = {int(k): v for k, v in channels.CHANNEL_MAP.items()}
		channels_to_start = set()
		
		if 1 in int_channel_map:
			channels_to_start.add(1)
		if 99 in int_channel_map:
			channels_to_start.add(99)
		
		for channel_id in int_channel_map.keys():
			if channel_id in [1, 99]:
				continue
			if user_input and channel_id <= user_input:
				channels_to_start.add(channel_id)
			elif not user_input:
				channels_to_start.add(channel_id)

		final_start_order = sorted(list(channels_to_start))

		for channel_id in final_start_order:
			cores = int_channel_map[channel_id]
			print_green(f"> Starting CH{channel_id}:")
			channel_started = False
			for core_id, maps in cores.items():
				name = f"channel{channel_id}_core{core_id}"
				print_green(f"\t> {name}")
				core_started = try_start(
					name,
					os.path.join(GAMEDIR, "channels", f"channel{channel_id}", f"core{core_id}"),
					f"./{name}",
					pids,
					"channel"
				)
				if core_started:
					channel_started = True
				else:
					print(f"\t> ERROR: {name} failed to start! Check syserr.log")
				time.sleep(1)
			
			if not channel_started:
				print(f"> ERROR: Channel {channel_id} failed to start!")
			print()

		print_green("> The server is running!")

	except Exception as e:
		print(f"> Unexpected error: {e}")
		traceback.print_exc()

	finally:
		os.chdir(GAMEDIR)
		try:
			with open(PIDS_FILE, "w") as f:
				json.dump(pids, f, indent=2)
			print_green(f"> PID file written to {PIDS_FILE}")

		except Exception as e:
			print(f"> Failed to write PID file: {e}")
			traceback.print_exc()

if __name__ == "__main__":
	main()