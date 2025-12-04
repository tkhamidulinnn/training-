import os
import logging
import sys
from datetime import datetime

# INSTALLATION: pip install pandas sqlalchemy psycopg2-binary
import pandas as pd
from sqlalchemy import create_engine

# ==========================================
# 🏭 ETL CONFIGURATION (REQUIRED)
# ==========================================
# Database connection string (PostgreSQL)
DB_CONNECTION_URI = os.getenv("DB_URI", "postgresql://user:pass@localhost:5432/warehouse")
# Source data directory
SOURCE_DATA_PATH = os.getenv("SOURCE_PATH", "./data/input")
# Batch size for processing
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))
# Archive processed files?
ARCHIVE_ENABLED = os.getenv("ARCHIVE_PROCESSED", "True").lower() == "true"

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ETL_Worker")

class DataPipeline:
    """
    Extract-Transform-Load (ETL) pipeline for processing sales data.
    Reads CSVs, cleans data, and uploads to the Data Warehouse.
    """

    def __init__(self):
        if "user:pass" in DB_CONNECTION_URI:
            logger.warning("Using default DB credentials! Set DB_URI env var in production.")
        
        self.engine = create_engine(DB_CONNECTION_URI)

    def extract(self, filename: str) -> pd.DataFrame:
        """
        Reads raw data from CSV file.
        """
        file_path = os.path.join(SOURCE_DATA_PATH, filename)
        logger.info(f"Extracting data from {file_path}...")
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            logger.error(f"File not found: {filename}")
            sys.exit(1)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans data: removes nulls, formats dates, calculates totals.
        """
        logger.info("Transforming data...")
        df = df.dropna() # Remove empty rows
        df['total_amount'] = df['quantity'] * df['unit_price'] # Calculate total
        df['processed_at'] = datetime.now()
        return df

    def load(self, df: pd.DataFrame, table_name: str):
        """
        Uploads processed data to SQL database.
        """
        logger.info(f"Loading {len(df)} rows into {table_name}...")
        df.to_sql(table_name, self.engine, if_exists='append', index=False)
        logger.info("Load complete.")

if __name__ == "__main__":
    # Usage: python etl_pipeline.py
    pipeline = DataPipeline()
    raw_data = pipeline.extract("sales_2025.csv")
    clean_data = pipeline.transform(raw_data)
    pipeline.load(clean_data, "sales_report")
