-- DESCRIBE katalogs;DROP TABLE IF EXISTS katalogs;

-- CREATE TABLE katalogs (
--     ProductID INT PRIMARY KEY,
--     EAN13 INT(13),
--     Pasūtījuma_kods VARCHAR(255),
--     Bilde BLOB,
--     Apraksts TEXT,
--     Iepirkuma_cena_bez_PVN FLOAT,
--     Cena FLOAT
-- );

DELETE FROM katalogs;


--@block

SELECT * FROM katalogs;