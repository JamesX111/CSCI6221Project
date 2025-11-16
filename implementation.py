"""
implementation.py
------------------
Phase 2: Predictive Modeling Component

This module performs hospital inflow forecasting using the normalized
`hospital.db` database produced in Phase 1. It retrieves temporal records
from the `appointment` or `bedrecords` tables, constructs a daily time-series
of inflow counts, fits an ARIMA(2,1,2) model, and produces predictions for
the next N days.

An optional OpenAI-based natural-language summary provides operational
interpretation for administrative planning.

Author:  
CSCI 6221 – Hospital Management AI System  
George Washington University
"""

import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import timedelta
from statsmodels.tsa.arima.model import ARIMA

from dotenv import load_dotenv
from openai import OpenAI

# -------------------------------------------------------------
# 1. Configuration
# -------------------------------------------------------------
load_dotenv()

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data/hospital.db")

engine = create_engine(f"sqlite:///{DB_PATH}")

# OpenAI client
env_path = os.path.join(os.path.dirname(__file__), "backend/.env")
load_dotenv(env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -------------------------------------------------------------
# 2. Load a Valid Time-Series Source
# -------------------------------------------------------------
def load_timeseries_source():
    """
    Attempts to load a suitable time-series for forecasting.
    Priority:
        1. appointment.appointment_Date
        2. bedrecords.occupied_from
    """

    # ---- Option 1: Appointment timestamps ----
    query_appt = """
        SELECT 
            appointment_Date AS ts
        FROM appointment
        WHERE appointment_Date IS NOT NULL
    """

    df = pd.read_sql(query_appt, engine)

    if not df.empty:
        df['ts'] = pd.to_datetime(df['ts'])
        df['date'] = df['ts'].dt.date
        df = df[['date']]
        df['source'] = "appointment"
        return df

    # ---- Option 2: Bed Occupancy timestamps ----
    query_beds = """
        SELECT 
            occupied_from AS ts
        FROM bedrecords
        WHERE occupied_from IS NOT NULL
    """

    df = pd.read_sql(query_beds, engine)

    if df.empty:
        print("No time-series source found in hospital.db.")
        return pd.DataFrame()

    df['ts'] = pd.to_datetime(df['ts'])
    df['date'] = df['ts'].dt.date
    df = df[['date']]
    df['source'] = "bedrecords"
    return df

def load_bed_data():
    """
    Loads hospital admissions using real bedrecords schema.
    """
    query = """
        SELECT 
            bed_No AS bed_id,
            admission_Date AS admission_date,
            discharge_Date AS discharge_date
        FROM bedrecords
        WHERE admission_Date IS NOT NULL
          AND discharge_Date IS NOT NULL
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        print("No records found in bedrecords.")
        return df

    df['admission_date'] = pd.to_datetime(df['admission_date'])
    df['discharge_date'] = pd.to_datetime(df['discharge_date'])

    df['duration_hr'] = (df['discharge_date'] - df['admission_date']).dt.total_seconds() / 3600
    df['date'] = df['admission_date'].dt.date

    return df


def compute_daily_inflow(df):
    """
    Computes daily admission counts.
    """
    daily_inflow = (
        df.groupby('date')
          .size()
          .reset_index(name='admissions')
    )

    daily_inflow['date'] = pd.to_datetime(daily_inflow['date'])
    daily_series = daily_inflow.set_index('date').asfreq('D').fillna(0)

    return daily_series



def forecast_inflow(days_ahead=7):
    df = load_bed_data()
    if df.empty:
        return pd.DataFrame()

    inflow_series = compute_daily_inflow(df)['admissions']

    if len(inflow_series) < 5:
        print("Not enough data to run ARIMA.")
        return pd.DataFrame()

    model = ARIMA(inflow_series, order=(2, 1, 2))
    fitted = model.fit()

    forecast = fitted.forecast(steps=days_ahead)

    future_dates = pd.date_range(
        start=inflow_series.index[-1] + pd.Timedelta(days=1),
        periods=days_ahead,
        freq='D'
    )

    return pd.DataFrame({
        "date": future_dates.date,
        "predicted_admissions": np.round(forecast.values, 2)
    })


def generate_ai_summary(forecast_df):
    if forecast_df.empty:
        return "No forecast data available for summary generation."

    avg_inflow = forecast_df['predicted_admissions'].mean()
    peak_day = forecast_df.loc[
        forecast_df['predicted_admissions'].idxmax(),
        'date'
    ]

    prompt = f"""
    Hospital Admission Forecast Summary:

    Forecast Data:
    {forecast_df.to_string(index=False)}

    Average admissions: {avg_inflow:.1f} patients/day
    Peak day: {peak_day}

    Generate a concise operational summary.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return response.choices[0].message.content
    
    except Exception as e:
        print("[AI ERROR]", e)
        return "Error generating summary."



# -------------------------------------------------------------
# 6. Script Execution
# -------------------------------------------------------------
if __name__ == "__main__":
    print("=== Running Forecast ===")
    forecast_df = forecast_inflow(7)
    print(forecast_df)

    print("\n=== AI Summary ===")
    print(generate_ai_summary(forecast_df))
