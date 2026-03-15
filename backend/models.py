from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class MedicationStatus(str, Enum):
    active = "active"
    discontinued = "discontinued"

class DosePeriod(BaseModel):
    start_date: str              # YYYY-MM-DD
    end_date: Optional[str]      # YYYY-MM-DD or null if active
    dose_mg: float
    dose_label: str              # e.g. "50mg"
    frequency: str               # e.g. "Once daily"
    route_label: str             # e.g. "Oral tablet"
    change_reason: Optional[str] # null for first dose entry

class MedicationRecord(BaseModel):
    id: str                      # slug e.g. "med-sertraline"
    name: str
    brand_name: Optional[str]
    drug_class: str              # e.g. SSRI, SNRI, NDRI
    indication: str
    status: MedicationStatus
    doses: List[DosePeriod]

class MedicationTimeline(BaseModel):
    patient_id: str
    diagnoses: List[str]
    medications: List[MedicationRecord]