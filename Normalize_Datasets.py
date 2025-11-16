"""
Normalize_Datasets.py
---------------------
Phase 1: Data Cleaning, Normalization, Feature Engineering, and Database Export.

This module reads the raw "Hospital Management System.xlsx" dataset, performs
data cleaning and feature normalization, engineers temporal and aggregate
features, documents the resulting schema, and exports all processed tables into
a normalized SQLite database located at data/hospital.db.

Dependencies:
    pandas, numpy, scikit-learn, sqlite3, openpyxl
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import sqlite3


# -------------------------------------------------------------------------
# 1. Project Paths
# -------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_FILE = os.path.join(DATA_DIR, "Hospital Management System.xlsx")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)


# -------------------------------------------------------------------------
# Utility Logging
# -------------------------------------------------------------------------
def log(msg: str):
    print(msg)


# -------------------------------------------------------------------------
# 2. Cleaning, Normalization, and Time Feature Extraction
# -------------------------------------------------------------------------
def clean_normalize_timeseries(file_path):
    """
    Reads an Excel workbook and performs cleaning, normalization,
    and feature extraction for each sheet.

    Returns:
        dict[str, pd.DataFrame]: Cleaned DataFrames by sheet name.
    """
    if not os.path.exists(file_path):
        log(f"File not found: {file_path}")
        return {}

    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    log(f"Loaded workbook with sheets: {sheet_names}")

    cleaned_dfs = {}

    for sheet in sheet_names:
        log(f"Processing sheet: {sheet}")
        df = pd.read_excel(xls, sheet_name=sheet)
        df.columns = df.columns.str.strip()

        # Remove duplicates and standardize missing values
        df.drop_duplicates(inplace=True)
        df.replace(['N/A', 'NA', 'NaN', 'null', '-', 'None', 'nan'], np.nan, inplace=True)

        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].astype(str).str.strip()

        # Convert date/time columns
        datetime_cols = []
        for col in df.columns:
            if any(x in col.lower() for x in ["date", "time", "timestamp"]):
                df[col] = pd.to_datetime(df[col], errors="coerce")
                datetime_cols.append(col)
        if datetime_cols:
            log(f"   Detected datetime columns: {datetime_cols}")

        # Attempt numeric conversion
        for col in df.columns:
            if df[col].dtype == object:
                try:
                    df[col] = pd.to_numeric(df[col])
                except Exception:
                    pass

        # Handle missing values
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col].fillna(df[col].mean(), inplace=True)
        for col in df.select_dtypes(exclude=[np.number]).columns:
            df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown", inplace=True)

        # Normalize numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            scaler = StandardScaler()
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
            log(f"   Normalized numeric columns: {numeric_cols}")

        # Encode categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            log(f"   Encoded categorical column: {col}")

        # Derive time-based features
        for col in datetime_cols:
            if df[col].notnull().any():
                df[f"{col}_year"] = df[col].dt.year
                df[f"{col}_month"] = df[col].dt.month
                df[f"{col}_day"] = df[col].dt.day
                df[f"{col}_hour"] = df[col].dt.hour
                df[f"{col}_weekday"] = df[col].dt.weekday
                df[f"{col}_is_weekend"] = (df[col].dt.weekday >= 5).astype(int)
                log(f"   Extracted features from {col}")

        # Normalize time-derived features
        time_features = [c for c in df.columns if any(x in c for x in ["_month", "_day", "_hour", "_weekday"])]
        if time_features:
            scaler = StandardScaler()
            df[time_features] = scaler.fit_transform(df[time_features])
            log(f"   Normalized time-based features: {time_features}")

        cleaned_dfs[sheet] = df
        log(f"   Completed sheet '{sheet}' ({len(df)} records).")

    log("All sheets processed successfully.\n")
    return cleaned_dfs


# -------------------------------------------------------------------------
# 3. Feature Engineering and Dataset Splitting
# -------------------------------------------------------------------------
def feature_engineer_and_split(cleaned_dfs):
    """
    Performs aggregate feature engineering and train/test splits.
    Produces documentation of all resulting columns.
    """
    log("Starting feature engineering and data partitioning.")

    schema_records = []

    for sheet_name, df in cleaned_dfs.items():
        log(f"Engineering features for: {sheet_name}")

        # Aggregate metrics
        if "patient_id" in df.columns and "doctor_id" in df.columns:
            agg = df.groupby("doctor_id")["patient_id"].count().reset_index(name="patients_per_doctor")
            df = df.merge(agg, on="doctor_id", how="left")

        if "bed_id" in df.columns and "patient_id" in df.columns:
            bed_util = df.groupby("bed_id")["patient_id"].count().reset_index(name="bed_usage_count")
            df = df.merge(bed_util, on="bed_id", how="left")

        if {"patients_per_doctor", "bed_usage_count"}.issubset(df.columns):
            df["bed_to_patient_ratio"] = df["bed_usage_count"] / (df["patients_per_doctor"] + 1)

        # Rolling features
        date_cols = [c for c in df.columns if "date" in c.lower() or "time" in c.lower()]
        if date_cols:
            df.sort_values(date_cols[0], inplace=True)
            df["record_count_cum"] = range(1, len(df) + 1)
            df["record_count_rolling7"] = df["record_count_cum"].rolling(window=7, min_periods=1).mean()

        # Train-test split
        split_prefix = sheet_name.lower().replace(' ', '_')
        if date_cols:
            cutoff = int(0.8 * len(df))
            train_df = df.iloc[:cutoff]
            test_df = df.iloc[cutoff:]
        else:
            train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

        train_df.to_csv(os.path.join(PROCESSED_DIR, f"{split_prefix}_train.csv"), index=False)
        test_df.to_csv(os.path.join(PROCESSED_DIR, f"{split_prefix}_test.csv"), index=False)

        # Schema documentation
        for col in df.columns:
            dtype = str(df[col].dtype)
            if "date" in col.lower() or "time" in col.lower():
                desc = "Date/Time Feature"
            elif np.issubdtype(df[col].dtype, np.number):
                desc = "Numeric Feature"
            else:
                desc = "Categorical/Encoded Feature"
            schema_records.append({"Sheet": sheet_name, "Column": col, "DataType": dtype, "Description": desc})

    schema_df = pd.DataFrame(schema_records)
    schema_path = os.path.join(PROCESSED_DIR, "schema_documentation.xlsx")
    schema_df.to_excel(schema_path, index=False)

    log("Feature engineering and documentation completed.\n")
    return schema_df


# -------------------------------------------------------------------------
# 4. Database Export
# -------------------------------------------------------------------------
def export_to_database(cleaned_dfs, db_type="sqlite",
                       db_name=os.path.join(DATA_DIR, "hospital.db"),
                       host="localhost", user="root", password=""):
    """
    Exports cleaned and processed DataFrames into a structured database.
    Defaults to SQLite (hospital.db) in the /data directory.
    """
    conn = None
    try:
        if db_type.lower() == "sqlite":
            conn = sqlite3.connect(db_name)
            log(f"Connected to SQLite database: {db_name}")
        elif db_type.lower() == "mysql":
            import mysql.connector
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            log(f"Connected to MySQL database: {db_name}@{host}")
        else:
            log("Unsupported database type. Use 'sqlite' or 'mysql'.")
            return

        for sheet_name, df in cleaned_dfs.items():
            table_name = sheet_name.lower().replace(" ", "_")
            log(f"Exporting {len(df)} rows to table '{table_name}'")
            if db_type.lower() == "sqlite":
                df.to_sql(table_name, conn, if_exists="replace", index=False)
            else:
                from sqlalchemy import create_engine
                engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}")
                df.to_sql(table_name, con=engine, if_exists="replace", index=False)

        if conn:
            conn.commit()
        log("All tables exported successfully.\n")

    except Exception as e:
        log(f"Error during database export: {e}")

    finally:
        if conn:
            conn.close()
            log("Database connection closed.")


# -------------------------------------------------------------------------
# 5. Entry Point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    # === Step 1: Load and clean dataset (normalized) ===
    cleaned_dfs = clean_normalize_timeseries(RAW_FILE)

    if cleaned_dfs:
        feature_engineer_and_split(cleaned_dfs)

        # ==============================================================
        # Step 2: Create a human-readable version before normalization
        # ==============================================================
        raw_xls = pd.ExcelFile(RAW_FILE)
        readable_dfs = {}

        for sheet in raw_xls.sheet_names:
            df = pd.read_excel(raw_xls, sheet_name=sheet)
            df.columns = df.columns.str.strip()
            df.drop_duplicates(inplace=True)

            # --- Specific corrections for known tables ---
            if "patient" in sheet.lower():
                # Combine firstname and lastname if available
                if any(col.lower() == "firstname" for col in df.columns) and any(col.lower() == "lastname" for col in df.columns):
                    first = next(col for col in df.columns if col.lower() == "firstname")
                    last = next(col for col in df.columns if col.lower() == "lastname")
                    df["name"] = df[first].astype(str) + " " + df[last].astype(str)
                elif any(col.lower() == "firstname" for col in df.columns):
                    first = next(col for col in df.columns if col.lower() == "firstname")
                    df["name"] = df[first]
                elif any(col.lower() == "lastname" for col in df.columns):
                    last = next(col for col in df.columns if col.lower() == "lastname")
                    df["name"] = df[last]

                # Ensure email exists
                email_cols = [c for c in df.columns if "email" in c.lower()]
                if not email_cols:
                    df["email"] = "unknown@example.com"
                else:
                    df[email_cols[0]].fillna("unknown@example.com", inplace=True)
                    if email_cols[0] != "email":
                        df.rename(columns={email_cols[0]: "email"}, inplace=True)


            elif sheet.lower() == "doctor":
                # Make sure each doctor has an email field
                if "email" not in df.columns:
                    df["email"] = "doctor@example.com"
                df["email"].fillna("doctor@example.com", inplace=True)

            elif sheet.lower() == "hospital":
                if "hospital_name" not in df.columns:
                    df["hospital_name"] = "Unnamed Hospital"
                if "address" not in df.columns:
                    df["address"] = "Unknown Address"

            elif sheet.lower() == "appointment":
                if "reason" not in df.columns:
                    df["reason"] = "General Checkup"
                if "mode_of_appointment" not in df.columns:
                    df["mode_of_appointment"] = "In-person"

            readable_dfs[sheet] = df

        # Export readable database for Flask/React
        export_to_database(
            readable_dfs,
            db_type="sqlite",
            db_name=os.path.join(DATA_DIR, "hospital_raw.db")
        )

        # ==============================================================
        # Step 3: Export normalized data for forecasting / AI
        # ==============================================================
        export_to_database(
            cleaned_dfs,
            db_type="sqlite",
            db_name=os.path.join(DATA_DIR, "hospital.db")
        )

        log("Exported both hospital_raw.db (readable) and hospital.db (normalized).")

    else:
        log("No sheets were loaded. Please verify the Excel path and structure.")

    log("Preprocessing and integration pipeline completed successfully.")

