from pydantic import BaseModel
from typing import Optional

#patient input from form
class PatientIntakeInput(BaseModel):
    first_name: str
    last_name: str
    dob: str
    returning_patient: int
    chest_pain: int
    shortness_of_breath: int
    smoking: int

#doctor inputs after taking vital
class ProviderVitalsInput(BaseModel):
    patient_id: Optional[str] = None
    elevated_troponin: float
    ecg: int
    heart_rate: int #raw heart rate

#data pulled from ehr
class HistoryFHIRInput(BaseModel):
    patient_id: Optional[str] = None
    age: int = 0
    hypertension: int = 0
    diabetes: int = 0
    coronary_artery_disease: int = 0
    myocardial_infarction: int = 0
    heart_disease_history: int = 0
    cardiovascular_disease: int = 0

class RiskInput(BaseModel):
    chest_pain: int
    shortness_of_breath: int
    smoking: int
    age: int
    hypertension: int
    diabetes: int
    heart_disease_history: int
    elevated_troponin: int
    ecg: int
    heart_rate: int

class FinalAssessmentRequest(BaseModel):
    patient_intake: PatientIntakeInput
    provider_triage: ProviderVitalsInput


# class Inputs(BaseModel):
#     # input data provided by patient
#     chest_pain: int
#     shortness_of_breath: int
#     radiating_pain: int

#     # structured data from EHR
#     age: int # Patient
#     elevated_troponin: int # Observation
#     ecg_abnormalities: int
#     hypertension: int # Condition
#     diabetes: int # Condition
#     smoking: int 
#     heart_disease_history: int # Condition
#     high_heart_rate: int # Observation


#     # FHIR data
#     patient_id: Optional[str] = None

# class SymptomInput(BaseModel): #input only
#     chest_pain: int
#     shortness_of_breath: int
#     radiating_pain: int