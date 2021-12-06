-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE vars (line_len);
INSERT INTO vars SELECT INSTR(s, char(10)) - 1 FROM input;

CREATE TABLE lines (s);
WITH RECURSIVE
    nn (s, rest)
AS (
    SELECT '', (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        SUBSTR(nn.rest, 1, INSTR(nn.rest, char(10)) - 1),
        SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO lines
SELECT nn.s FROM nn WHERE nn.s != '';

WITH RECURSIVE
    nn (i, o2_s, o2_num, co2_s, co2_num)
AS (
    SELECT -1, '', 0, '', 0
    UNION ALL
    SELECT
        nn.i + 1,
        CASE (
            SELECT COUNT(1) FROM lines WHERE s LIKE nn.o2_s || '1%'
        ) >= (
            SELECT COUNT(1) FROM lines WHERE s LIKE nn.o2_s || '0%'
        )
            WHEN 1 THEN nn.o2_s || '1'
            ELSE nn.o2_s || '0'
        END,
        CASE (
            SELECT COUNT(1) FROM lines WHERE s LIKE nn.o2_s || '1%'
        ) >= (
            SELECT COUNT(1) FROM lines WHERE s LIKE nn.o2_s || '0%'
        )
            WHEN 1 THEN nn.o2_num * 2 + 1
            ELSE nn.o2_num * 2
        END,
        CASE (
            (SELECT COUNT(1) FROM lines where s LIKE nn.co2_s || '1%') >= 1 AND
            (SELECT COUNT(1) FROM lines where s LIKE nn.co2_s || '0%') = 0
        ) OR (
            (SELECT COUNT(1) FROM lines where s LIKE nn.co2_s || '1%') >= 1 AND
            (SELECT COUNT(1) FROM lines where s LIKE nn.co2_s || '0%') >= 1 AND
            (
                SELECT COUNT(1) FROM lines WHERE s LIKE nn.co2_s || '0%'
            ) > (
                SELECT COUNT(1) FROM lines WHERE s LIKE nn.co2_s || '1%'
            )
        )
            WHEN 1 THEN nn.co2_s || '1'
            ELSE nn.co2_s || '0'
        END,
        CASE (
            (SELECT COUNT(1) FROM lines where s LIKE nn.co2_s || '1%') >= 1 AND
            (SELECT COUNT(1) FROM lines where s LIKE nn.co2_s || '0%') = 0
        ) OR (
            (SELECT COUNT(1) FROM lines where s LIKE nn.co2_s || '1%') >= 1 AND
            (SELECT COUNT(1) FROM lines where s LIKE nn.co2_s || '0%') >= 1 AND
            (
                SELECT COUNT(1) FROM lines WHERE s LIKE nn.co2_s || '0%'
            ) > (
                SELECT COUNT(1) FROM lines WHERE s LIKE nn.co2_s || '1%'
            )
        )
            WHEN 1 THEN nn.co2_num * 2 + 1
            ELSE nn.co2_num * 2
        END
    FROM nn
    WHERE nn.i < (SELECT line_len -1 FROM vars)
)
SELECT nn.o2_num * nn.co2_num FROM nn ORDER BY nn.i DESC LIMIT 1;
