-- kliendid, kes on ostnud
SELECT        
c.first_name,        
c.last_name,        
c.email,        
c.city,        
s.sale_id,        
s.sale_date,        
s.total_price    
FROM sales s    
INNER JOIN customers c ON s.customer_id = c.customer_id    
LIMIT 20;

-- TOP 10 klienti kogumüügi järgi
SELECT        
c.first_name || ' ' || c.last_name AS klient,        
c.city,        
COUNT(DISTINCT s.sale_id) AS ostude_arv,        
SUM(s.total_price) AS kogumüük    
FROM sales s    
INNER JOIN customers c ON s.customer_id = c.customer_id    
GROUP BY c.customer_id, c.first_name, c.last_name, c.city    
ORDER BY kogumüük DESC    
LIMIT 10;

-- müük linnade kaupa    
SELECT        
c.city,        
COUNT(DISTINCT c.customer_id) AS kliente,        
COUNT(s.sale_id) AS oste,        
SUM(s.total_price) AS kogumüük    
FROM sales s    
INNER JOIN customers c ON s.customer_id = c.customer_id    
GROUP BY c.city    
ORDER BY kogumüük DESC;

-- müük lojaalsustasemete kaupa    
SELECT        
c.loyalty_tier,        
COUNT(DISTINCT c.customer_id) AS kliente,        
SUM(s.total_price) AS kogumüük    
FROM sales s    
INNER JOIN customers c ON s.customer_id = c.customer_id    
GROUP BY c.loyalty_tier    
ORDER BY kogumüük DESC;

-- kliendid, kelle kogumüük on üle keskmise
SELECT       
c.first_name || ' ' || c.last_name AS klient,       
SUM(s.total_price) AS kogumüük   
FROM sales s   
INNER JOIN customers c ON s.customer_id = c.customer_id   
GROUP BY c.customer_id, c.first_name, c.last_name   
HAVING SUM(s.total_price) > 
(SELECT AVG(kliendi_müük)       
FROM (SELECT SUM(total_price) AS kliendi_müük           
FROM sales           
GROUP BY customer_id) AS keskmised)   
ORDER BY kogumüük DESC;   