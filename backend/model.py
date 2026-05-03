import math
from schemas import RiskInput

#figure out weigths
WEIGHTS = {
    "intercept": -5.0,
    "chest_pain": 1.2,
    "shortness_of_breath": 0.8,
    "age": 0.05,
    "elevated_troponin": 2.0,
    "ecg": 1.7,
    "hypertension": 0.6,
    "diabetes": 0.6,
    "smoking": 0.5,
    "heart_disease_history": 1.5,
    "heart_rate": 0.6,
    # "radiating_pain": 0.7,
}

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def compute_x(inputs: RiskInput):
    x = WEIGHTS["intercept"]
    x += WEIGHTS["chest_pain"] * inputs.chest_pain
    x += WEIGHTS["shortness_of_breath"] * inputs.shortness_of_breath
    x += WEIGHTS["age"] * inputs.age
    x += WEIGHTS["elevated_troponin"] * inputs.elevated_troponin
    x += WEIGHTS["ecg"] * inputs.ecg
    x += WEIGHTS["hypertension"] * inputs.hypertension
    x += WEIGHTS["diabetes"] * inputs.diabetes
    x += WEIGHTS["smoking"] * inputs.smoking
    x += WEIGHTS["heart_disease_history"] * inputs.heart_disease_history
    x += WEIGHTS["heart_rate"] * inputs.heart_rate
    # x += WEIGHTS["radiating_pain"] * inputs.radiating_pain
    return x

#determine risk category bounds
def risk_category(riskScore):
    if riskScore < 0.3:
        return "low"
    elif riskScore < 0.6:
        return "medium"
    else:
        return "high"

def predict_risk(inputs: RiskInput):
    x = compute_x(inputs)
    riskScore = sigmoid(x)
    category = risk_category(riskScore)
    return {"riskScore": riskScore, "category": category}