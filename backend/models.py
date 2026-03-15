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
    frequency: Optional[str] = None
    route_label: Optional[str] = None
    change_reason: Optional[str] = None

class MedicationRecord(BaseModel):
    id: str                      # slug e.g. "med-sertraline"
    name: str
    brand_name: Optional[str] = None
    drug_class: str              # e.g. SSRI, SNRI, NDRI
    indication: Optional[str] = None
    status: MedicationStatus
    doses: List[DosePeriod]

class MedicationTimeline(BaseModel):
    patient_id: str
    diagnoses: List[str]
    medications: List[MedicationRecord]