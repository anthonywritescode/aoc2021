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

SELECT SUM(
    ABS(
        n - (
            SELECT n FROM numbers
            WHERE ROWID = (SELECT MAX(ROWID) FROM numbers) / 2
        )
    )
) FROM numbers;
