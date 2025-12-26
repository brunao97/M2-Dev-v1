#!/usr/bin/env python3
import os
import json
import subprocess

def is_process_running(pid):
    """Check if a process with given PID is running"""
    try:
        import psutil
        return psutil.pid_exists(pid)
    except ImportError:
        try:
            result = subprocess.run(['tasklist', '/fi', f'PID eq {pid}'],
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0 and str(pid) in result.stdout
        except:
            return False

def check_status():
    status = {
        'database': False,
        'auth': False,
        'channels': [],
        'processes': []
    }

    print("Checking pids.json...")
    try:
        if os.path.exists('pids.json'):
            with open('pids.json', 'r') as f:
                pids_data = json.load(f)
            print(f"pids_data: {pids_data}")

            # Check database
            if 'db' in pids_data:
                db_pid = pids_data['db'].get('pid')
                print(f"DB PID: {db_pid}, Running: {is_process_running(db_pid) if db_pid else False}")
                if db_pid and is_process_running(db_pid):
                    status['database'] = True
                    status['processes'].append("db.exe")

            # Check auth
            if 'auth' in pids_data:
                auth_pid = pids_data['auth'].get('pid')
                print(f"Auth PID: {auth_pid}, Running: {is_process_running(auth_pid) if auth_pid else False}")
                if auth_pid and is_process_running(auth_pid):
                    status['auth'] = True
                    status['processes'].append("game_auth.exe")

            # Check channels
            if 'channel' in pids_data:
                print(f"Channels in pids.json: {len(pids_data['channel'])}")
                for i, channel in enumerate(pids_data['channel']):
                    channel_pid = channel.get('pid')
                    channel_name = channel.get('name', '')
                    print(f"Channel {i}: {channel_name}, PID: {channel_pid}, Running: {is_process_running(channel_pid) if channel_pid else False}")
                    if channel_pid and is_process_running(channel_pid):
                        if 'channel1_core1' in channel_name:
                            status['channels'].append("Channel 1 Core 1")
                        elif 'channel1_core2' in channel_name:
                            status['channels'].append("Channel 1 Core 2")
                        elif 'channel1_core3' in channel_name:
                            status['channels'].append("Channel 1 Core 3")
                        elif 'channel99_core1' in channel_name:
                            status['channels'].append("Channel 99 Core 1")
                        if 'channels' not in status['processes']:
                            status['processes'].append('channels')
        else:
            print("pids.json not found!")
    except Exception as e:
        print(f"Error: {e}")

    print(f"Final status: {status}")
    return status

if __name__ == "__main__":
    check_status()