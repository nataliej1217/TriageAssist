from schemas import RiskInput
from datetime import date

def calculate_age(dob: str) -> int:
    if not dob:
        return 0  #default to 0 if missing
    year, month, day = map(int, dob.split('-'))
    born = date(year, month, day)
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def derive_high_heart_rate(heart_rate: int) -> int:
    return 1 if heart_rate > 100 else 0

def derive_elevated_troponin(elevated_troponin: float) -> int:
    return 1 if elevated_troponin > 0.04 else 0

def merge_all_features(patient_form: dict, provider_data: dict, fhir_data: dict | None = None) -> RiskInput:
    fhir_data = fhir_data or {}

    #age from FHIR when available if not calculate from dob in form
    age = fhir_data.get("age", 0)
    if not age:
        age = calculate_age(patient_form.get("dob", ""))

    return RiskInput(
        chest_pain=patient_form.get("chest_pain", 0),
        shortness_of_breath=patient_form.get("shortness_of_breath", 0),
        smoking=patient_form.get("smoking", 0),
        age=age,
        hypertension=fhir_data.get("hypertension", 0),
        diabetes=fhir_data.get("diabetes", 0),
        heart_disease_history=(
            1 if (
                fhir_data.get("heart_disease_history", 0)
                or fhir_data.get("coronary_artery_disease", 0)
                or fhir_data.get("myocardial_infarction", 0)
                or fhir_data.get("cardiovascular_disease", 0)
            ) else 0
        ),
        elevated_troponin=derive_elevated_troponin(provider_data.get("elevated_troponin", 0)),
        ecg=provider_data.get("ecg", 0),
        heart_rate=derive_high_heart_rate(provider_data.get("heart_rate", 0)),
    )

# def extract_age_from_ehr(ehr_data: dict) -> int:
#     return calculate_age(ehr_data.get("birthDate", ""))

# def extract_high_rate_from_observations(observations: list) -> int:
#     entries = observations.get("entry", [])
#     for entry in entries:
#         resource = entry.get("resource", {})
#         if resource.get("code", {}).get("coding", [{}])[0].get("code") == "8867-4":  # LOINC code for heart rate
#             value = resource.get("valueQuantity", {}).get("value")
#             if value and value > 100:  # Threshold for high heart rate
#                 return 1
#     return 0

# def extract_elevated_troponin(observations: list) -> int:
#     entries = observations.get("entry", [])
#     for entry in entries:
#         resource = entry.get("resource", {})
#         if resource.get("code", {}).get("coding", [{}])[0].get("code") == "6598-7":  # LOINC code for troponin
#             value = resource.get("valueQuantity", {}).get("value")
#             if value and value > 0.04:  # Threshold for elevated troponin
#                 return 1
#     return 0

# def has_condition(conditions: list, condition_code: str) -> int:
#     entries = conditions.get("entry", [])
#     for entry in entries:
#         resource = entry.get("resource", {})
#         if resource.get("code", {}).get("coding", [{}])[0].get("code") == condition_code:
#             return 1
#     return 0

# def build_ehr_features(patient: dict, observations: dict, conditions: dict) -> dict:
#     return {
#         "age": extract_age_from_ehr(patient),
#         "elevated_troponin": extract_elevated_troponin(observations),
#         "ecg_abnormalities": has_condition(conditions, "I48"),  # Atrial fibrillation ~ ECG abnormalities
#         "hypertension": has_condition(conditions, ["hypertension"]), # code I10
#         "diabetes": has_condition(conditions, ["diabetes"]), # code E11
#         "smoking": has_condition(conditions, ["smoking", "nicotine"]), # code F17
#         "heart_disease_history": has_condition(conditions, ["coronary_artery_disease", "myocardial_infarction", "heart_disease", "cardiovascular_disease"]), # code I25
#         "high_heart_rate": extract_high_rate_from_observations(observations)
#     }


# def combine_form_and_ehr(form_data: dict, ehr_data: dict) -> Inputs:
#     combined_data = {
#         "age": ehr_data.get("age", form_data.get("age")),
#         "chest_pain": form_data.get("chest_pain", 0),
#         "shortness_of_breath": form_data.get("shortness_of_breath", 0),
#         "radiating_pain": form_data.get("radiating_pain", 0),
#         "elevated_troponin": ehr_data.get("elevated_troponin", form_data.get("elevated_troponin")),
#         "ecg_abnormalities": ehr_data.get("ecg_abnormalities", form_data.get("ecg_abnormalities")),
#         "hypertension": ehr_data.get("hypertension", form_data.get("hypertension")),
#         "diabetes": ehr_data.get("diabetes", form_data.get("diabetes")),
#         "smoking": ehr_data.get("smoking", form_data.get("smoking")),
#         "heart_disease_history": ehr_data.get("heart_disease_history", form_data.get("heart_disease_history")),
#         "high_heart_rate": ehr_data.get("high_heart_rate", form_data.get("high_heart_rate"))
#     }

    # return Inputs(**combined_data)