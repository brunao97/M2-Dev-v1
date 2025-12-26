const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const GAMEDIR = process.cwd();
const PORT = 8080;

class ServerManager {
    constructor() {
        this.gamedir = GAMEDIR;
        this.pidsFile = path.join(this.gamedir, "pids.json");
        this.pythonPath = null; // Will be detected on first use
        this.debugLogPath = path.join(this.gamedir, "web_manager_debug.log");
        this.debugLog("--- ServerManager Initialized ---");
    }

    debugLog(msg) {
        const timestamp = new Date().toISOString();
        const logMsg = `[${timestamp}] ${msg}\n`;
        console.log(logMsg.trim());
        try {
            fs.appendFileSync(this.debugLogPath, logMsg);
        } catch (e) {
            console.error('Failed to write to debug log:', e.message);
        }
    }

    async getPythonPath() {
        // If already detected, return it
        if (this.pythonPath) {
            return this.pythonPath;
        }

        // Known Python path from system detection
        const knownPaths = [
            'C:\\Users\\bruno\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe', // Detected path
            'C:\\Users\\bruno\\AppData\\Local\\Python\\bin\\python.exe', // Alternative path
            'C:\\Python313\\python.exe',
            'C:\\Python312\\python.exe',
            'C:\\Python311\\python.exe'
        ];

        // Try known paths first (fastest)
        for (const pythonPath of knownPaths) {
            try {
                const result = await this.runCommand(`"${pythonPath}" --version`);
                if (result.success || result.returncode === 0) {
                    this.pythonPath = pythonPath;
                    console.log(`[Python] Using known path: ${this.pythonPath}`);
                    return this.pythonPath;
                }
            } catch (e) {
                continue;
            }
        }

        // Try to detect Python path using py launcher
        try {
            const result = await this.runCommand('py -c "import sys; print(sys.executable)"');
            if (result.success && result.stdout && result.stdout.trim()) {
                const detectedPath = result.stdout.trim();
                // Verify the detected path exists
                const fs = require('fs');
                if (fs.existsSync(detectedPath)) {
                    this.pythonPath = detectedPath;
                    console.log(`[Python] Detected Python at: ${this.pythonPath}`);
                    return this.pythonPath;
                }
            }
        } catch (e) {
            console.log('[Python] Failed to detect Python via py launcher:', e.message);
        }

        // Try generic python.exe (if in PATH)
        try {
            const result = await this.runCommand('python.exe --version');
            if (result.success || result.returncode === 0) {
                this.pythonPath = 'python.exe';
                console.log(`[Python] Using python.exe from PATH`);
                return this.pythonPath;
            }
        } catch (e) {
            // Ignore
        }

        // Last resort: use py launcher
        this.pythonPath = 'py';
        console.log('[Python] Using py launcher as fallback');
        return this.pythonPath;
    }

    async runCommand(cmd, cwd = null, timeoutMs = null) {
        return new Promise((resolve) => {
            if (!cwd) cwd = this.gamedir;

            // Determine timeout based on command type
            let timeout = timeoutMs;
            if (!timeout) {
                if (cmd.includes('start.py')) {
                    timeout = 120000; // 2 minutes for server startup
                } else if (cmd.includes('tasklist') || cmd.includes('netstat') || cmd.includes('findstr')) {
                    timeout = 5000; // 5 seconds for quick system commands
                } else {
                    timeout = 30000; // 30 seconds default
                }
            }

            console.log(`[runCommand] Executing: ${cmd} in ${cwd} (timeout: ${timeout}ms)`);

            const child = spawn(cmd, {
                cwd,
                shell: true,
                stdio: ['pipe', 'pipe', 'pipe']
            });

            let stdout = '';
            let stderr = '';

            child.stdout.on('data', (data) => { 
                const text = data.toString();
                stdout += text;
                // Only log if not a quick command (to reduce spam)
                if (timeout > 5000) {
                    console.log(`[stdout] ${text.trim()}`);
                }
            });
            
            child.stderr.on('data', (data) => { 
                const text = data.toString();
                stderr += text;
                // Only log errors for quick commands
                if (timeout <= 5000 && text.trim()) {
                    console.log(`[stderr] ${text.trim()}`);
                }
            });

            child.on('error', (error) => {
                console.error(`[runCommand] Error spawning process: ${error.message}`);
                resolve({
                    success: false,
                    returncode: -1,
                    stdout,
                    stderr: stderr || error.message,
                    error: error.message
                });
            });

            const timeoutHandle = setTimeout(() => {
                if (!child.killed) {
                    console.log(`[runCommand] Timeout after ${timeout}ms, killing process`);
                    child.kill();
                    resolve({ success: false, error: 'Timeout', stdout, stderr });
                }
            }, timeout);

            child.on('close', (code) => {
                clearTimeout(timeoutHandle);
                if (timeout > 5000) {
                    this.debugLog(`[runCommand] Process exited with code: ${code}`);
                }
                resolve({
                    success: code === 0,
                    returncode: code,
                    stdout,
                    stderr
                });
            });
        });
    }

