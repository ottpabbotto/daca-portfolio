-- Toodete arv kategooriate kaupa
SELECT category, 
COUNT(*) AS toodete_arv   
FROM products   
GROUP BY category   
ORDER BY toodete_arv DESC; 

-- Keskmised hinnad kategooriate kaupa
SELECT category,          
COUNT(*) AS toodete_arv,          
MIN(retail_price) AS min_hind,          
MAX(retail_price) AS max_hind   
FROM products   
GROUP BY category   
ORDER BY max_hind DESC;

-- Tooted üle 50 euro konkreetses kategoorias
SELECT * FROM products   
WHERE retail_price > 50 AND category = 'naiste_riided'   
ORDER BY retail_price DESC;