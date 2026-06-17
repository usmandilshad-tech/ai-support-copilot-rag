from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from src.utils.config import DATABASE_URL, PROJECT_ROOT


DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_support_tickets.csv"
TABLE_NAME = "support_tickets"


def load_cleaned_data(data_path: Path = DATA_PATH) -> pd.DataFrame:
    """Load cleaned support ticket data from CSV."""
    if not data_path.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found at {data_path}. "
            "Run notebooks/01_data_exploration.ipynb first."
        )

    df = pd.read_csv(data_path)

    return df


def validate_required_columns(df: pd.DataFrame) -> None:
    """Validate that required database columns exist in the dataset."""
    required_columns = [
        "ticket_id",
        "customer_age",
        "customer_gender",
        "product_purchased",
        "date_of_purchase",
        "ticket_type",
        "ticket_subject",
        "ticket_description",
        "ticket_text",
        "ticket_status",
        "resolution",
        "ticket_priority",
        "ticket_channel",
        "first_response_time",
        "time_to_resolution",
        "customer_satisfaction_rating",
        "description_length",
        "subject_length",
        "resolution_length",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def prepare_for_database(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare dataframe before loading into MySQL."""
    df = df.copy()

    expected_columns = [
        "ticket_id",
        "customer_age",
        "customer_gender",
        "product_purchased",
        "date_of_purchase",
        "ticket_type",
        "ticket_subject",
        "ticket_description",
        "ticket_text",
        "ticket_status",
        "resolution",
        "ticket_priority",
        "ticket_channel",
        "first_response_time",
        "time_to_resolution",
        "customer_satisfaction_rating",
        "description_length",
        "subject_length",
        "resolution_length",
        "resolution_was_missing",
        "customer_satisfaction_rating_was_missing",
        "first_response_time_was_missing",
        "time_to_resolution_was_missing",
        "ticket_description_was_missing",
        "ticket_subject_was_missing",
    ]

    # Add any missing expected columns
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0 if col.endswith("_was_missing") else None

    # Keep only the columns that exist in the MySQL table
    df = df[expected_columns]

    # Ensure ticket_id is string
    df["ticket_id"] = df["ticket_id"].astype(str)

    numeric_columns = [
        "customer_age",
        "customer_satisfaction_rating",
        "description_length",
        "subject_length",
        "resolution_length",
        "resolution_was_missing",
        "customer_satisfaction_rating_was_missing",
        "first_response_time_was_missing",
        "time_to_resolution_was_missing",
        "ticket_description_was_missing",
        "ticket_subject_was_missing",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(-1)

    text_columns = [
        "customer_gender",
        "product_purchased",
        "date_of_purchase",
        "ticket_type",
        "ticket_subject",
        "ticket_description",
        "ticket_text",
        "ticket_status",
        "resolution",
        "ticket_priority",
        "ticket_channel",
        "first_response_time",
        "time_to_resolution",
    ]

    for col in text_columns:
        df[col] = df[col].fillna("Not available").astype(str)

    return df


def load_to_mysql(df: pd.DataFrame, table_name: str = TABLE_NAME) -> None:
    """Load dataframe into MySQL table."""
    engine = create_engine(DATABASE_URL)

    with engine.begin() as connection:
        connection.execute(text(f"TRUNCATE TABLE {table_name}"))

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=200,
        method=None,
    )


def verify_load(table_name: str = TABLE_NAME) -> None:
    """Verify row count after loading data."""
    engine = create_engine(DATABASE_URL)

    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        row_count = result.scalar()

    print(f"Rows loaded into {table_name}: {row_count}")


def main() -> None:
    print("Loading cleaned support ticket data...")
    df = load_cleaned_data()

    print(f"Loaded dataframe with shape: {df.shape}")

    print("Validating required columns...")
    validate_required_columns(df)

    print("Preparing data for database...")
    prepared_df = prepare_for_database(df)

    print("Loading data into MySQL...")
    load_to_mysql(prepared_df)

    print("Verifying database load...")
    verify_load()

    print("Database loading completed successfully.")


if __name__ == "__main__":
    main()