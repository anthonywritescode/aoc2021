-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

WITH RECURSIVE nn (s, rest) AS (
    SELECT '', (SELECT SUBSTR(s, INSTR(s, '|') + 2) || char(10) FROM input)
    UNION ALL
    SELECT
        SUBSTR(
            nn.rest,
            1,
            CASE INSTR(nn.rest, ' ') > 0
                WHEN 1
                THEN MIN(INSTR(nn.rest, ' '), INSTR(nn.rest, char(10))) - 1
                ELSE INSTR(nn.rest, char(10)) - 1
            END
        ),
        CASE (
            INSTR(nn.rest, ' ') > 0 AND
            INSTR(nn.rest, ' ') < INSTR(nn.rest, char(10))
        )
        WHEN 1 THEN SUBSTR(nn.rest, INSTR(nn.rest, ' ') + 1)
        ELSE
            CASE INSTR(nn.rest, '|') > 0
                WHEN 1 THEN SUBSTR(nn.rest, INSTR(nn.rest, '|') + 2)
                ELSE SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
            END
        END
    FROM nn WHERE nn.rest != ''
)
SELECT COUNT(1)
FROM nn
WHERE LENGTH(nn.s) IN (2, 3, 4, 7);
