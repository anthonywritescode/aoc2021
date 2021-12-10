-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE braces (k, v, n);
INSERT INTO braces VALUES
    ('(', ')', 3),
    ('[', ']', 57),
    ('{', '}', 1197),
    ('<', '>', 25137);

WITH RECURSIVE nn (total, stack, rest) AS (
    SELECT 0, '', (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        CASE
            WHEN (
                SUBSTR(nn.rest, 1, 1) IN (')', ']', '}', '>') AND
                SUBSTR(nn.rest, 1, 1) != SUBSTR(nn.stack, -1, 1)
            )
            THEN (
                nn.total +
                (SELECT n FROM braces WHERE v = SUBSTR(nn.rest, 1, 1))
            )
            ELSE nn.total
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
SELECT MAX(total) FROM nn;