    async isProcessRunning(pid) {
        if (!pid) return false;
        try {
            const { stdout } = await this.runCommand(`tasklist /FI "PID eq ${pid}" /NH`, null, 3000);
            return stdout && stdout.includes(pid.toString());
        } catch {
            return false;
        }
    }

    async clearLogs() {
        const pythonPath = await this.getPythonPath();
        const scriptPath = path.join(this.gamedir, 'clear.py');
        const cmd = `"${pythonPath}" "${scriptPath}"`;
        console.log(`[clearLogs] Executing: ${cmd}`);
        return await this.runCommand(cmd);
    }

    async checkStatus() {
        const status = {
            mysql: false,
            database: false,
            auth: false,
            channels: [],
            processes: [],
            stats: { accounts: 0, players: 0 }
        };

        try {
            // MySQL check - verificar processo mysqld e porta 3306
            const mysqlProcessCheck = await this.runCommand('tasklist /FI "IMAGENAME eq mysqld.exe" /NH');
            const mysqlPortCheck = await this.runCommand('netstat -ano | findstr ":3306" | findstr LISTENING');
            const mysqlRunning = mysqlProcessCheck.stdout.includes('mysqld.exe') || mysqlPortCheck.stdout.includes(':3306');

            // Tentar conectar ao MySQL se processo estiver rodando
            if (mysqlRunning) {
                try {
                    // Tentar múltiplos caminhos possíveis do MySQL
                    const mysqlPaths = [
                        'C:\\MySQL\\bin\\mysql.exe',
                        'C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe',
                        'C:\\Program Files\\MySQL\\MySQL Server 8.1\\bin\\mysql.exe',
                        'C:\\Program Files\\MariaDB\\bin\\mysql.exe',
                        'mysql.exe'
                    ];
                    
                    let mysqlConnected = false;
                    for (const mysqlPath of mysqlPaths) {
                        try {
                            const mysqlCheck = await this.runCommand(`powershell -Command "& '${mysqlPath}' -u root -e 'SELECT 1;'" 2>&1`);
                            if (mysqlCheck.success && !mysqlCheck.stderr.includes('ERROR') && !mysqlCheck.stdout.includes('ERROR')) {
                                mysqlConnected = true;
                                
                                // Buscar estatísticas
                                const accountStats = await this.runCommand(`powershell -Command "& '${mysqlPath}' -u root -e 'SELECT COUNT(*) FROM account.account;'" 2>&1`);
                                const playerStats = await this.runCommand(`powershell -Command "& '${mysqlPath}' -u root -e 'SELECT COUNT(*) FROM player.player;'" 2>&1`);
                                
                                const accountMatch = accountStats.stdout.match(/(\d+)/);
                                const playerMatch = playerStats.stdout.match(/(\d+)/);
                                
                                status.stats.accounts = accountMatch ? parseInt(accountMatch[1]) : 0;
                                status.stats.players = playerMatch ? parseInt(playerMatch[1]) : 0;
                                break;
                            }
                        } catch (e) {
                            // Continuar tentando outros caminhos
                            continue;
                        }
                    }
                    status.mysql = mysqlConnected;
                } catch (e) {
                    console.log('MySQL connection check error:', e.message);
                    // Se processo está rodando mas não consegue conectar, ainda marca como online
                    status.mysql = mysqlRunning;
                }
            } else {
                status.mysql = false;
            }

            // Verificar processos por nome e porta
            const { stdout: netstat } = await this.runCommand('netstat -ano | findstr LISTENING');
            
            // Database check - processo db.exe e porta 9000
            const dbProcessCheck = await this.runCommand('tasklist /FI "IMAGENAME eq db.exe" /NH');
            const dbPortCheck = new RegExp(':9000\\s+.*LISTENING', 'i').test(netstat);
            status.database = dbProcessCheck.stdout.toLowerCase().includes('db.exe') || dbPortCheck;

            // Auth check - processo game_auth.exe e porta 11000
            const authProcessCheck = await this.runCommand('tasklist /FI "IMAGENAME eq game_auth.exe" /NH');
            const authPortCheck = new RegExp(':11000\\s+.*LISTENING', 'i').test(netstat);
            status.auth = authProcessCheck.stdout.toLowerCase().includes('game_auth.exe') || authPortCheck;

            // Channel check - verificar processos e portas
            const channelConfig = {
                'CH1': { ports: [':11001', ':11002', ':11003'], processes: ['channel1_core1.exe', 'channel1_core2.exe', 'channel1_core3.exe'] },
                'CH2': { ports: [':12001', ':12002', ':12003'], processes: ['channel2_core1.exe', 'channel2_core2.exe', 'channel2_core3.exe'] },
                'CH3': { ports: [':13001', ':13002', ':13003'], processes: ['channel3_core1.exe', 'channel3_core2.exe', 'channel3_core3.exe'] },
                'CH4': { ports: [':14001', ':14002', ':14003'], processes: ['channel4_core1.exe', 'channel4_core2.exe', 'channel4_core3.exe'] },
                'CH99': { ports: [':11099'], processes: ['channel99_core1.exe'] }
            };

            for (const [ch, config] of Object.entries(channelConfig)) {
                let portOnline = false;
                for (const port of config.ports) {
                    const portRegex = new RegExp(`${port}\\s+.*LISTENING`, 'i');
                    if (portRegex.test(netstat)) {
                        portOnline = true;
                        break;
                    }
                }
                
                // Verificar processos pelo nome (check each process individually)
                let processOnline = false;
                for (const processName of config.processes) {
                    const processCheck = await this.runCommand(`tasklist /FI "IMAGENAME eq ${processName}" /NH`, null, 3000);
                    if (processCheck.stdout && processCheck.stdout.toLowerCase().includes(processName.toLowerCase())) {
                        processOnline = true;
                        break;
                    }
                }
                
                // Verificar via PID se disponível
                if (!processOnline && fs.existsSync(this.pidsFile)) {
                    try {
                        const pids = JSON.parse(fs.readFileSync(this.pidsFile, 'utf-8'));
                        if (pids.channel) {
                            const chNum = ch.replace('CH', '');
                            for (const chData of pids.channel) {
                                if (chData.name && chData.name.toLowerCase().includes(`channel${chNum}_core`)) {
                                    if (await this.isProcessRunning(chData.pid)) {
                                        processOnline = true;
                                        break;
                                    }
                                }
                            }
                        }
                    } catch (e) {
                        // Ignorar erros de leitura do PID
                    }
                }
                
                if (portOnline || processOnline) {
                    if (!status.channels.some(c => c.toUpperCase() === ch)) {
                        status.channels.push(ch);
                    }
                }
            }

            // Fallback: verificar via PID se ainda não detectado
            if (fs.existsSync(this.pidsFile)) {
                try {
                    const pids = JSON.parse(fs.readFileSync(this.pidsFile, 'utf-8'));
                    
                    if (!status.database && pids.db && await this.isProcessRunning(pids.db.pid)) {
                        status.database = true;
                    }
                    if (!status.auth && pids.auth && await this.isProcessRunning(pids.auth.pid)) {
                        status.auth = true;
                    }
                    
                    // Verificar canais via PID como fallback
                    if (pids.channel && status.channels.length === 0) {
                        const channelMap = {
                            'channel1': 'CH1',
                            'channel2': 'CH2',
                            'channel3': 'CH3',
                            'channel99': 'CH99'
                        };
                        
                        for (const ch of pids.channel) {
                            if (await this.isProcessRunning(ch.pid)) {
                                const chName = (ch.name || '').toLowerCase();
                                for (const [pattern, chId] of Object.entries(channelMap)) {
                                    if (chName.includes(pattern) && !status.channels.includes(chId)) {
                                        status.channels.push(chId);
                                        break;
                                    }
                                }
                            }
                        }
                    }
                } catch (e) {
                    console.log('Error reading pids.json:', e.message);
                }
            }

        } catch (error) {
            console.error('Error in checkStatus:', error);
        }

        return status;
    }

