-- Criar função PASSWORD() compatível com Metin2
USE mysql;
DELIMITER //

CREATE FUNCTION PASSWORD(input VARCHAR(255))
RETURNS VARCHAR(41)
DETERMINISTIC
BEGIN
    RETURN CONCAT("*", UPPER(SHA1(UNHEX(SHA1(input)))));
END;

//

DELIMITER ;

-- Testar a função
SELECT PASSWORD('test') as password_hash;