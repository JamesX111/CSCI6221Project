"""
Hospital Management System

What this script does
---------------------
extend data to create a large dataset
"""

import pandas as pd
import numpy as np

# ---------------- Configuration ----------------
SEED = 1007                              
SRC = "kaggle Hospital Management System.xlsx"  
OUT = "Hospital Management System.xlsx"
REPORT = "data_consistency_report.xlsx"

np.random.seed(SEED)

# ---------------- Helper functions ----------------
def max_id(df, col):
    """Return numeric max of a PK-like column, or 0 if not found/empty."""
    try:
        return int(pd.to_numeric(df[col], errors="coerce").max())
    except Exception:
        return 0

def rand_datetimes(n, start="2018-01-01", end="2025-10-06"):
    """
    Generate n random timestamps between start and end (inclusive) as a Pandas Series.
    We return a Series so callers can safely use `.dt` accessors.
    """
    start64 = np.datetime64(start, "s")
    end64 = np.datetime64(end, "s")
    span = (end64 - start64).astype("timedelta64[s]").astype(int)
    offs = np.random.randint(0, span, n).astype("timedelta64[s]")
    return pd.Series(pd.to_datetime(start64 + offs))

def to_date(series):
    """Coerce to date (YYYY-mm-dd), avoiding Excel ##### by using writer column width later."""
    return pd.to_datetime(series, errors="coerce").dt.date

def to_time(series):
    """Coerce to time (HH:MM:SS)."""
    return pd.to_datetime(series, errors="coerce").dt.time

def pk_phone(n):
    """Generate Pakistan mobile numbers like +92 3XXXXXXXXX."""
    ops = np.random.randint(10, 100, size=n)
    tails = np.random.randint(0, 10**7, size=n)
    return np.array([f"+92 3{op:02d}{tail:07d}" for op, tail in zip(ops, tails)])

def normalize_gender(series):
    """Normalize gender to {M, F} (first letter, uppercased)."""
    s = series.astype(str).str.strip().str[0].str.upper()
    return s.where(s.isin(["M", "F"]), pd.NA)

def align(df, cols):
    """
    Ensure all columns in `cols` exist in df (in that order). Fill missing with NA.
    This preserves the original schema (including typos) exactly.
    """
    for c in cols:
        if c not in df.columns:
            df[c] = pd.NA
    return df[cols]

# ---------------- Load original workbook + schema ----------------
xls = pd.ExcelFile(SRC)
schema = {name: pd.read_excel(SRC, sheet_name=name, nrows=0).columns.tolist()
          for name in xls.sheet_names}
dfs = {name: pd.read_excel(SRC, sheet_name=name) for name in xls.sheet_names}

# ---------------- Realistic targets ----------------
targets = {
    "Patients": 50_000,     # foundation of dataset
    "Doctor": 1_500,        # moderate, plausible for large system
    "Nurse": 2_000,         # increased to reflect patient:nurse ratio
    "Helpers": 2_000,       # support staff
    "Appointment": 40_000,  # moderate-heavy usage
    "MedicalRecord": 60_000,# heavy (time-series)
    "BedRecords": 30_000,   # heavy occupancy events
    "RoomRecords": 30_000,  # heavy admissions to rooms
    "SurgeryRecord": 20_000,# moderate
    "StaffShift": 25_000,   # moderate
    "Room": 1_200,          # facility capacity (not huge)
    "Bed": 1_000,           # physical beds capped to realistic level
}

# ---------------- Lookups ----------------
dept_ids = dfs.get("Department", pd.DataFrame()).get("dept_Id", pd.Series([], dtype="int64")).dropna().unique()
ward_nos = dfs.get("Ward", pd.DataFrame()).get("ward_No", pd.Series([], dtype="int64")).dropna().unique()

