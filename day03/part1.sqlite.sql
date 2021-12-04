-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE vars(line_len);
INSERT INTO vars SELECT INSTR(s, char(10)) - 1 FROM input;

-- no power function in this version sadface
CREATE TABLE vars2 (maxmult);
WITH RECURSIVE
    nn (mult, n)
AS (
    SELECT 1, 0
    UNION ALL
    SELECT nn.mult * 2, nn.n + 1
    FROM nn
    WHERE nn.n < (SELECT line_len FROM vars)
)
INSERT INTO vars2 SELECT MAX(nn.mult) FROM nn;

CREATE TABLE positions (mult, c);
WITH RECURSIVE
    nn (mult, c, rest)
AS (
    SELECT
        (SELECT maxmult FROM vars2),
        char(10),
        (SELECT s FROM input)
    UNION ALL
    SELECT
        CASE SUBSTR(nn.rest, 1, 1)
            WHEN char(10) THEN (SELECT maxmult FROM vars2)
            ELSE nn.mult / 2
        END,
        SUBSTR(nn.rest, 1, 1),
        SUBSTR(nn.rest, 2)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO positions
SELECT nn.mult, nn.c FROM nn WHERE nn.c != char(10);

SELECT (
    SELECT SUM(c * mult)
    FROM (
        SELECT c, mult, count(1)
        FROM positions
        GROUP BY mult, c
        ORDER BY COUNT(1) DESC LIMIT (SELECT line_len FROM vars)
    )
) *  (
    SELECT SUM(c * mult)
    FROM (
        SELECT c, mult, count(1)
        FROM positions
        GROUP BY mult, c
        ORDER BY COUNT(1) ASC LIMIT (SELECT line_len FROM vars)
    )
);
