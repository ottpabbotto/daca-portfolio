-- INNER JOIN: kliendid koos nende müükidega
SELECT
    c.first_name,
    c.last_name,
    c.city,
    s.sale_id,
    s.sale_date,
    s.total_price
FROM sales s
INNER JOIN customers c ON s.customer_id = c.customer_id
ORDER BY s.total_price DESC
LIMIT 20;
-- Enamus Tallinnast
-- Madis Roots, 2170.40 eur


-- INNER JOIN: kliendid koos nende müükidega
SELECT
    c.first_name,
    c.last_name,
    c.city,
    s.sale_id,
    s.sale_date,
    s.total_price
FROM sales s
INNER JOIN customers c ON s.customer_id = c.customer_id
ORDER BY s.total_price DESC;
-- 9130 rows

--Ise kirjutatud päring
SELECT
    p.product_name,
    p.category,
    s.quantity,
    s.unit_price
FROM sales s
INNER JOIN products p ON s.product_id = p.product_id
ORDER BY s.quantity DESC
LIMIT 15;
--

--Oma päring 2
SELECT 
    c.city, 
    COUNT(s.sale_id) AS tellimuste_arv,
    SUM(s.total_price) AS kogumyyk
FROM sales s
INNER JOIN customers c ON s.customer_id = c.customer_id
GROUP BY c.city
ORDER BY kogumyyk DESC;

-- kõik kliendid, ka need kes pole ostnud
SELECT
    c.first_name,
    c.last_name,
    c.city,
    s.sale_id,
    s.total_price
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
ORDER BY s.total_price DESC NULLS LAST;

-- Kliendid, kes pole KUNAGI ostnud
SELECT
    c.first_name,
    c.last_name,
    c.email,
    c.city,
    c.registration_date
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL;

-- Kadunud kliendid: LEFT JOIN + WHERE IS NULL
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS nimi,
    c.email,
    c.city,
    c.registration_date
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
ORDER BY c.registration_date ASC;
-- 599 rida
-- vanim kadunud klient 2.1.20, Erkki Ilves

-- Kadunud kliente per linn
SELECT
    c.city,
    COUNT(*) AS kadunud_klientide_arv
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
GROUP BY c.city
ORDER BY kadunud_klientide_arv DESC
LIMIT 1;
-- Tallinn, 231 klienti

-- Oma päring
SELECT
    p.product_name,    -- Toote nimi
    p.category,        -- Kategooria
    p.retail_price     -- Jaemüügi hind
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id
WHERE s.sale_id IS NULL;
-- 12 toodet
-- aksessuaarid (5)

-- Oma päring 2
SELECT
    c.city,
    COUNT(c.customer_id) AS kadunud_klientide_arv
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
GROUP BY c.city
ORDER BY kadunud_klientide_arv DESC;

-- Right join
SELECT
    c.first_name || ' ' || c.last_name AS klient,
    c.city,
    s.sale_date,
    s.total_price,
    p.product_name,
    p.category,
    s.quantity,
    s.unit_price
FROM sales s
INNER JOIN customers c ON s.customer_id = c.customer_id
INNER JOIN products p ON s.product_id = p.product_id
ORDER BY s.total_price DESC
LIMIT 20;

-- 3 tabeli JOIN: kes ostis mida?
SELECT
    c.first_name || ' ' || c.last_name AS klient,
    c.city AS linn,
    s.sale_date AS müügi_kuupäev,
    p.product_name AS toode,
    p.category AS kategooria,
    s.quantity AS kogus,
    s.unit_price AS ühikuhind,
    s.total_price AS rea_summa
FROM sales s
INNER JOIN customers c ON s.customer_id = c.customer_id
INNER JOIN products p ON s.product_id = p.product_id
ORDER BY rea_summa DESC
LIMIT 20;
-- Õhuline sünteetiline sporditossud
-- Valga
-- jalanõud

-- Müük linnade ja kategooriate kaupa
SELECT
    c.city,                      -- Linn klientide tabelist
    p.category,                  -- Kategooria toodete tabelist
    SUM(s.total_price) AS kogumyyk, -- Arvutame kogumüügi
    COUNT(s.sale_id) AS tehingute_arv -- Lisame ka tehingute arvu kontekstiks
FROM sales s
INNER JOIN customers c ON s.customer_id = c.customer_id -- Ühendame kliendiinfoga
INNER JOIN products p ON s.product_id = p.product_id   -- Ühendame tooteinfoga
GROUP BY c.city, p.category      -- Grupeerime nii linna kui kategooria järgi
ORDER BY kogumyyk DESC;          -- Sorteerime suurima tulu järgi
-- jalanõud Tallinnas
-- Tartu eelistab meesteriideid, Tallinn jalanõusid, muus osas kattub
-- lasteriided on selgelt kõige vähem eelistatum