# ---------------- Patients ----------------
if "Patients" in dfs:
    p = dfs["Patients"].copy()

    # Fix formats
    if "Gender" in p.columns:
        p["Gender"] = normalize_gender(p["Gender"])
    if "contact_No" in p.columns:
        mask = p["contact_No"].isna() | ~p["contact_No"].astype(str).str.match(r"^\+92 3\d{9}$")
        p.loc[mask, "contact_No"] = pk_phone(mask.sum())
    if "Date_Of_Birth" in p.columns:
        p["Date_Of_Birth"] = to_date(p["Date_Of_Birth"])
    if "pt_Address" in p.columns:
        mask = ~p["pt_Address"].astype(str).str.endswith(", Punjab, Pakistan", na=False)
        p.loc[mask, "pt_Address"] = p.loc[mask, "pt_Address"].astype(str).str.rstrip(", ") + ", Punjab, Pakistan"

    # Expand
    need = max(targets["Patients"] - len(p), 0)
    if need > 0 and "patient_Id" in p.columns:
        start = max_id(p, "patient_Id") + 1
        add = {"patient_Id": np.arange(start, start + need)}
        add["FName"] = np.random.choice(["Ayesha", "Bilal", "Zain", "Hira", "Usman", "Sara", "Hamza", "Amna", "Daniyal", "Maryam"], need)
        add["LName"] = np.random.choice(["Khan", "Malik", "Ahmad", "Hussain", "Sheikh", "Raza", "Siddiqui", "Farooq"], need)
        add["Gender"] = np.random.choice(["M", "F"], need)
        dob = pd.to_datetime(np.datetime64("1930-01-01")) + pd.to_timedelta(np.random.randint(0, 365 * 90, size=need), unit="D")
        add["Date_Of_Birth"] = pd.Series(dob).dt.date
        streets = ["Main St", "Oak Ave", "Pine Rd", "Maple Blvd", "Cedar Ln", "Elm St"]
        cities = ["Lahore", "Faisalabad", "Multan", "Rawalpindi", "Sialkot"]
        add["pt_Address"] = [f"{np.random.randint(1,9999)} {np.random.choice(streets)}, {np.random.choice(cities)}, Punjab, Pakistan" for _ in range(need)]
        add["contact_No"] = pk_phone(need)
        p = pd.concat([p, align(pd.DataFrame(add), schema["Patients"])], ignore_index=True)

    dfs["Patients"] = align(p, schema["Patients"])

# ---------------- Doctor ----------------
if "Doctor" in dfs:
    d = dfs["Doctor"].copy()

    # Fix formats
    if "Gender" in d.columns:
        d["Gender"] = normalize_gender(d["Gender"])
    if "contact_No" in d.columns:
        mask = d["contact_No"].isna() | ~d["contact_No"].astype(str).str.match(r"^\+92 3\d{9}$")
        d.loc[mask, "contact_No"] = pk_phone(mask.sum())
    if "surgeon_Type" in d.columns:
        d["surgeon_Type"] = d["surgeon_Type"].fillna("General")
    if "office_No" in d.columns:
        # Uppercase and strip any trailing text (like 'off')
        d["office_No"] = d["office_No"].astype(str).str.upper().str.extract(r"(OFF-\d{3,4})")[0]
        seq = np.arange(1, len(d) + 1)
        # Fill missing or invalid with sequential codes
        d.loc[d["office_No"].isna(), "office_No"] = [f"OFF-{i:04d}" for i in seq]

    # Expand (moderate)
    need = max(targets["Doctor"] - len(d), 0)
    if need > 0 and "doct_Id" in d.columns:
        start = max_id(d, "doct_Id") + 1
        add = {"doct_Id": np.arange(start, start + need)}
        add["dept_Id"] = np.random.choice(dept_ids, need) if len(dept_ids) else np.random.randint(1, 20, need)
        add["FName"] = np.random.choice(["Ayesha", "Bilal", "Zain", "Hira", "Usman", "Sara", "Hamza", "Amna"], need)
        add["LName"] = np.random.choice(["Khan", "Malik", "Ahmad", "Hussain", "Sheikh", "Raza"], need)
        add["Gender"] = np.random.choice(["M", "F"], need)
        add["contact_No"] = pk_phone(need)
        add["surgeon_Type"] = np.random.choice(["General", "Orthopedic", "Cardiac", "Neuro", "ENT", "Dental", "Pediatric"], need)
        add["office_No"] = [f"OFF-{np.random.randint(1, 999):03d}" for _ in range(need)]
        d = pd.concat([d, align(pd.DataFrame(add), schema["Doctor"])], ignore_index=True)

    dfs["Doctor"] = align(d, schema["Doctor"])

