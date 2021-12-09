-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE vars(width);
INSERT INTO vars SELECT INSTR(s, char(10)) - 1 FROM input;

CREATE TABLE coords(y, x, n INT);
WITH RECURSIVE nn (x, c, rest) AS (
    SELECT -1, '', (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        nn.x + 1,
        SUBSTR(nn.rest, 1, 1),
        CASE INSTR(nn.rest, char(10)) = 2
            WHEN 1 THEN SUBSTR(nn.rest, 3)
            ELSE SUBSTR(nn.rest, 2)
        END
    FROM nn WHERE nn.rest != ''
)
INSERT INTO coords
SELECT
    nn.x / (SELECT width FROM vars),
    nn.x % (SELECT width FROM vars),
    nn.c
FROM nn WHERE nn.c != '';

SELECT SUM(c.n + 1)
FROM coords AS c
LEFT OUTER JOIN coords AS c1 ON c1.y = c.y AND c1.x = c.x + 1
LEFT OUTER JOIN coords AS c2 ON c2.y = c.y AND c2.x = c.x - 1
LEFT OUTER JOIN coords AS c3 ON c3.y = c.y + 1 AND c3.x = c.x
LEFT OUTER JOIN coords AS c4 ON c4.y = c.y - 1 AND c4.x = c.x
WHERE (
    COALESCE(c1.n, 9) > c.n AND
    COALESCE(c2.n, 9) > c.n AND
    COALESCE(c3.n, 9) > c.n AND
    COALESCE(c4.n, 9) > c.n
);
