USE support_copilot_db;

-- 1. Total tickets
SELECT COUNT(*) AS total_tickets
FROM support_tickets;

-- 2. Tickets by type
SELECT 
    ticket_type,
    COUNT(*) AS ticket_count
FROM support_tickets
GROUP BY ticket_type
ORDER BY ticket_count DESC;

-- 3. Tickets by priority
SELECT 
    ticket_priority,
    COUNT(*) AS ticket_count
FROM support_tickets
GROUP BY ticket_priority
ORDER BY ticket_count DESC;

-- 4. Tickets by status
SELECT 
    ticket_status,
    COUNT(*) AS ticket_count
FROM support_tickets
GROUP BY ticket_status
ORDER BY ticket_count DESC;

-- 5. Tickets by channel
SELECT 
    ticket_channel,
    COUNT(*) AS ticket_count
FROM support_tickets
GROUP BY ticket_channel
ORDER BY ticket_count DESC;

-- 6. Average satisfaction by ticket type
SELECT 
    ticket_type,
    ROUND(AVG(NULLIF(customer_satisfaction_rating, -1)), 2) AS avg_satisfaction
FROM support_tickets
GROUP BY ticket_type
ORDER BY avg_satisfaction DESC;

-- 7. Average satisfaction by channel
SELECT 
    ticket_channel,
    ROUND(AVG(NULLIF(customer_satisfaction_rating, -1)), 2) AS avg_satisfaction
FROM support_tickets
GROUP BY ticket_channel
ORDER BY avg_satisfaction DESC;

-- 8. High priority or critical tickets
SELECT 
    ticket_id,
    ticket_type,
    ticket_priority,
    ticket_status,
    ticket_channel,
    ticket_subject
FROM support_tickets
WHERE ticket_priority IN ('High', 'Critical')
LIMIT 50;

-- 9. Missing resolution by status
SELECT
    ticket_status,
    COUNT(*) AS total_tickets,
    SUM(resolution_was_missing) AS missing_resolution_count,
    ROUND(SUM(resolution_was_missing) / COUNT(*) * 100, 2) AS missing_resolution_percentage
FROM support_tickets
GROUP BY ticket_status
ORDER BY missing_resolution_percentage DESC;

-- 10. Top products by ticket volume
SELECT 
    product_purchased,
    COUNT(*) AS ticket_count
FROM support_tickets
GROUP BY product_purchased
ORDER BY ticket_count DESC
LIMIT 10;