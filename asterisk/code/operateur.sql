DROP DATABASE IF EXISTS operateur;
CREATE DATABASE operateur;
USE operateur;

-- Crée la table si elle n'existe pas
CREATE TABLE codes_recharge (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    montant DECIMAL(10,2) ,
    utilise TINYINT DEFAULT 0
);

CREATE TABLE utilisateurs(
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT UNIQUE NOT NULL,
    nom VARCHAR(50),
    credit DECIMAL(10,2) DEFAULT 0.00,
    vola INT DEFAULT 0,
    passwd VARCHAR(4) DEFAULT "0000",
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
);



-- Ajoutons un utilisateur test
INSERT INTO utilisateurs (numero, nom, credit,vola) 
VALUES 
(1012, 'Lucas', 1000,5000000),
(1011, 'Mikajy', 10200,225000), 
(1013,'Nasa',5000,225000);
-- Ajoute quelques codes
INSERT INTO codes_recharge (code, montant) 
VALUES 
('123456789', 1000),
('987654321', 5000),
('11223344', 10000);

