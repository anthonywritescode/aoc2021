-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE lines (x1 INT, y1 INT, x2 INT, y2 INT);
WITH RECURSIVE
    nn (x1, y1, x2, y2, rest)
AS (
    SELECT -1, -1, -1, -1, (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        SUBSTR(nn.rest, 1, INSTR(nn.rest, ',') - 1),
        SUBSTR(
            nn.rest,
            INSTR(nn.rest, ',') + 1,
            INSTR(nn.rest, ' ') - INSTR(nn.rest, ',') - 1
        ),
        SUBSTR(
            nn.rest,
            INSTR(nn.rest, '>') + 2,
            INSTR(
                SUBSTR(nn.rest, INSTR(nn.rest, '>') + 2),
                ','
            ) - 1
        ),
        SUBSTR(
            nn.rest,
            INSTR(nn.rest, '>') +
            INSTR(SUBSTR(nn.rest, INSTR(nn.rest, '>')), ','),
            INSTR(nn.rest, char(10)) -
            INSTR(nn.rest, '>') -
            INSTR(SUBSTR(nn.rest, INSTR(nn.rest, '>')), ',')
        ),
        SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO lines
SELECT x1, y1, x2, y2
FROM nn
WHERE x1 > 0 AND (x1 = x2 OR y1 = y2);

CREATE TABLE points (x, y, val);
WITH RECURSIVE
    nn (rid, x, y, x2, y2)
AS (
    SELECT ROWID, x1, y1, x2, y2 FROM lines WHERE ROWID = 1
    UNION ALL
    SELECT
        CASE nn.x = nn.x2 AND nn.y = nn.y2
            WHEN 1 THEN nn.rid + 1
            ELSE nn.rid
        END,
        CASE nn.x = nn.x2 AND nn.y = nn.y2
            WHEN 1 THEN (SELECT lines.x1 FROM lines WHERE ROWID = nn.rid + 1)
            ELSE
                CASE nn.x = nn.x2
                    WHEN 1 THEN nn.x
                    ELSE
                        CASE nn.x < nn.x2
                            WHEN 1 THEN nn.x + 1
                            ELSE nn.x - 1
                        END
                END
        END,
        CASE nn.x = nn.x2 AND nn.y = nn.y2
            WHEN 1 THEN (SELECT lines.y1 FROM lines WHERE ROWID = nn.rid + 1)
            ELSE
                CASE nn.y = nn.y2
                    WHEN 1 THEN nn.y
                    ELSE
                        CASE nn.y < nn.y2
                            WHEN 1 THEN nn.y + 1
                            ELSE nn.y - 1
                        END
                END
        END,
        CASE nn.x = nn.x2 AND nn.y = nn.y2
            WHEN 1 THEN (SELECT lines.x2 FROM lines WHERE ROWID = nn.rid + 1)
            ELSE nn.x2
        END,
        CASE nn.x = nn.x2 AND nn.y = nn.y2
            WHEN 1 THEN (SELECT lines.y2 FROM lines WHERE ROWID = nn.rid + 1)
            ELSE nn.y2
        END
    FROM nn
    WHERE nn.x IS NOT NULL
)
INSERT INTO points
SELECT nn.x, nn.y, COUNT(1) FROM nn WHERE nn.x IS NOT NULL GROUP BY nn.x, nn.y;

SELECT COUNT(1) FROM points WHERE val > 1;
