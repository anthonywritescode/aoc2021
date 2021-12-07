-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE numbers (n INT);
WITH RECURSIVE
    nn (n, rest)
AS (
    SELECT -1, (SELECT s || ',' FROM input)
    UNION ALL
    SELECT
        SUBSTR(nn.rest, 1, INSTR(nn.rest, ',') - 1) + 0,
        SUBSTR(nn.rest, INSTR(nn.rest, ',') + 1)
    FROM nn WHERE nn.rest != ''
)
INSERT INTO numbers SELECT nn.n FROM nn WHERE nn.n >= 0 ORDER BY nn.n ASC;

WITH RECURSIVE nn(n) AS (
    SELECT MIN(n) FROM numbers
    UNION ALL
    SELECT nn.n + 1 FROM nn
    WHERE nn.n < (SELECT MAX(n) FROM numbers)
)
SELECT MIN(summed) FROM (
    SELECT
        (
            SELECT SUM(ABS(nn.n - n) * (ABS(nn.n - n) + 1) / 2)
            FROM numbers
        ) AS summed
    FROM nn
);
