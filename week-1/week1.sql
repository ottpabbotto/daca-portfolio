-- Mitu toodet on kokku?    
SELECT COUNT(*) AS toodete_arv FROM products;

-- Millised veerud ja andmed tabelis on?    
SELECT * FROM products LIMIT 10;

-- Kõik unikaalsed tootekategooriad    
SELECT DISTINCT category FROM products; 

-- 10 kalleimat toodet    
SELECT product_name, category, retail_price    
FROM products    
ORDER BY retail_price DESC    
LIMIT 10;

-- 10 odavaimat toodet
SELECT product_name, category, retail_price    
FROM products    
ORDER BY retail_price ASC    
LIMIT 10;

-- Kõik kindla kategooria tooted    
SELECT * FROM products    
WHERE category = 'naiste_riided'    
ORDER BY retail_price DESC;

-- Puuduvad hinnad    
SELECT COUNT(*) - COUNT(retail_price) AS puuduvad_hinnad    
FROM products;

--Puuduvad kategooriad    
SELECT COUNT(*) - COUNT(category) AS puuduvad_kategooriad
FROM products; 