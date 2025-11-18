import os
from typing import List, Tuple, Dict, Any
import sqlite3

# Import your forecast model
import implementation

# Import OpenAI client only if available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False


class ResourceOptimizer:
    """
    Uses ML model + hospital resources to:
    - Predict patient inflow
    - Suggest bed allocations (NO DB writes in simulation)
    - Provide AI operational summaries
    """
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.openai_key) if (OPENAI_AVAILABLE and self.openai_key) else None

        # DB path for read-only queries
        self.DB_PATH = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "hospital_raw.db")
        )

    # --------------------------------------------------------
    # FORECASTING PATIENTS
    # --------------------------------------------------------
    def forecast_patients(self, event: Dict[str, Any]) -> int:
        """
        Uses your real forecasting pipeline from implementation.py
        """
        try:
            return max(1, int(round(
                implementation.predict_admissions_from_event(
                    event_type=event["event_type"],
                    severity=event["severity"]
                )
            )))
        except Exception:
            # Fallback heuristic
            severity_map = {1: 1, 2: 2, 3: 4, 4: 6, 5: 10}
            return severity_map.get(event["severity"], 2)

    # --------------------------------------------------------
    # RESOURCE LOGIC (SIMULATION-ONLY, READ-ONLY)
    # --------------------------------------------------------
    def allocate_resources(self, n_patients: int) -> List[Tuple[int, int]]:
        """
        Suggest bed allocations for n_patients WITHOUT writing to the DB.

        Returns list of (sim_patient_index, bed_id_or_None), where
        sim_patient_index is 1..n_patients (simulated slot, not real DB ID).
        """
        # Read free beds snapshot
        try:
            conn = sqlite3.connect(self.DB_PATH, timeout=5.0)
            cur = conn.cursor()
            cur.execute("""
                SELECT bed_No 
                FROM bed
                WHERE bed_No NOT IN (
                    SELECT bed_No FROM bedrecords WHERE discharge_Date IS NULL
                )
                ORDER BY bed_No
                LIMIT ?
            """, (n_patients,))
            free_beds = [row[0] for row in cur.fetchall()]
            conn.close()
        except Exception as e:
            print("[SIM] Error reading beds for allocation:", e)
            free_beds = []

        allocations: List[Tuple[int, int]] = []

        for i in range(n_patients):
            sim_patient_index = i + 1
            bed_id = free_beds[i] if i < len(free_beds) else None
            allocations.append((sim_patient_index, bed_id))

        return allocations

    # --------------------------------------------------------
    # AI TEXT SUMMARY
    # --------------------------------------------------------
    def ai_summary(self, event: Dict[str, Any], n_patients: int, allocations: List[Tuple[int, int]]) -> str:
        if not self.client:
            return self._fallback_summary(event, n_patients, allocations)

        prompt = f"""
You are a hospital operations AI assistant.

Event detected:
{event}

Predicted incoming patients: {n_patients}
Suggested bed assignment results (simulation only, not yet booked): {allocations}

Write a professional 4-6 sentence summary explaining:
1. What the event is.
2. How many patients are expected.
3. Whether resources appear enough (beds & staff).
4. Any risks or bottlenecks.
5. Recommended actions.
"""

        try:
            out = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a hospital operations AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            return out.choices[0].message.content.strip()
        except Exception:
            return self._fallback_summary(event, n_patients, allocations)

    def _fallback_summary(self, event, n_patients, allocations):
        admitted = sum(1 for _, b in allocations if b is not None)
        waiting = sum(1 for _, b in allocations if b is None)

        return (
            f"Event '{event['event_type']}' (severity {event['severity']}) detected at {event['location']}. "
            f"Expected {n_patients} incoming patients. "
            f"{admitted} patients are projected to have beds and {waiting} may be waiting if no further beds are freed. "
            f"Staff should monitor bed turnover and consider surge strategies if additional incidents occur."
        )
