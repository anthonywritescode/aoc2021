-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE counts (n0, n1, n2, n3, n4, n5, n6, n7, n8);
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
INSERT INTO counts
SELECT
    (SELECT COUNT(1) FROM nn WHERE nn.n = 0),
    (SELECT COUNT(1) FROM nn WHERE nn.n = 1),
    (SELECT COUNT(1) FROM nn WHERE nn.n = 2),
    (SELECT COUNT(1) FROM nn WHERE nn.n = 3),
    (SELECT COUNT(1) FROM nn WHERE nn.n = 4),
    (SELECT COUNT(1) FROM nn WHERE nn.n = 5),
    (SELECT COUNT(1) FROM nn WHERE nn.n = 6),
    (SELECT COUNT(1) FROM nn WHERE nn.n = 7),
    (SELECT COUNT(1) FROM nn WHERE nn.n = 8);

WITH RECURSIVE
    nn (i, n0, n1, n2, n3, n4, n5, n6, n7, n8)
AS (
    SELECT 0, * FROM counts
    UNION ALL
    SELECT
        nn.i + 1,
        nn.n1,
        nn.n2,
        nn.n3,
        nn.n4,
        nn.n5,
        nn.n6,
        nn.n7 + nn.n0,
        nn.n8,
        nn.n0
    FROM nn WHERE nn.i < 256
)
SELECT n0 + n1 + n2 + n3 + n4 + n5 + n6 + n7 + n8
FROM nn ORDER BY nn.i DESC LIMIT 1;
