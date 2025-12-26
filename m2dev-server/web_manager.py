#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

GAMEDIR = os.getcwd()
PORT = 8080

class ServerManager:
    def __init__(self):
        self.gamedir = GAMEDIR

    def run_command(self, cmd, cwd=None):
        try:
            if cwd is None:
                cwd = self.gamedir
            result = subprocess.run(cmd, shell=True, cwd=cwd,
                                  capture_output=True, text=True, timeout=30)
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def check_status(self):
        status = {
            'database': False,
            'auth': False,
            'channels': [],
            'processes': []
        }

        try:
            netstat = subprocess.getoutput("netstat -ano | findstr LISTENING")
            if ":9000 " in netstat:
                status['database'] = True
            if ":11000 " in netstat:
                status['auth'] = True
            if ":11001 " in netstat:
                status['channels'].append("Channel 1 Core 1")
            if ":11002 " in netstat:
                status['channels'].append("Channel 1 Core 2")
            if ":11003 " in netstat:
                status['channels'].append("Channel 1 Core 3")
            if ":11099 " in netstat:
                status['channels'].append("Channel 99 Core 1")
        except:
            pass

        try:
            tasklist = subprocess.getoutput("tasklist /fo csv /nh")
            if "db.exe" in tasklist:
                status['processes'].append("db.exe")
            if "game_auth.exe" in tasklist:
                status['processes'].append("game_auth.exe")
            if "channel" in tasklist:
                status['processes'].append("channels")
        except:
            pass

        return status

    def get_logs(self, lines=20):
        logs = {}
        try:
            if os.path.exists("channels/db/syslog.log"):
                with open("channels/db/syslog.log", 'r', encoding='utf-8', errors='ignore') as f:
                    logs["db"] = "".join(f.readlines()[-lines:])
        except:
            logs["db"] = "Erro ao ler log"

        return logs

    def start_server(self, channels=1):
        return self.run_command(f"py start.py {channels}")

    def stop_server(self):
        return self.run_command("py stop.py")

    def restart_server(self, channels=1):
        self.stop_server()
        time.sleep(2)
        return self.start_server(channels)

class WebHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, manager=None, **kwargs):
        self.manager = manager
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.serve_html()
        elif self.path == '/api/status':
            self.api_status()
        elif self.path == '/api/logs':
            self.api_logs()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/start':
            self.api_start()
        elif self.path == '/api/stop':
            self.api_stop()
        elif self.path == '/api/restart':
            self.api_restart()
        else:
            self.send_error(404)

    def serve_html(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = """<!DOCTYPE html>
<html>
<head>
    <title>Metin2 Server Manager</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { text-align: center; background: #007acc; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .status-online { color: green; font-weight: bold; }
        .status-offline { color: red; font-weight: bold; }
        .btn { padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        .btn-primary { background: #007acc; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn-danger { background: #dc3545; color: white; }
        .btn-warning { background: #ffc107; color: black; }
        .logs { background: #1e1e1e; color: #f8f8f2; padding: 15px; border-radius: 5px; font-family: monospace; white-space: pre-wrap; max-height: 300px; overflow-y: auto; }
        .alert { padding: 10px; margin: 10px 0; border-radius: 5px; display: none; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>METIN2 SERVER MANAGER</h1>
            <p>Painel de Controle Local</p>
        </div>

        <div id="alert" class="alert"></div>

        <div class="card">
            <h3>Status do Servidor</h3>
            <div id="status-details">Carregando...</div>
            <button class="btn btn-primary" onclick="checkStatus()">Atualizar Status</button>
        </div>

        <div class="card">
            <h3>Controles do Servidor</h3>
            <div>
                <label>Canais: </label>
                <select id="channels">
                    <option value="1">1 Canal</option>
                    <option value="2">2 Canais</option>
                    <option value="3">3 Canais</option>
                    <option value="4">4 Canais</option>
                </select>
            </div>
            <div>
                <button class="btn btn-success" onclick="startServer()">Iniciar Servidor</button>
                <button class="btn btn-danger" onclick="stopServer()">Parar Servidor</button>
                <button class="btn btn-warning" onclick="restartServer()">Reiniciar Servidor</button>
            </div>
        </div>

        <div class="card">
            <h3>Logs do Servidor</h3>
            <button class="btn btn-primary" onclick="loadLogs()">Carregar Logs</button>
            <div id="logs-container" class="logs">Clique em "Carregar Logs" para ver os logs...</div>
        </div>
    </div>

    <script>
        function showAlert(message, type = 'success') {
            const alert = document.getElementById('alert');
            alert.textContent = message;
            alert.className = `alert alert-${type}`;
            alert.style.display = 'block';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 5000);
        }

        async function apiCall(endpoint, method = 'GET', data = null) {
            try {
                const config = {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                    }
                };

                if (data) {
                    config.body = JSON.stringify(data);
                }

                const response = await fetch(endpoint, config);
                const result = await response.json();
                return result;
            } catch (error) {
                showAlert('Erro: ' + error.message, 'error');
                return null;
            }
        }

        async function checkStatus() {
            const data = await apiCall('/api/status');
            if (data) {
                updateStatus(data);
            }
        }

        function updateStatus(data) {
            const statusDetails = document.getElementById('status-details');

            let html = '<ul>';
            html += `<li>Database: <span class="${data.database ? 'status-online' : 'status-offline'}">${data.database ? 'ONLINE' : 'OFFLINE'}</span></li>`;
            html += `<li>Auth Server: <span class="${data.auth ? 'status-online' : 'status-offline'}">${data.auth ? 'ONLINE' : 'OFFLINE'}</span></li>`;
            html += `<li>Channels: ${data.channels.length > 0 ? data.channels.join(', ') : 'Nenhum'}</li>`;
            html += `<li>Processos: ${data.processes.length > 0 ? data.processes.join(', ') : 'Nenhum'}</li>`;
            html += '</ul>';

            statusDetails.innerHTML = html;
        }

        async function startServer() {
            const channels = document.getElementById('channels').value;
            const data = await apiCall('/api/start', 'POST', { channels: parseInt(channels) });

            if (data && data.success) {
                showAlert(`Servidor iniciado com ${channels} canal(is)!`);
                setTimeout(checkStatus, 2000);
            } else {
                showAlert('Erro ao iniciar servidor', 'error');
            }
        }

        async function stopServer() {
            const data = await apiCall('/api/stop', 'POST');

            if (data && data.success) {
                showAlert('Servidor parado!');
                setTimeout(checkStatus, 1000);
            } else {
                showAlert('Erro ao parar servidor', 'error');
            }
        }

        async function restartServer() {
            const channels = document.getElementById('channels').value;
            const data = await apiCall('/api/restart', 'POST', { channels: parseInt(channels) });

            if (data && data.success) {
                showAlert(`Servidor reiniciado com ${channels} canal(is)!`);
                setTimeout(checkStatus, 3000);
            } else {
                showAlert('Erro ao reiniciar servidor', 'error');
            }
        }

        async function loadLogs() {
            const data = await apiCall('/api/logs');
            if (data) {
                const logsContainer = document.getElementById('logs-container');
                logsContainer.innerHTML = '';

                Object.entries(data).forEach(([key, content]) => {
                    logsContainer.innerHTML += `=== ${key.toUpperCase()} ===\\n${content}\\n\\n`;
                });
            }
        }

        // Carregar status inicial
        window.onload = function() {
            checkStatus();
        };
    </script>
</body>
</html>"""

        self.wfile.write(html.encode('utf-8'))

    def api_status(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        status = self.server.manager.check_status()
        self.wfile.write(json.dumps(status).encode('utf-8'))

    def api_logs(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        logs = self.server.manager.get_logs()
        self.wfile.write(json.dumps(logs).encode('utf-8'))

    def api_start(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        data = self.get_post_data()
        channels = data.get('channels', 1)

        result = self.server.manager.start_server(channels)
        self.wfile.write(json.dumps(result).encode('utf-8'))

    def api_stop(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        result = self.server.manager.stop_server()
        self.wfile.write(json.dumps(result).encode('utf-8'))

    def api_restart(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        data = self.get_post_data()
        channels = data.get('channels', 1)

        result = self.server.manager.restart_server(channels)
        self.wfile.write(json.dumps(result).encode('utf-8'))

    def get_post_data(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))

def run_server():
    manager = ServerManager()
    handler = lambda *args, **kwargs: WebHandler(*args, manager=manager, **kwargs)

    server = HTTPServer(('localhost', PORT), handler)
    server.manager = manager

    print(f"Servidor web iniciado em http://localhost:{PORT}")
    print("Acesse o painel no navegador")
    print("Pressione Ctrl+C para parar")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Servidor parado")
        server.shutdown()

if __name__ == "__main__":
    run_server()