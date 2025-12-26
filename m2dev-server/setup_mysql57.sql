-- Configuração MySQL 5.7 para Metin2
-- Execute como root: mysql -u root -p < setup_mysql57.sql

-- Criar bancos de dados
CREATE DATABASE IF NOT EXISTS account;
CREATE DATABASE IF NOT EXISTS common;
CREATE DATABASE IF NOT EXISTS log;
CREATE DATABASE IF NOT EXISTS player;

-- Criar usuário mt2
DROP USER IF EXISTS 'mt2'@'localhost';
CREATE USER 'mt2'@'localhost' IDENTIFIED BY 'mt2';

-- Dar permissões completas
GRANT ALL PRIVILEGES ON account.* TO 'mt2'@'localhost';
GRANT ALL PRIVILEGES ON common.* TO 'mt2'@'localhost';
GRANT ALL PRIVILEGES ON log.* TO 'mt2'@'localhost';
GRANT ALL PRIVILEGES ON player.* TO 'mt2'@'localhost';

-- Aplicar mudanças
FLUSH PRIVILEGES;

-- Verificar versão do MySQL
SELECT VERSION() AS mysql_version;