# ---------------- Nurse (preserve typo 'conatct_No') ----------------
if "Nurse" in dfs:
    n = dfs["Nurse"].copy()

    # Fix formats
    if "Gender" in n.columns:
        n["Gender"] = normalize_gender(n["Gender"])
    if "conatct_No" in n.columns:
        mask = n["conatct_No"].isna() | ~n["conatct_No"].astype(str).str.match(r"^\+92 3\d{9}$")
        n.loc[mask, "conatct_No"] = pk_phone(mask.sum())

    # Expand (to ~2000)
    need = max(targets["Nurse"] - len(n), 0)
    if need > 0 and "nurse_Id" in n.columns:
        start = max_id(n, "nurse_Id") + 1
        add = {"nurse_Id": np.arange(start, start + need)}
        add["dept_Id"] = np.random.choice(dept_ids, need) if len(dept_ids) else np.random.randint(1, 20, need)
        add["FName"] = np.random.choice(["Nadia", "Huma", "Mariam", "Fatima", "Noor", "Asma", "Kiran"], need)
        add["LName"] = np.random.choice(["Ali", "Khan", "Riaz", "Shah"], need)
        add["Gender"] = np.random.choice(["M", "F"], need)
        add["conatct_No"] = pk_phone(need)
        n = pd.concat([n, align(pd.DataFrame(add), schema["Nurse"])], ignore_index=True)

    dfs["Nurse"] = align(n, schema["Nurse"])

# ---------------- Helpers ----------------
if "Helpers" in dfs:
    h = dfs["Helpers"].copy()

    # Fix formats
    if "Gender" in h.columns:
        h["Gender"] = normalize_gender(h["Gender"])
    if "contact_No" in h.columns:
        mask = h["contact_No"].isna() | ~h["contact_No"].astype(str).str.match(r"^\+92 3\d{9}$")
        h.loc[mask, "contact_No"] = pk_phone(mask.sum())

    # Expand (to ~2000)
    need = max(targets["Helpers"] - len(h), 0)
    if need > 0 and "helper_Id" in h.columns:
        start = max_id(h, "helper_Id") + 1
        add = {"helper_Id": np.arange(start, start + need)}
        add["dept_Id"] = np.random.choice(dept_ids, need) if len(dept_ids) else np.random.randint(1, 20, need)
        add["FName"] = np.random.choice(["Arif", "Noman", "Imran", "Asif", "Danish", "Tahir", "Adnan"], need)
        add["LName"] = np.random.choice(["Ali", "Khan", "Riaz", "Shah", "Yousaf", "Tariq"], need)
        add["Gender"] = np.random.choice(["M", "F"], need)
        add["contact_No"] = pk_phone(need)
        h = pd.concat([h, align(pd.DataFrame(add), schema["Helpers"])], ignore_index=True)

    dfs["Helpers"] = align(h, schema["Helpers"])

# ---------------- Infrastructure: Room (cap ~1200) ----------------
if "Room" in dfs and "room_No" in dfs["Room"].columns:
    r = dfs["Room"].copy()
    need = max(targets["Room"] - len(r), 0)
    if need > 0:
        start = int(pd.to_numeric(r["room_No"], errors="coerce").max()) + 1 if len(r) else 1
        add = {"room_No": np.arange(start, start + need)}
        if "dept_Id" in r.columns:
            add["dept_Id"] = np.random.choice(dept_ids, need) if len(dept_ids) else np.random.randint(1, 20, need)
        if "room_Type" in r.columns:
            add["room_Type"] = np.random.choice(["General", "ICU", "Private", "Semi-Private", "Pediatric", "Surgical"], need)
        r = pd.concat([r, align(pd.DataFrame(add), schema["Room"])], ignore_index=True)
    dfs["Room"] = align(r, schema["Room"])

