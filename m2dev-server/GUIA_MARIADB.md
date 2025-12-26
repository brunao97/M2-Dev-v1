# Guia de Instalação do MariaDB para Metin2

## Por que MariaDB?
O MariaDB 10.x mantém compatibilidade com a função `PASSWORD()` que o MySQL 8.0 removeu.
Isso evita a necessidade de recompilar os binários do servidor.

## Passo 1: Parar o MySQL 8.0

### Opção A - Via Services (Recomendado)
1. Pressione `Win + R` e digite `services.msc`
2. Procure por "MySQL80" ou "MySQL"
3. Clique com botão direito → **Parar**
4. Clique com botão direito → **Propriedades**
5. Tipo de inicialização: **Manual** (para não iniciar automaticamente)

### Opção B - Via PowerShell (Como Administrador)
```powershell
Stop-Service MySQL80 -Force
Set-Service MySQL80 -StartupType Manual
```

## Passo 2: Baixar MariaDB

1. Acesse: https://mariadb.org/download/
2. Escolha a versão: **MariaDB 10.11 LTS** (Long Term Support)
3. Sistema: **Windows x64**
4. Baixe o instalador MSI

## Passo 3: Instalar MariaDB

1. Execute o instalador **como Administrador**
2. Aceite a licença
3. **Importante:** Na tela de configuração:
   - ✅ Marque: "Enable networking"
   - ✅ Porta: **3307** (para não conflitar com MySQL na 3306)
   - ✅ Marque: "Use UTF8 as default server's character set"
   - ✅ Defina senha root: **dev** (ou a que preferir)
   - ✅ Marque: "Install as service"
   - ✅ Nome do serviço: **MariaDB**

4. Continue a instalação até o fim

## Passo 4: Configurar MariaDB

### 4.1 - Conectar ao MariaDB
```cmd
"C:\Program Files\MariaDB 10.11\bin\mysql.exe" -u root -pdev -P 3307
```

### 4.2 - Criar Bancos e Usuário
```sql
-- Criar bancos de dados
CREATE DATABASE IF NOT EXISTS account;
CREATE DATABASE IF NOT EXISTS common;
CREATE DATABASE IF NOT EXISTS log;
CREATE DATABASE IF NOT EXISTS player;

-- Criar usuário mt2
DROP USER IF EXISTS 'mt2'@'localhost';
CREATE USER 'mt2'@'localhost' IDENTIFIED BY 'mt2';

-- Dar permissões
GRANT ALL PRIVILEGES ON account.* TO 'mt2'@'localhost';
GRANT ALL PRIVILEGES ON common.* TO 'mt2'@'localhost';
GRANT ALL PRIVILEGES ON log.* TO 'mt2'@'localhost';
GRANT ALL PRIVILEGES ON player.* TO 'mt2'@'localhost';

FLUSH PRIVILEGES;

-- Sair
EXIT;
```

## Passo 5: Importar Dados

### 5.1 - Importar Schemas SQL
```cmd
cd G:\metin2-files-clean-64\M2-Dev\m2dev-server

"C:\Program Files\MariaDB 10.11\bin\mysql.exe" -u mt2 -pmt2 -P 3307 account < sql/account.sql
"C:\Program Files\MariaDB 10.11\bin\mysql.exe" -u mt2 -pmt2 -P 3307 common < sql/common.sql
"C:\Program Files\MariaDB 10.11\bin\mysql.exe" -u mt2 -pmt2 -P 3307 log < sql/log.sql
"C:\Program Files\MariaDB 10.11\bin\mysql.exe" -u mt2 -pmt2 -P 3307 player < sql/player.sql
```

## Passo 6: Atualizar Configuração do Servidor

Edite o arquivo de configuração do DB (normalmente em `m2dev-server/channels/db/CONFIG` ou similar):

```
SQL_ACCOUNT = "localhost mt2 mt2 account 3307"
SQL_PLAYER = "localhost mt2 mt2 player 3307"
SQL_COMMON = "localhost mt2 mt2 common 3307"
SQL_HOTBACKUP = "localhost mt2 mt2 hotbackup 3307"
```

## Passo 7: Testar

### 7.1 - Testar Função PASSWORD()
```cmd
"C:\Program Files\MariaDB 10.11\bin\mysql.exe" -u mt2 -pmt2 -P 3307 -e "SELECT PASSWORD('admin');"
```

Deve retornar algo como: `*4ACFE3202A5FF5CF467898FC58AAB1D615029441`

### 7.2 - Iniciar Servidor
```cmd
cd m2dev-server
py start.py 1
```

## Verificação Final

```cmd
# Verificar se MariaDB está rodando na porta 3307
netstat -ano | findstr ":3307"

# Verificar processos do servidor
netstat -ano | findstr ":9000"   # DB
netstat -ano | findstr ":11000"  # Auth
```

## Troubleshooting

### MariaDB não inicia
- Verifique os logs em: `C:\ProgramData\MySQL\MariaDB 10.11\data\*.err`
- Tente iniciar manualmente: `net start MariaDB`

### Conflito de porta
- Se a porta 3307 já estiver em uso, escolha outra (ex: 3308)
- Lembre-se de atualizar as configs do servidor

### Senha incorreta
- Redefina a senha do root:
  ```cmd
  mysqladmin -u root -p password dev
  ```

## Desinstalar MySQL 8.0 (Opcional)

Se quiser remover completamente o MySQL 8.0:

1. Painel de Controle → Programas → Desinstalar
2. Procure por "MySQL Server 8.0"
3. Desinstale
4. Delete as pastas:
   - `C:\Program Files\MySQL`
   - `C:\ProgramData\MySQL`

---

**Após seguir este guia, seu servidor Metin2 estará usando MariaDB com suporte nativo ao PASSWORD()!**
