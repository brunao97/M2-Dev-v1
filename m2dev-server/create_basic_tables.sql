-- Script para criar tabelas básicas do Metin2
-- Execute: mysql -u mt2 -pmt2 account < create_basic_tables.sql

DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(30) NOT NULL DEFAULT '',
  `password` varchar(45) NOT NULL DEFAULT '',
  `social_id` varchar(13) NOT NULL DEFAULT '',
  `email` varchar(64) NOT NULL DEFAULT '',
  `create_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `is_testor` tinyint(1) NOT NULL DEFAULT 0,
  `status` varchar(8) NOT NULL DEFAULT 'OK',
  `newsletter` tinyint(1) DEFAULT 0,
  `empire` tinyint(4) NOT NULL DEFAULT 0,
  `name_checked` tinyint(1) NOT NULL DEFAULT 0,
  `availDt` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `mileage` int(11) NOT NULL DEFAULT 0,
  `cash` int(11) NOT NULL DEFAULT 0,
  `gold_expire` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `silver_expire` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `safebox_expire` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `autoloot_expire` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `fish_mind_expire` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `marriage_fast_expire` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `money_drop_rate_expire` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `total_cash` int(11) NOT NULL DEFAULT 0,
  `total_mileage` int(11) NOT NULL DEFAULT 0,
  `channel_company` varchar(30) NOT NULL DEFAULT '',
  `ip` varchar(255) DEFAULT NULL,
  `last_play` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`),
  KEY `social_id` (`social_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Inserir conta de teste
INSERT INTO `account` VALUES 
(1,'admin','*4ACFE3202A5FF5CF467898FC58AAB1D615029441','1234567','','0000-00-00 00:00:00',0,'OK',0,0,0,'0000-00-00 00:00:00',0,0,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',0,0,'',NULL,'2021-11-21 20:10:46'),
(2,'test','*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29','1234567','','0000-00-00 00:00:00',0,'OK',0,0,0,'0000-00-00 00:00:00',0,0,'0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00','0000-00-00 00:00:00',0,0,'',NULL,'2021-08-06 11:42:12');

DROP TABLE IF EXISTS `string`;
CREATE TABLE `string` (
  `name` varchar(64) NOT NULL DEFAULT '',
  `text` text DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
