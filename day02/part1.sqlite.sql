-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE answer (n INT);
WITH RECURSIVE
    nn (n, position, depth, rest)
AS (
    SELECT 0, 0, 0, (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        nn.n + 1,
        CASE SUBSTR(nn.rest, 0, INSTR(nn.rest, ' '))
            WHEN 'forward' THEN
                nn.position +
                SUBSTR(
                    nn.rest,
                    INSTR(nn.rest, ' '),
                    INSTR(nn.rest, char(10)) - INSTR(nn.rest, ' ')
                )
            ELSE nn.position
        END,
        CASE SUBSTR(nn.rest, 0, INSTR(nn.rest, ' '))
            WHEN 'up' THEN
                nn.depth -
                SUBSTR(
                    nn.rest,
                    INSTR(nn.rest, ' '),
                    INSTR(nn.rest, char(10)) - INSTR(nn.rest, ' ')
                )
            WHEN 'down' THEN
                nn.depth +
                SUBSTR(
                    nn.rest,
                    INSTR(nn.rest, ' '),
                    INSTR(nn.rest, char(10)) - INSTR(nn.rest, ' ')
                )
            ELSE nn.depth
        END,
        SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO answer
SELECT nn.position * nn.depth FROM nn ORDER BY nn.n DESC LIMIT 1;

SELECT * FROM answer;
