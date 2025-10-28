import os
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import sqlite3

# ----------------------------------------------------
# 1. Project Paths 
# ----------------------------------------------------

# Base project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data directory
DATA_DIR = os.path.join(BASE_DIR, "data")

# Input raw Excel file
RAW_FILE = os.path.join(DATA_DIR, "Hospital Management System.xlsx")

# Processed output directory
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# Make sure /data/processed exists (auto-create if missing)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# ----------------------------------------------------
# Utility Print 
# ----------------------------------------------------
def log(msg: str):
    print(msg)

# ----------------------------------------------------
# 3. Cleaning + Normalization + Time Features
# ----------------------------------------------------
def clean_normalize_timeseries(file_path):
    if not os.path.exists(file_path):
        log(f"File not found: {file_path}")
        return {}

    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    log(f"Loaded file with sheets: {sheet_names}")

    cleaned_dfs = {}

    for sheet in sheet_names:
        log(f"\n🧹 Processing sheet: {sheet}")
        df = pd.read_excel(xls, sheet_name=sheet)
        df.columns = df.columns.str.strip()

        # --- Basic cleaning ---
        df.drop_duplicates(inplace=True)
        df.replace(['N/A','NA','NaN','null','-','None','nan'], np.nan, inplace=True)
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].astype(str).str.strip()

        # --- Detect and convert datetime columns ---
        datetime_cols = []
        for col in df.columns:
            if any(x in col.lower() for x in ["date", "time", "timestamp"]):
                df[col] = pd.to_datetime(df[col], errors="coerce")
                datetime_cols.append(col)
        if datetime_cols:
            log(f"   Detected datetime columns: {datetime_cols}")

        # --- Convert numeric-like strings ---
        for col in df.columns:
            if df[col].dtype == object:
                try:
                    df[col] = pd.to_numeric(df[col])
                except Exception:
                    pass

        # --- Handle missing values ---
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col].fillna(df[col].mean(), inplace=True)
        for col in df.select_dtypes(exclude=[np.number]).columns:
            df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown", inplace=True)

        # --- Normalize numeric columns ---
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            scaler = StandardScaler()
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
            log(f"   ➤ Normalized numeric columns: {numeric_cols}")

        # --- Encode categorical columns ---
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            log(f"   ➤ Encoded categorical column: {col}")

        # --- Extract time-series features ---
        for col in datetime_cols:
            if df[col].notnull().any():
                df[f"{col}_year"] = df[col].dt.year
                df[f"{col}_month"] = df[col].dt.month
                df[f"{col}_day"] = df[col].dt.day
                df[f"{col}_hour"] = df[col].dt.hour
                df[f"{col}_weekday"] = df[col].dt.weekday
                df[f"{col}_is_weekend"] = (df[col].dt.weekday >= 5).astype(int)
                log(f"   Extracted features from {col}")

        # --- Normalize derived time features ---
        time_features = [c for c in df.columns if any(x in c for x in ["_month", "_day", "_hour", "_weekday"])]
        if time_features:
            scaler = StandardScaler()
            df[time_features] = scaler.fit_transform(df[time_features])
            log(f"   ➤ Normalized time-based features: {time_features}")

        cleaned_dfs[sheet] = df
        log(f"   Finished sheet '{sheet}' ({len(df)} rows)")

    log(f"\ncompleted successfully.")
    return cleaned_dfs

