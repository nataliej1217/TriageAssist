#from http.client import HTTPException
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import PatientIntakeInput, ProviderVitalsInput, FinalAssessmentRequest
from model import predict_risk
from fhir_utils import (get_metadata, search_patients, get_patient_data, get_observations, get_conditions, build_ehr_features)
from feature_builder import merge_all_features

app = FastAPI(title="TriageAssist API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")

def root():
    return {"message": "TriageAssist API is running"}

#re order
@app.get("/fhir/metadata")
def fhir_metadata():
    try:
        return get_metadata()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # from fhir_utils import get_metadata
    # return get_metadata()

@app.get("/fhir/patients")
def fhir_patients(name: str | None = None, count: int = 5):
    try:
        return search_patients(name = name, count = count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # from fhir_utils import search_patients
    # return search_patients(name, count)

@app.get("/fhir/patient/{patient_id}")
def fhir_patient(patient_id: str):
    try:
        return get_patient_data(patient_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/fhir/patient/{patient_id}/observations")
def fhir_patient_observations(patient_id: str, count: int = 50):
    try:
        return get_observations(patient_id, count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/fhir/patient/{patient_id}/conditions")
def fhir_patient_conditions(patient_id: str, count: int = 50):
    try:
        return get_conditions(patient_id, count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/fhir/features/{patient_id}")
def fhir_patient_features(patient_id: str):
    patient_data = get_patient_data(patient_id)
    observations = get_observations(patient_id)
    conditions = get_conditions(patient_id)

    ehr_data = build_ehr_features(patient_data, observations, conditions)
    return ehr_data


#New Input workflow
@app.post("/patientIntake")
def patient_intake(input: PatientIntakeInput):
    return {"message": "Patient intake submitted", "intakeData": input.dict()}

@app.post("/providerIntake")
def provider_intake(input: ProviderVitalsInput):
    return {"message": "Vitals submitted", "vitalsData": input.dict()}

@app.post("/final-risk-assessment")
def final_risk_assessment(inputData: FinalAssessmentRequest):
    try:
        patient_form = inputData.patient_intake.dict()
        provider_data = inputData.provider_triage.dict()

        ehr_data = {}

        if patient_form.get("returning_patient") == 1 and not provider_data.get("patient_id"):
            raise HTTPException(status_code=400, detail="Patient ID is required for returning patients.")

        if patient_form.get("returning_patient") == 1:
            patient_id = provider_data["patient_id"]
            patient = get_patient_data(patient_id)
            observations = get_observations(patient_id)
            conditions = get_conditions(patient_id)
            ehr_data = build_ehr_features(patient, observations, conditions)

        merged_inputs = merge_all_features(patient_form, provider_data, ehr_data)
        prediction = predict_risk(merged_inputs)

        return {
            "patient_intake": patient_form,
            "provider_triage": provider_data,
            "fhir_data": ehr_data,
            "merged_inputs": merged_inputs.dict(),
            "prediction": prediction
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/predict")
# def predict(input: RiskInput):
#     return predict_risk(input)

# @app.post("/predictFromFHIR/{patient_id}")
# def predict_from_fhir(patient_id: str, form_data: SymptomInput = Body(...)):
#     try:
#         patient_data = get_patient_data(patient_id)
#         observations = get_observations(patient_id)
#         conditions = get_conditions(patient_id)

#         ehr_data = build_ehr_features(patient_data, observations, conditions)
#         combined_input = combine_form_and_ehr(form_data.dict(), ehr_data)
#         combined_input.patient_id = patient_id
#         return {
#             "ehr_data": ehr_data,
#             "combined_input": combined_input.dict(),
#             "prediction": predict_risk(combined_input)
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    