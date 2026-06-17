CREATE DATABASE IF NOT EXISTS support_copilot_db;

USE support_copilot_db;

DROP TABLE IF EXISTS support_tickets;

CREATE TABLE support_tickets (
    ticket_id VARCHAR(50) PRIMARY KEY,
    customer_age INT,
    customer_gender VARCHAR(50),
    product_purchased VARCHAR(255),
    date_of_purchase VARCHAR(100),
    ticket_type VARCHAR(100),
    ticket_subject TEXT,
    ticket_description TEXT,
    ticket_text TEXT,
    ticket_status VARCHAR(100),
    resolution TEXT,
    ticket_priority VARCHAR(100),
    ticket_channel VARCHAR(100),
    first_response_time VARCHAR(100),
    time_to_resolution VARCHAR(100),
    customer_satisfaction_rating FLOAT,
    description_length INT,
    subject_length INT,
    resolution_length INT,

    resolution_was_missing INT DEFAULT 0,
    customer_satisfaction_rating_was_missing INT DEFAULT 0,
    first_response_time_was_missing INT DEFAULT 0,
    time_to_resolution_was_missing INT DEFAULT 0,
    ticket_description_was_missing INT DEFAULT 0,
    ticket_subject_was_missing INT DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);