# ----------------------------------------------------
# 4. Phase 1c + 1d – Feature Engineering + Split + Schema
# ----------------------------------------------------
def feature_engineer_and_split(cleaned_dfs):
    log("\nStarting Phase 1c: Feature Engineering + Phase 1d: Splitting + Schema")

    processed_dir = PROCESSED_DIR
    os.makedirs(processed_dir, exist_ok=True)
    schema_records = []

    for sheet_name, df in cleaned_dfs.items():
        log(f"\nEngineering features for sheet: {sheet_name}")

        # Derived aggregate features
        if "patient_id" in df.columns and "doctor_id" in df.columns:
            agg = df.groupby("doctor_id")["patient_id"].count().reset_index(name="patients_per_doctor")
            df = df.merge(agg, on="doctor_id", how="left")
            log("   ➤ Added patients_per_doctor")

        if "bed_id" in df.columns and "patient_id" in df.columns:
            bed_util = df.groupby("bed_id")["patient_id"].count().reset_index(name="bed_usage_count")
            df = df.merge(bed_util, on="bed_id", how="left")
            log("   ➤ Added bed_usage_count")

        # Ratios & interaction terms
        if {"patients_per_doctor", "bed_usage_count"}.issubset(df.columns):
            df["bed_to_patient_ratio"] = df["bed_usage_count"] / (df["patients_per_doctor"] + 1)
            log("   ➤ Added bed_to_patient_ratio")

        # Rolling / lag features
        date_cols = [c for c in df.columns if "date" in c.lower() or "time" in c.lower()]
        if date_cols:
            df.sort_values(date_cols[0], inplace=True)
            df["record_count_cum"] = range(1, len(df) + 1)
            df["record_count_rolling7"] = df["record_count_cum"].rolling(window=7, min_periods=1).mean()
            log(f"   Added rolling count features using {date_cols[0]}")

        # Dataset splitting
        split_file_prefix = f"{sheet_name.lower().replace(' ', '_')}"
        if date_cols:
            cutoff = int(0.8 * len(df))
            train_df = df.iloc[:cutoff]
            test_df = df.iloc[cutoff:]
            log(f"   Time-based split: {len(train_df)} train / {len(test_df)} test")
        else:
            train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
            log(f"   Random split: {len(train_df)} train / {len(test_df)} test")

        train_df.to_csv(os.path.join(processed_dir, f"{split_file_prefix}_train.csv"), index=False)
        test_df.to_csv(os.path.join(processed_dir, f"{split_file_prefix}_test.csv"), index=False)

        # Schema documentation
        for col in df.columns:
            schema_records.append({
                "Sheet": sheet_name,
                "Column": col,
                "DataType": str(df[col].dtype),
                "Description": (
                    "Date/Time Feature" if "date" in col.lower() or "time" in col.lower()
                    else "Numeric Feature" if np.issubdtype(df[col].dtype, np.number)
                    else "Categorical/Encoded Feature"
                )
            })

    schema_df = pd.DataFrame(schema_records)
    schema_path = os.path.join(processed_dir, "schema_documentation.xlsx")
    schema_df.to_excel(schema_path, index=False)

    log(f"\nPhase 1c & 1d complete.")
    log(f"Outputs saved to: {processed_dir}")
    return schema_df

# ----------------------------------------------------
# 5. Database Integration 
# ----------------------------------------------------
def export_to_database(cleaned_dfs, db_type="sqlite", db_name="hospital.db",
                       host="localhost", user="root", password=""):
    """
    Exports cleaned & processed DataFrames into Person B's database.
    Works with SQLite (default) or MySQL.
    """

    conn = None

    try:
        # ---------- SQLite ----------
        if db_type.lower() == "sqlite":
            conn = sqlite3.connect(db_name)
            log(f" Connected to SQLite database: {db_name}")

        # ---------- MySQL ----------
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

        # ---------- Export Each DataFrame ----------
        for sheet_name, df in cleaned_dfs.items():
            table_name = sheet_name.lower().replace(" ", "_")
            log(f"Exporting {len(df)} rows → table '{table_name}'")

            if db_type.lower() == "sqlite":
                df.to_sql(table_name, conn, if_exists="replace", index=False)
            else:
                from sqlalchemy import create_engine
                engine = create_engine(
                    f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}"
                )
                df.to_sql(table_name, con=engine, if_exists="replace", index=False)

        if conn:
            conn.commit()
        log("All data exported successfully.\n")

    except Exception as e:
        log(f"Error during database export: {e}")

    finally:
        if conn:
            conn.close()
            log("Database connection closed.")

# ----------------------------------------------------
# 6. Entry point
# ----------------------------------------------------
if __name__ == "__main__":
    log("Starting Person A pipeline (Phases 1b → 1d + Integration)")
    cleaned_dfs = clean_normalize_timeseries(RAW_FILE)

    if cleaned_dfs:
        feature_engineer_and_split(cleaned_dfs)

        # ---- Integration Step ----
        # Option 1: SQLite (default)
        export_to_database(cleaned_dfs, db_type="sqlite", db_name="hospital.db")

        # Option 2: MySQL
        # export_to_database(
        #     cleaned_dfs,
        #     db_type="mysql",
        #     db_name="hospital",
        #     host="localhost",
        #     user="root",
        #     password="your_password"
        # )

    log(" All preprocessing and integration phases completed successfully.")
