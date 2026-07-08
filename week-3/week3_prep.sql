-- Kustuta duplikaadid sales tabelist (sama loogika mis W2 sales_test peal)
DELETE FROM sales
WHERE id NOT IN (
    SELECT MIN(id)
    FROM sales
    GROUP BY sale_id
);

-- Paranda tuleviku kuupäevad
UPDATE sales
SET sale_date = CURRENT_DATE
WHERE sale_date > CURRENT_DATE;

-- Ühtlusta klientide linnanimed (muidu GROUP BY city näitab 50+ varianti 12 asemel)
UPDATE customers
SET city = INITCAP(TRIM(city))
WHERE city IS NOT NULL;

-- Kontrolli tulemusi
SELECT COUNT(*) AS sales_ridu FROM sales;           
-- Oodatav: ~10 118
SELECT COUNT(DISTINCT city) AS linnu FROM customers; 
-- Oodatav: 12