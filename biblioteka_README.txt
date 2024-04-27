-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS biblioteka;

-- Use the database
USE biblioteka;

-- Create the table "tytuły"
CREATE TABLE IF NOT EXISTS tytuły (
    title_id VARCHAR(10) PRIMARY KEY,
    title VARCHAR(255)
);

-- Create a procedure to insert new rows with automatically generated title_id
DELIMITER //
CREATE PROCEDURE insert_title(IN new_title VARCHAR(255))
BEGIN
    DECLARE new_title_id VARCHAR(10);
    SELECT CONCAT('T', IFNULL(MAX(CAST(SUBSTRING(title_id, 2) AS UNSIGNED)) + 1, 1)) INTO new_title_id FROM tytuły;
    INSERT INTO tytuły (title_id, title) VALUES (new_title_id, new_title);
END //
DELIMITER ;

-- Call the procedure to insert sample data (optional)
CALL insert_title('Sample Title 1');
CALL insert_title('Sample Title 2');