    async getLogs(lines = 50) {
        const logs = {};
        const logPaths = {
            db: path.join(this.gamedir, 'channels', 'db', 'syserr.log'),
            auth: path.join(this.gamedir, 'channels', 'auth', 'syserr.log'),
            ch1: path.join(this.gamedir, 'channels', 'channel1', 'core1', 'syserr.log')
        };

        for (const [key, logPath] of Object.entries(logPaths)) {
            try {
                if (fs.existsSync(logPath)) {
                    const content = fs.readFileSync(logPath, 'utf-8').split('\n');
                    logs[key] = content.slice(-lines).join('\n');
                } else {
                    logs[key] = 'Nenhum log erro encontrado.';
                }
            } catch (e) {
                logs[key] = 'Erro ao ler: ' + e.message;
            }
        }
        return logs;
    }

    async startServer(channels = 1) {
        // Get Python path (will detect automatically on first call)
        const pythonPath = await this.getPythonPath();
        
        // Ensure channels 1 and 99 are always started (obligatory)
        // The start.py script will handle this, but we pass the number anyway
        const scriptPath = path.join(this.gamedir, 'start.py');
        const cmd = `"${pythonPath}" "${scriptPath}" ${channels}`;
        
        console.log(`[startServer] Executing: ${cmd}`);
        const result = await this.runCommand(cmd);
        
        // Check if there were any errors
        if (!result.success) {
            console.error('Start server error:', result.stderr || result.stdout);
            // If Python path detection failed, try to re-detect
            if (result.stderr && result.stderr.includes('Python') && result.stderr.includes('não foi encontrado')) {
                console.log('[startServer] Python not found, clearing cache and re-detecting...');
                this.pythonPath = null;
                const newPythonPath = await this.getPythonPath();
                const retryCmd = `"${newPythonPath}" "${scriptPath}" ${channels}`;
                console.log(`[startServer] Retrying with: ${retryCmd}`);
                return await this.runCommand(retryCmd);
            }
        }
        
        return result;
    }

