-- Veritabanları
CREATE DATABASE IF NOT EXISTS account;
CREATE DATABASE IF NOT EXISTS common;
CREATE DATABASE IF NOT EXISTS log;
CREATE DATABASE IF NOT EXISTS player;

CREATE USER IF NOT EXISTS 'mt2'@'localhost' IDENTIFIED BY 'mt2';

-- Yetkiler
GRANT SELECT, INSERT, UPDATE, DELETE ON account.*    TO 'mt2'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON common.*     TO 'mt2'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON log.*        TO 'mt2'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON player.*     TO 'mt2'@'localhost';

-- Yetkileri yenile
FLUSH PRIVILEGES;
