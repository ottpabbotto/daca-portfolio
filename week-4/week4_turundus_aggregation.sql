WITH kliendi_kokkuvote AS (      
  SELECT        
  c.customer_id,        
  c.first_name || ' ' || c.last_name AS nimi,        
  c.city,        
  COUNT(o.sale_id) AS tellimuste_arv,        
  SUM(o.total_price) AS kogukäive      
  FROM customers c      
  JOIN sales o ON c.customer_id = o.customer_id      
  GROUP BY c.customer_id, c.first_name, c.last_name, c.city    )    
  SELECT      
  nimi,      
  city,      
  tellimuste_arv,      
  kogukäive,      
  CASE        
  WHEN kogukäive > 800 THEN 'VIP'       -- vali ise piir!        
  WHEN kogukäive > 100 THEN 'Regular'    -- vali ise piir!        
  ELSE 'Uus'      
  END AS segment    
  FROM kliendi_kokkuvote    
  ORDER BY kogukäive DESC;

-- TOP 10 klienti
SELECT
  c.customer_id,
  c.first_name || ' ' || c.last_name AS nimi,
  COUNT(s.sale_id) AS tellimuste_arv,
  SUM(s.total_price) AS kogukaive
FROM customers c
INNER JOIN sales s ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(s.sale_id) >= 2
ORDER BY kogukaive DESC
LIMIT 10;

-- Mitu klienti on igas segmendis?
WITH kliendi_statistika AS (
    -- iga kliendi kogukäive, kus NULL väärtused asendatud nulliga
    SELECT 
        c.customer_id,
        COALESCE(SUM(s.total_price), 0) AS kogukaive
    FROM customers c
    LEFT JOIN sales s ON c.customer_id = s.customer_id
    GROUP BY c.customer_id
),
kliendi_segmendid AS (
    SELECT 
        customer_id,
        CASE 
            WHEN kogukaive > 800 THEN 'VIP'
            WHEN kogukaive BETWEEN 100 AND 800 THEN 'Regular'
            WHEN kogukaive BETWEEN 0 AND 100 THEN 'Uus'
            ELSE '?'
        END AS segment
    FROM kliendi_statistika
)
SELECT 
    segment,
    COUNT(*) AS klientide_arv
FROM kliendi_segmendid
GROUP BY segment
ORDER BY klientide_arv DESC;

-- Iga segmendi keskmine käive
WITH kliendi_kogutulu AS (
    SELECT 
      c.customer_id,
      COALESCE(SUM(s.total_price), 0) AS kogutulu
    FROM customers c
    LEFT JOIN sales s ON c.customer_id = s.customer_id
    GROUP BY c.customer_id
),
segmentide_maaramine AS (
    -- segmendid vastavalt käibepiiridele
    SELECT 
        kogutulu,
        CASE 
            WHEN kogutulu > 800 THEN 'VIP'
            WHEN kogutulu BETWEEN 100 AND 800 THEN 'Regular'
            WHEN kogutulu BETWEEN 0 AND 100 THEN 'Uus'
            ELSE '?'
        END AS segment
    FROM kliendi_kogutulu
)
-- iga segmendi keskmine käive kliendi kohta
SELECT 
    segment,
    COUNT(*) AS klientide_arv,
    ROUND(AVG(kogutulu), 2) AS keskmine_kaive_kliendi_kohta
FROM segmentide_maaramine
GROUP BY segment
ORDER BY keskmine_kaive_kliendi_kohta DESC;

-- VIP kliendid linnade kaupa
WITH kliendi_koond AS (
    -- kliendid, kelle käive ületab 800€
    SELECT 
        customer_id, 
        SUM(total_price) AS kogukaive
    FROM sales
    GROUP BY customer_id
    HAVING SUM(total_price) > 800
)
-- JOIN klientide tabeliga, et näha asukohta
SELECT 
    c.city, 
    COUNT(*) AS vip_klientide_arv
FROM customers c
JOIN kliendi_koond k ON c.customer_id = k.customer_id
GROUP BY c.city
ORDER BY vip_klientide_arv DESC;

-- keskmine kogukäive kliendi kohta
WITH kliendi_kogutulud AS (
    SELECT 
        c.customer_id,
        COALESCE(SUM(s.total_price), 0) AS kogutulu
    FROM customers c
    LEFT JOIN sales s ON c.customer_id = s.customer_id
    GROUP BY c.customer_id
)
SELECT 
    ROUND(AVG(kogutulu), 2) AS keskmine_kogukaive_kliendi_kohta
FROM kliendi_kogutulud;