    async stopServer() {
        this.debugLog("Stopping server...");
        
        // Get Python path (will detect automatically on first call)
        const pythonPath = await this.getPythonPath();
        const scriptPath = path.join(this.gamedir, 'stop.py');
        const cmd = `"${pythonPath}" "${scriptPath}"`;
        
        this.debugLog(`Executing script: ${cmd}`);
        let result = await this.runCommand(cmd);
        
        // List processes before force kill
        const beforeKill = await this.runCommand('powershell -Command "Get-Process | Where-Object { $_.Name -like \'channel*\' -or $_.Name -like \'game*\' -or $_.Name -eq \'db\' } | Select-Object Name, Id | Format-Table -HideTableHeaders"');
        this.debugLog("Processes found before force kill:\n" + beforeKill.stdout);

        // Final force kill for all Metin2 related processes on Windows using PowerShell for maximum reliability
        this.debugLog("Executing final force kill via PowerShell...");
        const psKill = 'powershell -Command "Get-Process | Where-Object { $_.Name -like \'channel*\' -or $_.Name -like \'game*\' -or $_.Name -eq \'db\' } | Stop-Process -Force -ErrorAction SilentlyContinue"';
        await this.runCommand(psKill);
        
        // Wait a small moment
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // List processes after force kill
        const afterKill = await this.runCommand('powershell -Command "Get-Process | Where-Object { $_.Name -like \'channel*\' -or $_.Name -like \'game*\' -or $_.Name -eq \'db\' } | Select-Object Name, Id | Format-Table -HideTableHeaders"');
        this.debugLog("Processes found after force kill:\n" + (afterKill.stdout.trim() || "None (All cleared)"));

        // Clean up pids.json
        if (fs.existsSync(this.pidsFile)) {
            try { this.debugLog("Deleting pids.json"); fs.unlinkSync(this.pidsFile); } catch(e) { this.debugLog("Error deleting pids.json: " + e.message); }
        }
        
        return { success: true };
    }

    async restartServer(channels = 1) {
        await this.stopServer();
        await new Promise(resolve => setTimeout(resolve, 2000));
        await this.clearLogs();
        await new Promise(resolve => setTimeout(resolve, 1000));
        return this.startServer(channels);
    }
}

const manager = new ServerManager();

