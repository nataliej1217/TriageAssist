# def get_patient_data_from_fhir(patient_id: str):
#     # Placeholder function to simulate fetching patient data from FHIR server
#     return {
#         "age": 65,
#         "elevated_troponin": 1,
#         "ecg_abnormalities": 1,
#         "hypertension": 1,
#         "diabetes": 0,
#         "smoking": 1,
#         "heart_disease_history": 1,
#         "high_heart_rate": 1
#     }

import os
import requests
from datetime import date

FHIR_BASE_URL = os.getenv("FHIR_BASE_URL", "https://r4.smarthealthit.org/") #DOUBLE CHECK THIS URL 

def fhir_get(path:str, params:dict | None = None):
    url = f"{FHIR_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

    # try:
    #     response = requests.get(url, params=params)
    #     response.raise_for_status()
    #     return response.json()
    # except requests.RequestException as e:
    #     print(f"Error fetching data from FHIR server: {e}")
    #     return None

def get_metadata():
    return fhir_get("metadata")

def search_patients(name: str | None = None, count: int = 5):
    params = {"_count": count}
    if name:
        params["name"] = name
    return fhir_get("Patient", params=params)

def get_patient_data(patient_id: str):
    return fhir_get(f"Patient/{patient_id}")

def get_observations(patient_id: str, count: int = 50):
    return fhir_get("Observation", params={"patient": patient_id, "_count": count})

def get_conditions(patient_id: str, count: int = 50):
    return fhir_get("Condition", params={"patient": patient_id, "_count": count})

def calculate_age(dob: str | None) -> int: #iN FEATURE BUILDER ALREADY
    if not dob:
        return 0
    try:
        year, month, day = map(int, dob.split("-"))
        born = date(year, month, day)
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    except Exception:
        return 0


#use to extract condition
def get_code_text(resource: dict) -> str:
    code = resource.get("code", {})

    text = code.get("text")
    if text:
        return str(text).lower()

    for coding in code.get("coding", []):
        display = coding.get("display")
        if display:
            return str(display).lower()

    return ""

def has_condition(conditions_bundle: dict, keywords: list[str]) -> int:
    for entry in conditions_bundle.get("entry", []):
        resource = entry.get("resource", {})
        code_text = get_code_text(resource)
        if any(keyword in code_text for keyword in keywords):
            return 1
    return 0

def build_ehr_features(patient: dict, observations: dict, conditions: dict) -> dict:
    return {
        "age": calculate_age(patient.get("birthDate")),
        "hypertension": has_condition(conditions, ["hypertension"]),
        "diabetes": has_condition(conditions, ["diabetes"]),
        "coronary_artery_disease": has_condition(conditions, ["coronary artery disease", "cad"]),
        "myocardial_infarction": has_condition(conditions, ["myocardial infarction", "mi"]),
        "heart_disease_history": has_condition(conditions, ["heart disease"]),
        "cardiovascular_disease": has_condition(conditions, ["cardiovascular disease"])
    }