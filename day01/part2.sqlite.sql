-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE numbers(n INT);
INSERT INTO numbers
SELECT t.value
FROM json_each('[' || REPLACE((SELECT s FROM input), char(10), ',') || ']') t;

SELECT SUM(numbers1.n > numbers2.n)
FROM numbers AS numbers1
INNER JOIN numbers as numbers2
WHERE numbers1.ROWID = numbers2.ROWID + 3;
