-- SQL script that meets the following requirements:
-- Create a function SafeDiv
-- The function SafeDiv takes 2 arguments:
-- a (INT), b (INT)
-- Returns a / b or 0 if b == 0

DELIMITER |
DROP FUNCTION IF EXISTS SafeDiv;
CREATE FUNCTION SafeDiv (a INT, b INT)
RETURNS FLOAT
BEGIN
    DECLARE result FLOAT;
    IF b = 0 THEN
        SET result = 0;
    ELSE
        SET result = a / b;
    END IF;
    RETURN result;
END;
|