# ---------------- Infrastructure: Bed (cap ~3000) ----------------
if "Bed" in dfs and "bed_No" in dfs["Bed"].columns:
    b = dfs["Bed"].copy()
    need = max(targets["Bed"] - len(b), 0)
    if need > 0:
        start = int(pd.to_numeric(b["bed_No"], errors="coerce").max()) + 1 if len(b) else 1
        add = {"bed_No": np.arange(start, start + need)}
        if "ward_No" in b.columns:
            add["ward_No"] = np.random.choice(
                dfs["Ward"]["ward_No"] if "Ward" in dfs else np.arange(1, 50), need
            )
        b = pd.concat([b, align(pd.DataFrame(add), schema["Bed"])], ignore_index=True)
    dfs["Bed"] = align(b, schema["Bed"])

# ---------------- Appointment ----------------
if "Appointment" in dfs:
    a = dfs["Appointment"].copy()
    need = max(targets["Appointment"] - len(a), 0)
    if need > 0 and {"appoIntment_Id", "patient_Id", "doct_Id"}.issubset(a.columns):
        start = max_id(a, "appoIntment_Id") + 1
        appt_dates = rand_datetimes(need).dt.date
        add = pd.DataFrame({
            "appoIntment_Id": np.arange(start, start + need),
            "patient_Id": np.random.choice(dfs["Patients"]["patient_Id"].dropna().unique(), need),
            "doct_Id": np.random.choice(dfs["Doctor"]["doct_Id"].dropna().unique(), need),
            "reason": np.random.choice(
                ["Flu", "Fracture", "Hypertension", "Diabetes", "Asthma", "Infection", "Allergy", "Headache", "Back Pain", "Covid-19"], need
            ),
            "appointment_Date": appt_dates,
            "payment_amount": np.random.randint(500, 15000, size=need),
            "mode_of_payment": np.random.choice(["Cash", "Card", "Insurance", "Online"], need),
            "mode_of_appointment": np.random.choice(["In-Person", "Telehealth"], need),
            "appointment_status": np.random.choice(["Booked", "Completed", "Cancelled", "No-Show"], need, p=[0.2, 0.6, 0.1, 0.1]),
        })
        a = pd.concat([a, align(add, schema["Appointment"])], ignore_index=True)

    if "appointment_Date" in a.columns:
        a["appointment_Date"] = to_date(a["appointment_Date"])
    if "payment_amount" in a.columns:
        a["payment_amount"] = pd.to_numeric(a["payment_amount"], errors="coerce").fillna(0).round(0).astype(int)

    dfs["Appointment"] = align(a, schema["Appointment"])