// HTML Interface
const htmlTemplate = `<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <title>Metin2 Manager</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Geist:wght@100;300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: { sans: ['Geist', 'Inter', 'sans-serif'] },
                    colors: {
                        border: "hsl(240 3.7% 15.9%)",
                        input: "hsl(240 3.7% 15.9%)",
                        ring: "hsl(240 4.9% 83.9%)",
                        background: "hsl(240 10% 3.9%)",
                        foreground: "hsl(0 0% 98%)",
                        primary: {
                            DEFAULT: "hsl(0 0% 98%)",
                            foreground: "hsl(240 5.9% 10%)"
                        },
                        secondary: {
                            DEFAULT: "hsl(240 3.7% 15.9%)",
                            foreground: "hsl(0 0% 98%)"
                        },
                        destructive: {
                            DEFAULT: "hsl(0 62.8% 30.6%)",
                            foreground: "hsl(0 0% 98%)"
                        },
                        muted: {
                            DEFAULT: "hsl(240 3.7% 15.9%)",
                            foreground: "hsl(240 5% 64.9%)"
                        },
                        accent: {
                            DEFAULT: "hsl(240 3.7% 15.9%)",
                            foreground: "hsl(0 0% 98%)"
                        },
                        card: {
                            DEFAULT: "hsl(240 10% 3.9%)",
                            foreground: "hsl(0 0% 98%)"
                        }
                    }
                }
            }
        }
    </script>
    <style>
        :root {
            --background: 240 10% 3.9%;
            --foreground: 0 0% 98%;
            --card: 240 10% 3.9%;
            --card-foreground: 0 0% 98%;
            --primary: 0 0% 98%;
            --primary-foreground: 240 5.9% 10%;
            --secondary: 240 3.7% 15.9%;
            --secondary-foreground: 0 0% 98%;
            --muted: 240 3.7% 15.9%;
            --muted-foreground: 240 5% 64.9%;
            --accent: 240 3.7% 15.9%;
            --accent-foreground: 0 0% 98%;
            --destructive: 0 62.8% 30.6%;
            --destructive-foreground: 0 0% 98%;
            --border: 240 3.7% 15.9%;
            --input: 240 3.7% 15.9%;
            --ring: 240 4.9% 83.9%;
        }

        .dark {
            --background: 240 10% 3.9%;
            --foreground: 0 0% 98%;
            --card: 240 10% 3.9%;
            --card-foreground: 0 0% 98%;
            --primary: 0 0% 98%;
            --primary-foreground: 240 5.9% 10%;
            --secondary: 240 3.7% 15.9%;
            --secondary-foreground: 0 0% 98%;
            --muted: 240 3.7% 15.9%;
            --muted-foreground: 240 5% 64.9%;
            --accent: 240 3.7% 15.9%;
            --accent-foreground: 0 0% 98%;
            --destructive: 0 62.8% 30.6%;
            --destructive-foreground: 0 0% 98%;
            --border: 240 3.7% 15.9%;
            --input: 240 3.7% 15.9%;
            --ring: 240 4.9% 83.9%;
        }

        body {
            background-color: hsl(var(--background));
            color: hsl(var(--foreground));
            height: 100vh;
            overflow: hidden;
        }

        .bg-card { background-color: hsl(var(--card)); }
        .text-card-foreground { color: hsl(var(--card-foreground)); }
        .bg-primary { background-color: hsl(var(--primary)); }
        .text-primary { color: hsl(var(--primary)); }
        .text-primary-foreground { color: hsl(var(--primary-foreground)); }
        .bg-secondary { background-color: hsl(var(--secondary)); }
        .text-secondary { color: hsl(var(--secondary)); }
        .text-secondary-foreground { color: hsl(var(--secondary-foreground)); }
        .bg-muted { background-color: hsl(var(--muted)); }
        .text-muted-foreground { color: hsl(var(--muted-foreground)); }
        .bg-accent { background-color: hsl(var(--accent)); }
        .text-accent-foreground { color: hsl(var(--accent-foreground)); }
        .bg-destructive { background-color: hsl(var(--destructive)); }
        .text-destructive { color: hsl(var(--destructive)); }
        .text-destructive-foreground { color: hsl(var(--destructive-foreground)); }
        .border-border { border-color: hsl(var(--border)); }
        .bg-input { background-color: hsl(var(--input)); }
        .border-input { border-color: hsl(var(--input)); }
        .focus\:ring-ring:focus { --tw-ring-color: hsl(var(--ring)); }

        .status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 8px; }
        .status-online { background-color: #10b981; box-shadow: 0 0 10px #10b981; }
        .status-offline { background-color: #ef4444; }
        .scroll-hide::-webkit-scrollbar { display: none; }
        .scroll-hide { -ms-overflow-style: none; scrollbar-width: none; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .animate-in { animation: fadeIn 0.5s ease-out forwards; }
    </style>
</head>
<body class="flex items-center justify-center p-4 md:p-8 font-sans">
    <div class="w-full max-w-6xl grid grid-cols-1 md:grid-cols-12 gap-6 h-[90vh] animate-in">
        
        <div class="md:col-span-4 flex flex-col gap-6 h-full overflow-hidden">
            <div class="p-6 rounded-xl border border-border bg-card">
                <div class="flex items-center gap-3 mb-2">
                    <div class="p-2 bg-white/5 rounded-lg text-primary"><i data-lucide="server"></i></div>
                    <h1 class="text-xl font-bold tracking-tight">M2 Manager</h1>
                </div>
                <p class="text-xs text-muted-foreground">Painel Administrativo v2.0</p>
            </div>

            <div class="flex-1 p-6 rounded-xl border border-border bg-card overflow-hidden flex flex-col">
                <h3 class="text-sm font-medium mb-4 flex items-center justify-between uppercase tracking-widest text-muted-foreground">
                    Status do Sistema
                    <button onclick="checkStatus()" class="hover:rotate-180 transition-transform duration-500">
                        <i data-lucide="refresh-cw" class="w-4 h-4"></i>
                    </button>
                </h3>
                <div id="status-list" class="space-y-2 overflow-y-auto scroll-hide flex-1">
                    <div class="flex items-center justify-center h-full opacity-20">
                        <i data-lucide="loader-2" class="animate-spin w-8 h-8"></i>
                    </div>
                </div>
                
                <div class="mt-4 pt-4 border-t border-border grid grid-cols-2 gap-4">
                    <div class="text-left p-3 rounded-lg bg-white/5">
                        <p class="text-[10px] uppercase text-muted-foreground mb-1">Contas</p>
                        <p id="stat-accounts" class="text-lg font-bold">--</p>
                    </div>
                    <div class="text-left p-3 rounded-lg bg-white/5">
                        <p class="text-[10px] uppercase text-muted-foreground mb-1">Players</p>
                        <p id="stat-players" class="text-lg font-bold">--</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="md:col-span-8 flex flex-col gap-6 h-full overflow-hidden">
            <div class="p-6 rounded-xl border border-border bg-card">
                <h3 class="text-sm font-medium mb-6 flex items-center gap-2 uppercase tracking-widest text-muted-foreground">
                    <i data-lucide="sliders" class="w-4 h-4"></i>
                    Controles de Operação
                </h3>
                <div class="flex flex-col md:flex-row items-end gap-4">
                    <div class="w-full md:w-48">
                        <label class="text-[10px] uppercase font-bold text-muted-foreground mb-2 block">Canais Ativos</label>
                        <select id="channels" class="w-full bg-secondary border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-ring transition-all">
                            <option value="1">1 Canal</option>
                            <option value="2">2 Canais</option>
                            <option value="3">3 Canais</option>
                            <option value="4">4 Canais</option>
                        </select>
                    </div>
                    <div class="flex-1 flex gap-2 w-full">
                        <button id="btn-start" onclick="startServer()" class="flex-1 h-10 bg-primary text-primary-foreground text-sm font-medium rounded-md hover:bg-primary/90 transition-all flex items-center justify-center gap-2">
                            <i data-lucide="play" class="w-4 h-4"></i> Iniciar
                        </button>
                        <button id="btn-stop" onclick="stopServer()" class="flex-1 h-10 bg-secondary text-secondary-foreground text-sm font-medium rounded-md border border-border hover:bg-destructive hover:text-white transition-all flex items-center justify-center gap-2">
                            <i data-lucide="square" class="w-4 h-4"></i> Parar
                        </button>
                        <button id="btn-restart" onclick="restartServer()" class="flex-1 h-10 bg-secondary text-secondary-foreground text-sm font-medium rounded-md border border-border hover:bg-accent transition-all flex items-center justify-center gap-2">
                            <i data-lucide="refresh-ccw" class="w-4 h-4"></i> Reiniciar
                        </button>
                        <button id="btn-clear" onclick="clearLogs()" class="flex-1 h-10 bg-secondary text-secondary-foreground text-sm font-medium rounded-md border border-border hover:bg-accent transition-all flex items-center justify-center gap-2">
                            <i data-lucide="trash-2" class="w-4 h-4"></i> Limpar
                        </button>
                    </div>
                </div>
            </div>

            <div class="flex-1 p-6 rounded-xl border border-border bg-card flex flex-col overflow-hidden">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-sm font-medium flex items-center gap-2 uppercase tracking-widest text-muted-foreground">
                        <i data-lucide="terminal" class="w-4 h-4"></i>
                        Logs de Erro
                    </h3>
                    <div class="flex gap-1">
                        <button onclick="clearLogs()" class="text-[10px] px-3 py-1 rounded bg-red-500/10 hover:bg-red-500/20 text-red-500 border border-red-500/20 transition-all flex items-center gap-1 font-bold mr-2"><i data-lucide="trash" class="w-3 h-3"></i> LIMPAR TUDO</button>
                        <button onclick="loadLogs('db')" class="text-[10px] px-3 py-1 rounded bg-white/5 hover:bg-white/10 transition-all border border-border">DB</button>
                        <button onclick="loadLogs('auth')" class="text-[10px] px-3 py-1 rounded bg-white/5 hover:bg-white/10 transition-all border border-border">AUTH</button>
                        <button onclick="loadLogs('ch1')" class="text-[10px] px-3 py-1 rounded bg-primary text-primary-foreground font-bold transition-all shadow-lg shadow-white/5">CH1</button>
                    </div>
                </div>
                <div id="logs-container" class="flex-1 bg-black/40 rounded-lg p-4 font-mono text-[11px] leading-relaxed text-blue-100/60 overflow-y-auto scroll-hide border border-white/5 whitespace-pre-wrap">
                    Aguardando seleção de log...
                </div>
            </div>
        </div>
    </div>

    <div id="toast" class="fixed bottom-8 right-8 p-4 rounded-lg border border-border bg-card shadow-2xl translate-y-20 opacity-0 transition-all duration-500 z-50 flex items-center gap-3">
        <div id="toast-icon" class="p-1.5 rounded-full"></div>
        <p id="toast-msg" class="text-sm font-medium"></p>
    </div>

    <script>
        lucide.createIcons();

        function showToast(msg, type = 'success') {
            const toast = document.getElementById('toast');
            const icon = document.getElementById('toast-icon');
            const msgEl = document.getElementById('toast-msg');
            msgEl.textContent = msg;
            toast.className = "fixed bottom-8 right-8 p-4 rounded-lg border border-border bg-card shadow-2xl transition-all duration-500 z-50 flex items-center gap-3 translate-y-0 opacity-100";
            if(type === 'success') {
                icon.className = "p-1.5 rounded-full bg-emerald-500/10 text-emerald-500";
                icon.innerHTML = '<i data-lucide="check" class="w-4 h-4"></i>';
            } else {
                icon.className = "p-1.5 rounded-full bg-red-500/10 text-red-500";
                icon.innerHTML = '<i data-lucide="alert-triangle" class="w-4 h-4"></i>';
            }
            lucide.createIcons();
            setTimeout(() => {
                toast.classList.add('translate-y-20', 'opacity-0');
                toast.classList.remove('translate-y-0', 'opacity-100');
            }, 4000);
        }

        async function apiCall(endpoint, method = 'GET', data = null) {
            try {
                const config = {
                    method,
                    headers: { 'Content-Type': 'application/json' },
                    body: data ? JSON.stringify(data) : null
                };
                const res = await fetch(endpoint, config);
                return await res.json();
            } catch (error) {
                showToast(error.message, 'error');
                return null;
            }
        }

        function createStatusItem(label, isOnline) {
            return '<div class="flex items-center justify-between p-3 rounded-lg bg-white/[0.02] border border-white/5 hover:bg-white/[0.04] transition-colors"><span class="text-sm text-white/70 font-medium">' + label + '</span><div class="flex items-center gap-2"><span class="text-[9px] font-black ' + (isOnline ? 'text-emerald-500' : 'text-red-500') + '">' + (isOnline ? 'ONLINE' : 'OFFLINE') + '</span><div class="status-dot ' + (isOnline ? 'status-online' : 'status-offline') + '"></div></div></div>';
        }

        async function checkStatus() {
            const list = document.getElementById('status-list');
            const data = await apiCall('/api/status');
            if (data) {
                let html = '';
                html += createStatusItem('Base de Dados (MySQL)', data.mysql);
                html += createStatusItem('Processo Database', data.database);
                html += createStatusItem('Processo Auth', data.auth);
                ['CH1', 'CH2', 'CH3', 'CH4', 'CH99'].forEach(ch => {
                    const online = data.channels.some(c => c.toUpperCase() === ch);
                    html += createStatusItem('Canal ' + ch, online);
                });
                list.innerHTML = html;
                document.getElementById('stat-accounts').textContent = data.stats.accounts;
                document.getElementById('stat-players').textContent = data.stats.players;
            }
        }

        async function startServer() {
            const btn = document.getElementById('btn-start');
            const ch = document.getElementById('channels').value;
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="animate-spin w-4 h-4"></i>';
            lucide.createIcons();
            const res = await apiCall('/api/start', 'POST', { channels: parseInt(ch) });
            if(res) showToast('Servidor iniciado!');
            setTimeout(() => {
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="play" class="w-4 h-4"></i> Iniciar';
                lucide.createIcons();
                checkStatus();
            }, 5000);
        }

        async function stopServer() {
            const btn = document.getElementById('btn-stop');
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="animate-spin w-4 h-4"></i>';
            lucide.createIcons();
            const res = await apiCall('/api/stop', 'POST');
            if(res) showToast('Parada solicitada');
            setTimeout(() => {
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="square" class="w-4 h-4"></i> Parar';
                lucide.createIcons();
                checkStatus();
            }, 5000);
        }

        async function restartServer() {
            const btn = document.getElementById('btn-restart');
            const ch = document.getElementById('channels').value;
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="animate-spin w-4 h-4"></i>';
            lucide.createIcons();
            const res = await apiCall('/api/restart', 'POST', { channels: parseInt(ch) });
            if(res) showToast('Sistema reiniciado com sucesso!');
            setTimeout(() => {
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="refresh-ccw" class="w-4 h-4"></i> Reiniciar';
                lucide.createIcons();
                checkStatus();
            }, 5000);
        }

        async function clearLogs() {
            const btn = document.getElementById('btn-clear');
            btn.disabled = true;
            btn.innerHTML = '<i data-lucide="loader-2" class="animate-spin w-4 h-4"></i>';
            lucide.createIcons();
            const res = await apiCall('/api/clear', 'POST');
            if(res) showToast('Logs e arquivos temporários limpos!');
            setTimeout(() => {
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="trash-2" class="w-4 h-4"></i> Limpar';
                lucide.createIcons();
            }, 2000);
        }

        async function loadLogs(type) {
            const container = document.getElementById('logs-container');
            container.innerHTML = '<div class="flex items-center gap-2 opacity-50"><i data-lucide="loader-2" class="animate-spin w-3 h-3"></i></div>';
            lucide.createIcons();
            const data = await apiCall('/api/logs');
            if(data && data[type]) {
                container.textContent = data[type];
                container.scrollTop = container.scrollHeight;
            } else {
                container.textContent = "Log vazio ou não encontrado.";
            }
        }

        window.onload = () => {
            checkStatus();
            setInterval(checkStatus, 15000);
            loadLogs('ch1');
        };
    </script>
</body>
</html>
`;

