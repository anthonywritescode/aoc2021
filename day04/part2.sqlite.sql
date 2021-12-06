-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE bingo_rows (id, c, c1, c2, c3, c4, c5, c1d, c2d, c3d, c4d, c5d);
WITH RECURSIVE
    nn (id, r, c1, c2, c3, c4, c5, rest)
AS (
    SELECT
        -1, 4, 0, 0, 0, 0, 0,
        (
            SELECT
                SUBSTR(s, INSTR(s, char(10)) + 2) || char(10) || char(10)
            FROM input
        )
    UNION ALL
    SELECT
        CASE nn.r = 4 WHEN 1 THEN nn.id + 1 ELSE nn.id END,
        CASE nn.r = 4 WHEN 1 THEN 0 ELSE nn.r + 1 END,
        SUBSTR(nn.rest, 1, 2) + 0,
        SUBSTR(nn.rest, 4, 2) + 0,
        SUBSTR(nn.rest, 7, 2) + 0,
        SUBSTR(nn.rest, 10, 2) + 0,
        SUBSTR(nn.rest, 13, 2) + 0,
        CASE nn.r = 3
            WHEN 1 THEN SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 2)
            ELSE SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
        END
    FROM nn WHERE nn.rest != ''
)
INSERT INTO bingo_rows
SELECT nn.id, 1, nn.c1, nn.c2, nn.c3, nn.c4, nn.c5, 0, 0, 0, 0, 0
FROM nn WHERE nn.id >= 0;

WITH RECURSIVE
    nn (id, r, c1, c2, c3, c4, c5, rest)
AS (
    SELECT
        -1, 4, 0, 0, 0, 0, 0,
        (
            SELECT
                SUBSTR(s, INSTR(s, char(10)) + 2) || char(10) || char(10)
            FROM input
        )
    UNION ALL
    SELECT
        CASE nn.r = 4 WHEN 1 THEN nn.id + 1 ELSE nn.id END,
        CASE nn.r = 4 WHEN 1 THEN 0 ELSE nn.r + 1 END,
        SUBSTR(nn.rest, 1 + nn.r * 3, 2) + 0,
        SUBSTR(nn.rest, 16 + nn.r * 3, 2) + 0,
        SUBSTR(nn.rest, 31 + nn.r * 3, 2) + 0,
        SUBSTR(nn.rest, 46 + nn.r * 3, 2) + 0,
        SUBSTR(nn.rest, 61 + nn.r * 3, 2) + 0,
        CASE nn.r = 3
            WHEN 1 THEN
                SUBSTR(nn.rest, INSTR(nn.rest, char(10) || char(10)) + 2)
            ELSE nn.rest
        END
    FROM nn WHERE nn.rest != ''
)
INSERT INTO bingo_rows
SELECT nn.id, 0, nn.c1, nn.c2, nn.c3, nn.c4, nn.c5, 0, 0, 0, 0, 0
FROM nn WHERE nn.id >= 0;

CREATE TABLE answers (n INT);
CREATE TABLE nums (n INT);
CREATE TRIGGER ttrig AFTER INSERT ON nums FOR EACH ROW BEGIN
    UPDATE bingo_rows SET c1d = 1 WHERE c1 = NEW.n;
    UPDATE bingo_rows SET c2d = 1 WHERE c2 = NEW.n;
    UPDATE bingo_rows SET c3d = 1 WHERE c3 = NEW.n;
    UPDATE bingo_rows SET c4d = 1 WHERE c4 = NEW.n;
    UPDATE bingo_rows SET c5d = 1 WHERE c5 = NEW.n;

    INSERT INTO answers
    SELECT NEW.n * (
        SELECT
            SUM(
                c1 * (1 - c1d) +
                c2 * (1 - c2d) +
                c3 * (1 - c3d) +
                c4 * (1 - c4d) +
                c5 * (1 - c5d)
            )
        FROM bingo_rows AS b2
        WHERE b2.id = bingo_rows.id AND b2.c = 1
    )
    FROM bingo_rows
    WHERE c1d and c2d and c3d and c4d and c5d;

    DELETE FROM bingo_rows WHERE id IN (
        SELECT id FROM bingo_rows
        WHERE c1d and c2d and c3d and c4d and c5d
    );
END;

WITH RECURSIVE
    nn (n, rest)
AS (
    SELECT -1, (SELECT SUBSTR(s, 1, INSTR(s, char(10)) - 1) || ',' FROM input)
    UNION ALL
    SELECT
        SUBSTR(nn.rest, 1, INSTR(nn.rest, ',') - 1),
        SUBSTR(nn.rest, INSTR(nn.rest, ',') + 1)
    FROM nn
    WHERE nn.rest != ''
)
INSERT INTO nums
SELECT nn.n FROM nn WHERE nn.n != -1;

SELECT n FROM answers ORDER BY ROWID DESC LIMIT 1;