# ---------------- MedicalRecord ----------------
if "MedicalRecord" in dfs:
    mr = dfs["MedicalRecord"].copy()
    need = max(targets["MedicalRecord"] - len(mr), 0)
    if need > 0 and "record_Id" in mr.columns:
        start = max_id(mr, "record_Id") + 1
        visit = rand_datetimes(need).dt.date
        nextv = (pd.to_datetime(visit) + pd.to_timedelta(np.random.randint(7, 120, size=need), unit="D")).dt.date
        add = {
            "record_Id": np.arange(start, start + need),
            "doct_Id": np.random.choice(dfs["Doctor"]["doct_Id"].dropna().unique(), need),
            "patient_Id": np.random.choice(dfs["Patients"]["patient_Id"].dropna().unique(), need),
            "visit_Date": visit,
            "curr_Weight": np.random.randint(40, 120, size=need),
            "curr_height": np.random.randint(140, 200, size=need),
            "curr_Blood_Pressure": [f"{np.random.randint(100,150)}/{np.random.randint(60,95)}" for _ in range(need)],
            "curr_Temp_F": np.random.randint(97, 103, size=need),
            "diagnosis": np.random.choice(
                ["Flu", "Fracture", "Hypertension", "Diabetes", "Asthma", "Infection", "Allergy", "Headache", "Back Pain", "Covid-19"], need
            ),
            "treatment": np.random.choice(
                ["Medication", "Surgery", "Therapy", "Observation", "Vaccination", "IV Fluids", "Cast", "Rest", "Physical Therapy", "Consultation"], need
            ),
            "next_Visit": nextv,
        }
        mr = pd.concat([mr, align(pd.DataFrame(add), schema["MedicalRecord"])], ignore_index=True)

    for c in ["visit_Date", "next_Visit"]:
        if c in mr.columns:
            mr[c] = to_date(mr[c])

    dfs["MedicalRecord"] = align(mr, schema["MedicalRecord"])

# ---------------- BedRecords ----------------
if "BedRecords" in dfs:
    br = dfs["BedRecords"].copy()
    need = max(targets["BedRecords"] - len(br), 0)
    if need > 0 and "admission_Id" in br.columns:
        start = max_id(br, "admission_Id") + 1
        ad = rand_datetimes(need).dt.date
        stay = np.random.randint(1, 15, size=need)
        dis = (pd.to_datetime(ad) + pd.to_timedelta(stay, unit="D")).dt.date
        add = {
            "admission_Id": np.arange(start, start + need),
            "bed_No": np.random.choice(dfs["Bed"]["bed_No"].dropna().unique(), need) if "Bed" in dfs else np.random.randint(1, 3000, size=need),
            "patient_Id": np.random.choice(dfs["Patients"]["patient_Id"].dropna().unique(), need),
            "nurse_Id": np.random.choice(dfs["Nurse"]["nurse_Id"].dropna().unique(), need),
            "helper_Id": np.random.choice(dfs["Helpers"]["helper_Id"].dropna().unique(), need),
            "admission_Date": ad,
            "discharge_Date": dis,
            "amount": np.random.randint(1000, 50000, size=need),
            "mode_of_payment": np.random.choice(["Cash", "Card", "Insurance", "Online"], need),
        }
        br = pd.concat([br, align(pd.DataFrame(add), schema["BedRecords"])], ignore_index=True)

    for c in ["admission_Date", "discharge_Date"]:
        if c in br.columns:
            br[c] = to_date(br[c])
    if "amount" in br.columns:
        br["amount"] = pd.to_numeric(br["amount"], errors="coerce").fillna(0).round(0).astype(int)

    dfs["BedRecords"] = align(br, schema["BedRecords"])

# ---------------- RoomRecords (preserve 'admisson_ID' typo) ----------------
if "RoomRecords" in dfs:
    rr = dfs["RoomRecords"].copy()
    id_col = "admisson_ID" if "admisson_ID" in rr.columns else "admission_ID"
    need = max(targets["RoomRecords"] - len(rr), 0)
    if need > 0 and id_col in rr.columns:
        start = max_id(rr, id_col) + 1
        ad = rand_datetimes(need).dt.date
        stay = np.random.randint(1, 10, size=need)
        dis = (pd.to_datetime(ad) + pd.to_timedelta(stay, unit="D")).dt.date
        add = {
            id_col: np.arange(start, start + need),
            "room_no": np.random.choice(dfs["Room"]["room_No"].dropna().unique(), need) if "Room" in dfs else np.random.randint(1, 1000, size=need),
            "patient_Id": np.random.choice(dfs["Patients"]["patient_Id"].dropna().unique(), need),
            "nurse_Id": np.random.choice(dfs["Nurse"]["nurse_Id"].dropna().unique(), need),
            "helper_Id": np.random.choice(dfs["Helpers"]["helper_Id"].dropna().unique(), need),
            "admission_Date": ad,
            "discharge_Date": dis,
            "amount": np.random.randint(1000, 60000, size=need),
            "mode_of_payment": np.random.choice(["Cash", "Card", "Insurance", "Online"], need),
        }
        rr = pd.concat([rr, align(pd.DataFrame(add), schema["RoomRecords"])], ignore_index=True)

    for c in ["admission_Date", "discharge_Date"]:
        if c in rr.columns:
            rr[c] = to_date(rr[c])
    if "amount" in rr.columns:
        rr["amount"] = pd.to_numeric(rr["amount"], errors="coerce").fillna(0).round(0).astype(int)

    dfs["RoomRecords"] = align(rr, schema["RoomRecords"])

