# Guia para Resolver Problemas do MySQL

## Problema Identificado
O MySQL não está iniciando devido a problemas de permissões e configuração.

## Solução Passo-a-Passo

### Opção 1: Usar MySQL 8.0 (Recomendado)
1. **Abrir services.msc como administrador:**
   - Pressione Win + R, digite `services.msc`
   - Clique com botão direito em "Executar como administrador"

2. **Iniciar o serviço MySQL80:**
   - Procure por "MySQL80" na lista
   - Clique com botão direito → "Propriedades"
   - Na aba "Geral", clique em "Iniciar"
   - Aguarde até o status ficar "Executando"

3. **Verificar se está funcionando:**
   ```cmd
   netstat -ano | findstr ":3306"
   ```
   Deve aparecer algo como: `TCP    0.0.0.0:3306    0.0.0.0:0    LISTENING`

### Opção 2: Instalar MySQL 5.7 Corretamente
1. **Desinstalar MySQL atual (se necessário):**
   ```cmd
   sc delete MySQL80
   sc delete MySQL57
   ```

2. **Executar instalador MySQL 5.7:**
   - Execute o instalador como administrador
   - Escolha "Custom" installation
   - Selecione MySQL Server 5.7
   - Configure como serviço Windows
   - Defina senha root como "mt2"

3. **Iniciar o serviço:**
   ```cmd
   net start MySQL57
   ```

### Opção 3: Iniciar MySQL Manualmente (Temporário)
1. **Executar como administrador:**
   ```cmd
   # Para MySQL 8.0
   "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe" --console --port=3306

   # OU para MySQL 5.7 (se conseguir inicializar)
   "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqld.exe" --initialize-insecure --console
   ```

## Após Resolver MySQL

### 1. Importar Dados do Backup
```bash
cd m2dev-server
powershell -ExecutionPolicy Bypass -File import_backup.ps1
```

### 2. Executar Setup SQL
```bash
# Conectar ao MySQL
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p

# Executar setup
source setup_mysql57.sql
```

### 3. Testar Servidor
```bash
cd m2dev-server
python start.py 1
```

## Verificação Final
Após seguir os passos acima, execute:
```bash
# Verificar MySQL
netstat -ano | findstr ":3306"

# Verificar DB
netstat -ano | findstr ":9000"

# Verificar Auth
netstat -ano | findstr ":11000"

# Verificar Canais
tasklist | findstr channel
```

## Status Atual
- ❌ MySQL não está rodando
- ❌ DB não consegue conectar
- ❌ Auth não consegue conectar
- ❌ Canais não iniciam

## Próximos Passos
1. Resolver MySQL seguindo uma das opções acima
2. Importar dados do backup
3. Testar servidor completo
4. Verificar logs para erros restantes