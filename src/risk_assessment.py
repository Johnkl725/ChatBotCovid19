
# risk_assessment.py

from config import MESSAGES

def evaluate_risk(user_data):
    age = user_data.get("age", 0)
    symptoms = user_data.get("symptoms", [])
    comorbidities = user_data.get("comorbidities", [])
    exposure = user_data.get("exposure", False)

    # Convertir síntomas y comorbilidades a un formato más fácil de manejar
    has_fever = "Fiebre >38°C (🔥)" in symptoms
    has_cough = "Tos seca persistente (🤧)" in symptoms
    has_respiratory_difficulty = "Dificultad respiratoria (😮💨)" in symptoms
    has_chest_pain = "Dolor/presión torácica (💢)" in symptoms
    has_loss_of_smell_taste = "Pérdida olfato/gusto (👃❌)" in symptoms
    has_extreme_fatigue = "Fatiga extrema (😩)" in symptoms

    num_comorbidities = len(comorbidities)

    # Reglas de riesgo CRÍTICO
    if (has_respiratory_difficulty and has_chest_pain) or \
       (age > 65 and has_fever and num_comorbidities >= 2):
        return "CRÍTICO", MESSAGES["critical_risk"]

    # Reglas de riesgo MODERADO
    if (has_fever and has_cough and exposure) or \
       (40 <= age <= 64 and (has_fever or has_cough or has_respiratory_difficulty or has_chest_pain or has_loss_of_smell_taste or has_extreme_fatigue)):
        return "MODERADO", MESSAGES["moderate_risk"]

    # Reglas de riesgo BAJO
    if (not symptoms and not exposure) or \
       (len(symptoms) <= 1 and num_comorbidities == 0):
        return "BAJO", MESSAGES["low_risk"]

    # Si no encaja en ninguna categoría anterior, por defecto se considera moderado para precaución
    return "MODERADO", MESSAGES["moderate_risk"]


