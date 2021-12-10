-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE braces (k, v, n);
INSERT INTO braces VALUES
    ('(', ')', 1),
    ('[', ']', 2),
    ('{', '}', 3),
    ('<', '>', 4),
    ('x', 'x', 0);

CREATE TABLE leftovers (n INT);
WITH RECURSIVE nn (s, stack, rest) AS (
    SELECT '', '', (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        CASE
            WHEN SUBSTR(nn.rest, 1, 1) = char(10)
            THEN (
                nn.stack ||
                SUBSTR('xxxxxxxxxxxxxxx', 1, 15 - LENGTH(nn.stack))
            )
            ELSE ''
        END,
        CASE
            WHEN SUBSTR(nn.rest, 1, 1) = char(10) THEN ''
            WHEN SUBSTR(nn.rest, 1, 1) IN ('(', '[', '{', '<')
            THEN (
                nn.stack ||
                (SELECT v FROM braces WHERE k = SUBSTR(nn.rest, 1, 1))
            )
            WHEN SUBSTR(nn.rest, 1, 1) = SUBSTR(nn.stack, -1, 1)
            THEN SUBSTR(nn.stack, 1, LENGTH(nn.stack) - 1)
            WHEN SUBSTR(nn.rest, 1, 1) != SUBSTR(nn.stack, -1, 1)
            THEN ''
            ELSE 'WAT?'
        END,
        CASE
            WHEN (
                SUBSTR(nn.rest, 1, 1) IN (')', ']', '}', '>') AND
                SUBSTR(nn.rest, 1, 1) != SUBSTR(nn.stack, -1, 1)
            )
            THEN SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
            ELSE SUBSTR(nn.rest, 2)
        END
    FROM nn WHERE nn.rest != ''
)
INSERT INTO leftovers
SELECT t.n FROM (
    SELECT (
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -15, 1)) * 1 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -14, 1)) * 5 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -13, 1)) * 25 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -12, 1)) * 125 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -11, 1)) * 625 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -10, 1)) * 3125 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -9, 1)) * 15625 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -8, 1)) * 78125 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -7, 1)) * 390625 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -6, 1)) * 1953125 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -5, 1)) * 9765625 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -4, 1)) * 48828125 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -3, 1)) * 244140625 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -2, 1)) * 1220703125 +
        (SELECT n FROM braces WHERE v = SUBSTR(nn.s, -1, 1)) * 6103515625
    ) AS n
    FROM nn WHERE nn.s != ''
) AS t
ORDER BY t.n ASC;

SELECT leftovers.n FROM leftovers
WHERE ROWID = (SELECT COUNT(1) / 2 + 1 FROM leftovers);
