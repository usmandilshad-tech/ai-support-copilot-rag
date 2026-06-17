# SQL Data Pipeline

## Purpose

This project loads cleaned customer support ticket data into a MySQL database to support analytics, dashboarding, and API-based retrieval.

## Database

Database name:

`support_copilot_db`

Main table:

`support_tickets`

## Pipeline Flow

1. Raw Kaggle dataset is cleaned in `notebooks/01_data_exploration.ipynb`.
2. Cleaned data is saved to `data/processed/cleaned_support_tickets.csv`.
3. MySQL schema is created using `sql/create_tables.sql`.
4. Data is loaded into MySQL using `src/data/db_loader.py`.
5. Analytical queries and views are stored in `sql/sample_queries.sql` and `sql/views.sql`.

## Key Skills Demonstrated

- MySQL database design
- SQL table creation
- Python-based ETL loading
- SQLAlchemy database connection
- Data validation before loading
- Missing-value indicator preservation
- Dashboard-ready SQL views

## Verification

The database was successfully loaded with 8,469 support ticket records.

Sample ticket count by type:

| Ticket Type | Count |
|---|---:|
| Refund request | 1,752 |
| Technical issue | 1,747 |
| Cancellation request | 1,695 |
| Product inquiry | 1,641 |
| Billing inquiry | 1,634 |

## Notes

The dataset contains synthetic customer support records. During earlier modeling, label quality issues were identified in the `ticket_type` field, so this dataset is used primarily for SQL analytics, dashboarding, RAG assistance, and workflow simulation.