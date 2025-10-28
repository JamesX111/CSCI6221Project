# CSCI6221-2025-Fall-Project

# Treasure's Update
## What the implementation.py Script Does

### Load Raw Data
* Reads Hospital Management System.xlsx from the working directory.

### Clean the Dataset
* Removes duplicates, null values, and invalid placeholders (N/A, None, etc.).
* Trims spaces and standardizes column names.

### Normalize & Encode
* Normalizes all numeric columns with StandardScaler.
* Label-encodes categorical fields for model compatibility.

### Extract Time-Series Features
* Derives year, month, day, hour, weekday, and is_weekend flags.
* Normalizes derived time-based columns.

### Feature Engineering
* Computes patients_per_doctor, bed_usage_count, and bed_to_patient_ratio.
* Adds rolling averages and cumulative counts for time-dependent trends.

### Split for Training & Testing
* Automatically separates each sheet into training and test datasets.
* Time-based or random splitting is applied depending on data availability.

### Schema Documentation
- Generates a structured Excel file listing each column, data type, and feature category.

## Outputs
After running the script, the following outputs are generated inside a new /processed/ folder:
### Example
/processed/<sheet>_train.csv which is the Training dataset per sheet
/processed/<sheet>_test.csv	which is the Testing dataset per sheet
/processed/schema_documentation.xlsx which is the Summary of all columns, data types, and feature descriptions 

## James's Update
### lucid chart link
* https://lucid.app/lucidchart/74e089cf-a466-464a-9845-f531cc3830f8/edit?viewport_loc=-130%2C-231%2C2483%2C1299%2C0_0&invitationId=inv_ef64f099-1a18-469d-ad24-fcbe0c239071



## db:
* using postgres: https://www.postgresql.org/download/windows/
* put correct format of name into app.py should work
```
DATABASE_URL=postgresql://username:password@hostname:port/database_name
```