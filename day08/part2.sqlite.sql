-- our puzzle input
CREATE TABLE input (s STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE nums (id INT, s STRING, val INT, PRIMARY KEY (id, s));
WITH RECURSIVE nn (pos, s, rest) AS (
    SELECT -1, '', (SELECT s || char(10) FROM input)
    UNION ALL
    SELECT
        nn.pos + 1,
        SUBSTR(nn.rest, 1, INSTR(nn.rest, ' ') - 1),
        CASE SUBSTR(nn.rest, INSTR(nn.rest, ' ') + 1, 1) = '|'
            WHEN 1 THEN SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
            ELSE SUBSTR(nn.rest, INSTR(nn.rest, ' ') + 1)
        END
    FROM nn WHERE nn.rest != ''
)
INSERT INTO nums
SELECT
    CAST(nn.pos / 10 AS INT),
    (CASE nn.s LIKE '%a%' WHEN 1 THEN 'a' ELSE '' END) ||
    (CASE nn.s LIKE '%b%' WHEN 1 THEN 'b' ELSE '' END) ||
    (CASE nn.s LIKE '%c%' WHEN 1 THEN 'c' ELSE '' END) ||
    (CASE nn.s LIKE '%d%' WHEN 1 THEN 'd' ELSE '' END) ||
    (CASE nn.s LIKE '%e%' WHEN 1 THEN 'e' ELSE '' END) ||
    (CASE nn.s LIKE '%f%' WHEN 1 THEN 'f' ELSE '' END) ||
    (CASE nn.s LIKE '%g%' WHEN 1 THEN 'g' ELSE '' END),
    NULL
FROM nn WHERE nn.s != '';

UPDATE nums SET val = 1 WHERE LENGTH(nums.s) = 2;
UPDATE nums SET val = 7 WHERE LENGTH(nums.s) = 3;
UPDATE nums SET val = 4 WHERE LENGTH(nums.s) = 4;
UPDATE nums SET val = 8 WHERE LENGTH(nums.s) = 7;

-- old sqlite does not have update with join
INSERT OR REPLACE INTO nums
SELECT nums.id, nums.s, 6
FROM nums INNER JOIN nums AS n2 ON nums.id = n2.id AND n2.val = 1
WHERE (
    LENGTH(nums.s) = 6 AND
    1 = (
        (nums.s LIKE '%' || SUBSTR(n2.s, 1, 1) || '%') +
        (nums.s LIKE '%' || SUBSTR(n2.s, 2, 1) || '%')
    )
);

INSERT OR REPLACE INTO nums
SELECT nums.id, nums.s, 9
FROM nums INNER JOIN nums AS n2 ON nums.id = n2.id AND n2.val = 4
WHERE (
    LENGTH(nums.s) = 6 AND
    nums.s LIKE '%' || SUBSTR(n2.s, 1, 1) || '%' AND
    nums.s LIKE '%' || SUBSTR(n2.s, 2, 1) || '%' AND
    nums.s LIKE '%' || SUBSTR(n2.s, 3, 1) || '%' AND
    nums.s LIKE '%' || SUBSTR(n2.s, 4, 1) || '%'
);

UPDATE nums SET val = 0 WHERE nums.val IS NULL AND LENGTH(nums.s) = 6;

INSERT OR REPLACE INTO nums
SELECT nums.id, nums.s, 3
FROM nums INNER JOIN nums AS n2 ON nums.id = n2.id AND n2.val = 1
WHERE (
    LENGTH(nums.s) = 5 AND
    nums.s LIKE '%' || SUBSTR(n2.s, 1, 1) || '%' AND
    nums.s LIKE '%' || SUBSTR(n2.s, 2, 1) || '%'
);

INSERT OR REPLACE INTO nums
SELECT nums.id, nums.s, 5
FROM nums INNER JOIN nums AS n2 ON nums.id = n2.id AND n2.val = 6
WHERE (
    LENGTH(nums.s) = 5 AND
    n2.s LIKE '%' || SUBSTR(nums.s, 1, 1) || '%' AND
    n2.s LIKE '%' || SUBSTR(nums.s, 2, 1) || '%' AND
    n2.s LIKE '%' || SUBSTR(nums.s, 3, 1) || '%' AND
    n2.s LIKE '%' || SUBSTR(nums.s, 4, 1) || '%' AND
    n2.s LIKE '%' || SUBSTR(nums.s, 5, 1) || '%'
);

UPDATE nums SET val = 2 WHERE nums.val IS NULL;

CREATE TABLE outputs (id, pos, s);
WITH RECURSIVE nn (pos, s, rest) AS (
    SELECT -1, '', (SELECT SUBSTR(s, INSTR(s, '|') + 2) || char(10) FROM input)
    UNION ALL
    SELECT
        nn.pos + 1,
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
INSERT INTO outputs
SELECT
    CAST(nn.pos / 4 AS INT),
    nn.pos % 4,
    (CASE nn.s LIKE '%a%' WHEN 1 THEN 'a' ELSE '' END) ||
    (CASE nn.s LIKE '%b%' WHEN 1 THEN 'b' ELSE '' END) ||
    (CASE nn.s LIKE '%c%' WHEN 1 THEN 'c' ELSE '' END) ||
    (CASE nn.s LIKE '%d%' WHEN 1 THEN 'd' ELSE '' END) ||
    (CASE nn.s LIKE '%e%' WHEN 1 THEN 'e' ELSE '' END) ||
    (CASE nn.s LIKE '%f%' WHEN 1 THEN 'f' ELSE '' END) ||
    (CASE nn.s LIKE '%g%' WHEN 1 THEN 'g' ELSE '' END)
FROM nn  WHERE nn.pos >= 0;

SELECT SUM(
    (
        CASE outputs.pos
            WHEN 0 THEN 1000
            WHEN 1 THEN 100
            WHEN 2 THEN 10
            WHEN 3 THEN 1
        END
    ) * nums.val
)
FROM outputs
INNER JOIN nums ON nums.id = outputs.id AND nums.s = outputs.s;