const server = http.createServer(async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    if (req.method === 'OPTIONS') { res.writeHead(200); res.end(); return; }
    const url = new URL(req.url, `http://localhost:${PORT}`);
    if (url.pathname === '/') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(htmlTemplate);
    }
    else if (url.pathname === '/api/status') {
        const status = await manager.checkStatus();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(status));
    }
    else if (url.pathname === '/api/logs') {
        const logs = await manager.getLogs();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(logs));
    }
    else if (url.pathname === '/api/start' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', async () => {
            try {
                const data = JSON.parse(body);
                const result = await manager.startServer(data.channels || 1);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(result));
            } catch (error) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: false, error: error.message }));
            }
        });
    }
    else if (url.pathname === '/api/stop' && req.method === 'POST') {
        const result = await manager.stopServer();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
    }
    else if (url.pathname === '/api/restart' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', async () => {
            try {
                const data = JSON.parse(body);
                const result = await manager.restartServer(data.channels || 1);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(result));
            } catch (error) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: false, error: error.message }));
            }
        });
    }
    else if (url.pathname === '/api/clear' && req.method === 'POST') {
        const result = await manager.clearLogs();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
    }
    else { res.writeHead(404); res.end('Not Found'); }
});

server.listen(PORT, '0.0.0.0', () => {
    console.log(`✅ Servidor rodando na porta ${PORT}`);
});