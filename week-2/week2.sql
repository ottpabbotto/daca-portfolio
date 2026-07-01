-- Orbid müügid — kas on customer_id, mida pole customers tabelis?
SELECT COUNT(*) AS orb_klient
FROM sales
WHERE customer_id IS NOT NULL
  AND customer_id NOT IN (SELECT customer_id FROM customers WHERE customer_id IS NOT NULL);

-- orb_client = 0

-- Orbid müügid — kas on product_id, mida pole products tabelis?
SELECT COUNT(*) AS orb_toode
FROM sales
WHERE product_id IS NOT NULL
  AND product_id NOT IN (SELECT product_id FROM products WHERE product_id IS NOT NULL);

-- orb_toode = 0

SELECT COUNT(*) AS vaimkliendid
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM sales WHERE customer_id IS NOT NULL);

-- vaimkliendid = 592

SELECT COUNT(*) AS vaimtooted
FROM products
WHERE product_id NOT IN (SELECT product_id FROM sales WHERE product_id IS NOT NULL);

-- vaimtooted = 12