USE support_copilot_db;

CREATE OR REPLACE VIEW vw_ticket_volume_by_type AS
SELECT 
    ticket_type,
    COUNT(*) AS ticket_count
FROM support_tickets
GROUP BY ticket_type;

CREATE OR REPLACE VIEW vw_ticket_volume_by_priority AS
SELECT 
    ticket_priority,
    COUNT(*) AS ticket_count
FROM support_tickets
GROUP BY ticket_priority;

CREATE OR REPLACE VIEW vw_ticket_volume_by_channel AS
SELECT 
    ticket_channel,
    COUNT(*) AS ticket_count
FROM support_tickets
GROUP BY ticket_channel;

CREATE OR REPLACE VIEW vw_satisfaction_by_type AS
SELECT 
    ticket_type,
    ROUND(AVG(NULLIF(customer_satisfaction_rating, -1)), 2) AS avg_satisfaction,
    COUNT(*) AS ticket_count
FROM support_tickets
GROUP BY ticket_type;

CREATE OR REPLACE VIEW vw_support_kpi_summary AS
SELECT
    COUNT(*) AS total_tickets,
    SUM(CASE WHEN ticket_status = 'Open' THEN 1 ELSE 0 END) AS open_tickets,
    SUM(CASE WHEN ticket_status = 'Closed' THEN 1 ELSE 0 END) AS closed_tickets,
    SUM(CASE WHEN ticket_priority = 'Critical' THEN 1 ELSE 0 END) AS critical_tickets,
    ROUND(AVG(NULLIF(customer_satisfaction_rating, -1)), 2) AS avg_satisfaction
FROM support_tickets;