# ---------------- SurgeryRecord ----------------
if "SurgeryRecord" in dfs:
    sr = dfs["SurgeryRecord"].copy()
    need = max(targets["SurgeryRecord"] - len(sr), 0)
    if need > 0 and "surgery_Id" in sr.columns:
        start = max_id(sr, "surgery_Id") + 1
        s_dates = rand_datetimes(need)
        start_hours = np.random.randint(6, 18, size=need)
        dur = np.random.randint(1, 6, size=need)  
        start_dt = s_dates + pd.to_timedelta(start_hours, unit="h")
        end_dt = start_dt + pd.to_timedelta(dur, unit="h")

        realistic_notes = [
            "Successful", "Patient stable", "Minor complications",
            "Observation needed", "Follow-up scheduled",
            "Patient recovering well", "Under observation", "Stable condition"
        ]

        add = pd.DataFrame({
            "surgery_Id": np.arange(start, start + need),
            "patient_Id": np.random.choice(dfs["Patients"]["patient_Id"].dropna().unique(), need),
            "surgeon_Id": np.random.choice(dfs["Doctor"]["doct_Id"].dropna().unique(), need),
            "surgery_Type": np.random.choice(
                ["Appendectomy", "Cholecystectomy", "Hernia Repair", "Knee Replacement", "CABG", "Cataract", "C-Section"], size=need
            ),
            "surgery_Date": s_dates.dt.date,
            "start_Time": pd.Series(start_dt).dt.time,
            "end_Time": pd.Series(end_dt).dt.time,
            "room_no": np.random.choice(dfs["Room"]["room_No"].dropna().unique(), need) if "Room" in dfs else np.random.randint(1, 1000, size=need),
            "notes": np.random.choice(realistic_notes, size=need),
            "nurse_Id": np.random.choice(dfs["Nurse"]["nurse_Id"].dropna().unique(), need),
            "helper_Id": np.random.choice(dfs["Helpers"]["helper_Id"].dropna().unique(), need),
        })
        sr = pd.concat([sr, align(add, schema["SurgeryRecord"])], ignore_index=True)

    if "surgery_Date" in sr.columns:
        sr["surgery_Date"] = to_date(sr["surgery_Date"])

    dfs["SurgeryRecord"] = align(sr, schema["SurgeryRecord"])

# ---------------- StaffShift ----------------
if "StaffShift" in dfs:
    ss = dfs["StaffShift"].copy()
    need = max(targets["StaffShift"] - len(ss), 0)
    if need > 0 and "shift_Id" in ss.columns:
        start = max_id(ss, "shift_Id") + 1
        dates = rand_datetimes(need)
        start_hours = np.random.choice([7, 8, 9, 15, 16, 17, 19], size=need)
        durations = np.random.choice([8, 10, 12], size=need, p=[0.5, 0.3, 0.2])
        start_dt = dates + pd.to_timedelta(start_hours, unit="h")
        end_dt = start_dt + pd.to_timedelta(durations, unit="h")
        add = pd.DataFrame({
            "shift_Id": np.arange(start, start + need),
            "doct_Id": np.random.choice(dfs["Doctor"]["doct_Id"].dropna().unique(), need),
            "nurse_Id": np.random.choice(dfs["Nurse"]["nurse_Id"].dropna().unique(), need),
            "helper_Id": np.random.choice(dfs["Helpers"]["helper_Id"].dropna().unique(), need),
            "shift_Date": dates.dt.date,
            "shift_Start": pd.Series(start_dt).dt.time,
            "shift_End": pd.Series(end_dt).dt.time,
        })
        ss = pd.concat([ss, align(add, schema["StaffShift"])], ignore_index=True)

    if "shift_Date" in ss.columns:
        ss["shift_Date"] = to_date(ss["shift_Date"])

    dfs["StaffShift"] = align(ss, schema["StaffShift"])