-- tulemused linna piires
WITH kliendi_kokkuvote AS (
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS nimi,
        c.city,
        COUNT(o.sale_id) AS tellimuste_arv,
        SUM(o.total_price) AS kogukäive
    FROM customers c
    JOIN sales o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.city
)
SELECT
    nimi,
    city,
    tellimuste_arv,
    kogukäive,
    CASE
        WHEN kogukäive > 800 THEN 'VIP'
        WHEN kogukäive > 100 THEN 'Regular'
        ELSE 'Uus'
    END AS segment,
    -- Lisatud akna funktsioon kliendi järjestamiseks linna piires
    RANK() OVER (
        PARTITION BY city
        ORDER BY kogukäive DESC
    ) AS koht_linnas
FROM kliendi_kokkuvote
ORDER BY city, koht_linnas;

-- TOP 20 klienti
WITH kliendi_kokkuvote AS (
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS nimi,
        c.city,
        COUNT(o.sale_id) AS tellimuste_arv,
        SUM(o.total_price) AS kogukäive
    FROM customers c
    JOIN sales o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.city
)
SELECT
    nimi,
    city,
    tellimuste_arv,
    kogukäive,
    CASE
        WHEN kogukäive > 800 THEN 'VIP'
        WHEN kogukäive > 100 THEN 'Regular'
        ELSE 'Uus'
    END AS segment,
    -- Üldine pingerida üle kogu ettevõtte
    RANK() OVER (ORDER BY kogukäive DESC) AS üldine_koht
FROM kliendi_kokkuvote
-- Filtreerime ainult positiivse käibega tehingud (igaks juhuks, kui on tagastusi)
WHERE kogukäive > 0
ORDER BY kogukäive DESC
LIMIT 20;

-- Iga linna TOP 5 klienti kogukäibe järgi
WITH kliendi_kokkuvote AS (
    -- Samm 1: Agregeerime müügid kliendi tasemele
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS nimi,
        c.city,
        COUNT(o.sale_id) AS tellimuste_arv,
        SUM(o.total_price) AS kogukäive
    FROM customers c
    JOIN sales o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.city
),
linna_edetabel AS (
    -- segmendid ja järjestus iga linna sees
    SELECT
        *,
        CASE
            WHEN kogukäive > 800 THEN 'VIP'
            WHEN kogukäive > 100 THEN 'Regular'
            ELSE 'Uus'
        END AS segment,
        -- PARTITION BY city jagab andmed rühmadesse linna järgi
        RANK() OVER (
            PARTITION BY city 
            ORDER BY kogukäive DESC
        ) AS koht_linnas
    FROM kliendi_kokkuvote
    WHERE kogukäive > 0
)
-- igast linnast TOP 5 ja järjestame kogukäibe järgi
SELECT
    nimi,
    city,
    tellimuste_arv,
    kogukäive,
    segment,
    koht_linnas
FROM linna_edetabel
WHERE koht_linnas <= 5
ORDER BY kogukäive DESC;

-- keskmine käive miinuses
SELECT 
    c.customer_id, 
    c.first_name || ' ' || c.last_name AS nimi, 
    ROUND(AVG(s.total_price), 2) AS keskmine_kaive
FROM customers c
JOIN sales s ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING AVG(s.total_price) < 0
ORDER BY keskmine_kaive ASC;

-- keskmine kogukäive koos ja ilma miinustes klientidega
WITH kliendi_statistika AS (
    -- iga unikaalse kliendi kogukäive ja keskmise tehingu väärtus
    SELECT 
        c.customer_id,
        COALESCE(SUM(s.total_price), 0) AS kogutulu,
        AVG(s.total_price) AS keskmine_tehinguväärtus,
        COUNT(s.sale_id) AS ostude_arv
    FROM customers c
    -- Kaasa need 47 klienti, kes pole veel ostnud [3, 4]
    LEFT JOIN sales s ON c.customer_id = s.customer_id
    GROUP BY c.customer_id
)
  -- koondnäitajad üle kogu kliendibaasi
SELECT 
    -- keskmine (sisaldab kõiki registreeritud kliente)
    ROUND(AVG(kogutulu), 2) AS üldine_keskmine_kogukaive,
    
    -- puhastatud keskmine (eemaldab kliendid, kelle tehingute keskmine on miinuses)
    ROUND(AVG(CASE 
        WHEN keskmine_tehinguväärtus >= 0 OR ostude_arv = 0 THEN kogutulu 
    END), 2) AS puhastatud_keskmine_kogukaive
FROM kliendi_statistika;