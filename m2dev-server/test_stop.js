const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const GAMEDIR = process.cwd();

async function runCommand(cmd) {
    return new Promise((resolve) => {
        console.log(`[Executing] ${cmd}`);
        const child = spawn(cmd, { shell: true });
        let stdout = '';
        let stderr = '';
        child.stdout.on('data', (data) => stdout += data.toString());
        child.stderr.on('data', (data) => stderr += data.toString());
        child.on('close', (code) => resolve({ code, stdout, stderr }));
    });
}

async function testStop() {
    console.log("--- TEST STOP LOGIC ---");
    
    // 1. List Metin2 processes
    const before = await runCommand('powershell -Command "Get-Process | Where-Object { $_.Name -like \'channel*\' -or $_.Name -like \'game*\' -or $_.Name -eq \'db\' } | Select-Object Name, Id, Path"');
    console.log("Processes BEFORE:\n", before.stdout || "None");

    // 2. Try to kill
    console.log("Executing Stop-Process...");
    const kill = await runCommand('powershell -Command "Get-Process | Where-Object { $_.Name -like \'channel*\' -or $_.Name -like \'game*\' -or $_.Name -eq \'db\' } | Stop-Process -Force -PassThru"');
    console.log("Kill Result:\n", kill.stdout || kill.stderr || "No output");

    // 3. List again
    await new Promise(r => setTimeout(r, 2000));
    const after = await runCommand('powershell -Command "Get-Process | Where-Object { $_.Name -like \'channel*\' -or $_.Name -like \'game*\' -or $_.Name -eq \'db\' } | Select-Object Name, Id"');
    console.log("Processes AFTER:\n", after.stdout || "None (SUCCESS)");
}

testStop();
