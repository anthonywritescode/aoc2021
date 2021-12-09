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

CREATE TABLE minimums (y, x);
INSERT INTO minimums
SELECT c.y, c.x
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

PRAGMA recursive_triggers = on;

CREATE TABLE basins (y, x, orig_y, orig_x, PRIMARY KEY (y, x));
CREATE TRIGGER ttrig AFTER INSERT ON basins
BEGIN
    INSERT OR REPLACE INTO basins
    SELECT y, x, NEW.orig_y, NEW.orig_x
    FROM coords
    WHERE (
        (
            (coords.y = NEW.y AND coords.x = NEW.x + 1) OR
            (coords.y = NEW.y AND coords.x = NEW.x - 1) OR
            (coords.y = NEW.y + 1 AND coords.x = NEW.x) OR
            (coords.y = NEW.y - 1 AND coords.x = NEW.x)
        ) AND
        coords.n < 9 AND
        (
            SELECT 1
            FROM basins
            WHERE basins.y = coords.y AND basins.x = coords.x
        ) IS NULL
    );
END;

INSERT INTO basins
SELECT y, x, y, x FROM minimums;

CREATE TABLE sizes (n);

INSERT INTO sizes
SELECT COUNT(1)
FROM basins
GROUP BY orig_y, orig_x
ORDER BY COUNT(1) DESC LIMIT 3;

SELECT
    (SELECT n FROM sizes WHERE ROWID = 1) *
    (SELECT n FROM sizes WHERE ROWID = 2) *
    (SELECT n FROM sizes WHERE ROWID = 3);
