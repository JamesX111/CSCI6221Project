import os
import math
from typing import List, Tuple, Dict, Any


from backend.db_util import patient_util, bed_util, event_util
from backend.db_model import db


# Import your forecast model
import implementation

# Import OpenAI client only if available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False


class ResourceOptimizer:
    """
    Uses ML model + hospital resources to:
    - Predict patient inflow
    - Allocate beds
    - Create patients
    - Provide AI operational summaries
    """
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.openai_key) if (OPENAI_AVAILABLE and self.openai_key) else None

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
        except:
            # Fallback heuristic
            severity_map = {1: 1, 2: 2, 3: 4, 4: 6, 5: 10}
            return severity_map.get(event["severity"], 2)

    # --------------------------------------------------------
    # RESOURCE LOGIC
    # --------------------------------------------------------
    def allocate_resources(self, n_patients: int) -> List[Tuple[int, int]]:
        """
        Creates new patients + attempts bed allocation.
        Returns list of (patient_id, bed_id or None)
        """
        results = []

        for i in range(n_patients):
            name = f"SimPatient {i+1}"
            patient_data = {
                "name": name,
                "email": f"{name.lower().replace(' ', '')}@simulation.com",
                "phone": "000-000-0000",
                "gender": "Unknown",
                "address": "Simulation Lane",
                "doctor_id": None,
            }
            patient = patient_util.create_patient(patient_data)


            bed_id = bed_util.allocate_available_bed()

            if bed_id is not None:
                bed_util.assign_patient_to_bed(patient["id"], bed_id)
                results.append((patient["id"], bed_id))
            else:
                # They remain unassigned
                results.append((patient["id"], None))

        db.session.commit()
        return results

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
Bed assignment results: {allocations}

Write a professional 4-6 sentence summary explaining:
1. What the event is.
2. How many patients are expected.
3. Whether resources are enough (beds & staff).
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
        admitted = sum(1 for p, b in allocations if b is not None)
        waiting = sum(1 for p, b in allocations if b is None)

        return (
            f"Event '{event['event_type']}' (severity {event['severity']}) detected at {event['location']}. "
            f"Expected {n_patients} incoming patients. "
            f"{admitted} patients were assigned beds and {waiting} are waiting. "
            f"Additional staffing or bed capacity may be required depending on continued event activity."
        )