# ---------------- Write final workbook ----------------
with pd.ExcelWriter(OUT, engine="xlsxwriter", datetime_format="yyyy-mm-dd", date_format="yyyy-mm-dd") as w:
    for name in xls.sheet_names:
        df = align(dfs[name], schema[name])
        df.to_excel(w, sheet_name=name[:31], index=False)
        ws = w.sheets[name[:31]]
        # Adjust row/column sizes so dates/phones don't display as #### in Excel
        ws.set_default_row(15)
        ws.set_column(0, len(df.columns) - 1, 17)
        for i, c in enumerate(df.columns):
            lc = c.lower()
            if "date" in lc or "time" in lc:
                ws.set_column(i, i, 20)
            if "contact" in lc or "phone" in lc or "email" in lc:
                ws.set_column(i, i, 26)

# ---------------- Data Consistency Report (QA) ----------------
rows = []
def add_check(sheet, check, result):
    rows.append({"Sheet": sheet, "Check": check, "Result": result})

# 1) Row counts per sheet
for name in xls.sheet_names:
    add_check(name, "Rows", len(dfs[name]))

# 2) Gender validity where present
if "Patients" in dfs and "Gender" in dfs["Patients"].columns:
    pct = (dfs["Patients"]["Gender"].isin(["M", "F"])).mean() * 100
    add_check("Patients", "Gender {M,F}", f"{pct:.2f}% valid")
if "Nurse" in dfs and "Gender" in dfs["Nurse"].columns:
    pct = (dfs["Nurse"]["Gender"].isin(["M", "F"])).mean() * 100
    add_check("Nurse", "Gender {M,F}", f"{pct:.2f}% valid")
if "Doctor" in dfs and "Gender" in dfs["Doctor"].columns:
    pct = (dfs["Doctor"]["Gender"].isin(["M", "F"])).mean() * 100
    add_check("Doctor", "Gender {M,F}", f"{pct:.2f}% valid")

# 3) Phone format checks (use +92 3XXXXXXXXX)
def pct_match(df, col):
    return df[col].astype(str).str.match(r"^\+92 3\d{9}$").mean() * 100 if col in df.columns else 0.0

if "Patients" in dfs:
    add_check("Patients", "Phone +92 3XXXXXXXXX", f"{pct_match(dfs['Patients'], 'contact_No'):.2f}% valid")
if "Nurse" in dfs:
    add_check("Nurse", "Phone +92 3XXXXXXXXX", f"{pct_match(dfs['Nurse'], 'conatct_No'):.2f}% valid")
if "Doctor" in dfs:
    add_check("Doctor", "Phone +92 3XXXXXXXXX", f"{pct_match(dfs['Doctor'], 'contact_No'):.2f}% valid")
if "Helpers" in dfs:
    add_check("Helpers", "Phone +92 3XXXXXXXXX", f"{pct_match(dfs['Helpers'], 'contact_No'):.2f}% valid")

pd.DataFrame(rows).to_excel(REPORT, index=False)

# ---------------- Post-run summary (quick validation) ----------------
print("\n=== Build Summary (v3.3, seed=1007) ===")
for name in xls.sheet_names:
    print(f"{name:15s} : {len(dfs[name]):,} rows")
print(f"\nWrote: {OUT}")
print(f"QA  : {REPORT}")
