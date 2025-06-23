
-- SEGMENTAÇÃO RFM COM STATUS DE CLIENTES
WITH recencia AS (
    SELECT 
        c.customer_id AS cliente,
        MAX(o.order_date) AS data_ultima_compra,
        (SELECT MAX(order_date) FROM orders) - MAX(o.order_date) AS dias_ultima_compra
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
),
frequencia AS (
    SELECT 
        c.customer_id AS cliente,
        COUNT(o.customer_id) AS qnt_pedidos
    FROM customers c 
    INNER JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
),
monetario AS (
    SELECT 
        c.customer_id AS cliente,
        COUNT(DISTINCT o.order_id) AS pedidos_distintos,
        SUM(od.unit_price * od.quantity) AS total_gasto,
        SUM(od.unit_price * od.quantity) / COUNT(o.order_id) AS ticket_medio
    FROM customers c 
    INNER JOIN orders o ON c.customer_id = o.customer_id
    INNER JOIN order_details od ON o.order_id = od.order_id
    GROUP BY c.customer_id	
)
SELECT 
    recencia.cliente,
    recencia.dias_ultima_compra,
    frequencia.qnt_pedidos,
    monetario.total_gasto,
    ROUND(monetario.ticket_medio, 2) AS ticket_medio,
    CASE 
        WHEN recencia.dias_ultima_compra <= 30 AND frequencia.qnt_pedidos >= 5 THEN 'Cliente Ativo'
        WHEN recencia.dias_ultima_compra BETWEEN 31 AND 90 THEN 'Risco de Churn'
        WHEN recencia.dias_ultima_compra > 90 THEN 'Cliente Inativo'
        ELSE 'Novo Cliente'
    END AS status_cliente
FROM recencia
JOIN frequencia USING (cliente)
JOIN monetario USING (cliente);

-- CONTAGEM DE CLIENTES POR STATUS
WITH contagem AS (
    SELECT 
        c.customer_id AS codigo_cliente,
        COUNT(od.quantity) AS qnt_pedidos,
        (SELECT MAX(order_date) FROM orders) - MAX(o.order_date) AS dias_ultima_compra
    FROM customers c 
    INNER JOIN orders o ON c.customer_id = o.customer_id
    INNER JOIN order_details od ON o.order_id = od.order_id 
    GROUP BY c.customer_id
)	
SELECT 
    CASE 
        WHEN dias_ultima_compra <= 30 AND qnt_pedidos >= 5 THEN 'Cliente Ativo'
        WHEN dias_ultima_compra BETWEEN 31 AND 90 THEN 'Risco de Churn'
        WHEN dias_ultima_compra > 90 THEN 'Cliente Inativo'
        ELSE 'Novo Cliente'
    END AS status_cliente,
    COUNT(DISTINCT codigo_cliente) AS quantidade_clientes
FROM contagem
GROUP BY status_cliente
ORDER BY quantidade_clientes DESC;
