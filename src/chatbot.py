from risk_assessment import evaluate_risk
from api_integrations import get_nearby_hospitals

# chatbot.py

from config import MESSAGES, OPTIONS
from utils import validate_age, get_multiple_choice_selection

class CoviAlertChatbot:
    def __init__(self):
        self.user_data = {}

    def start_chat(self):
        print(MESSAGES["welcome"])
        choice = input("Elige una opción: ")
        if choice == "1": # 🟢 Sí, evaluarme
            self.collect_user_data()
        else:
            print("Gracias por tu visita. ¡Cuídate!")

    def collect_user_data(self):
        # P1: Edad
        while True:
            age_input = input(MESSAGES["age_prompt"] + " ")
            is_valid, result = validate_age(age_input)
            if is_valid:
                self.user_data["age"] = result
                break
            else:
                print(result)

        # P2: Síntomas
        print("\n" + MESSAGES["symptoms_prompt"])
        selected_symptoms = get_multiple_choice_selection(OPTIONS["symptoms"], "Selecciona tus síntomas (ingresa el número y presiona Enter, 0 para terminar):")
        self.user_data["symptoms"] = selected_symptoms

        # P3: Comorbilidades
        print("\n" + MESSAGES["comorbidities_prompt"])
        selected_comorbidities = get_multiple_choice_selection(OPTIONS["comorbidities"], "Selecciona tus condiciones (ingresa el número y presiona Enter, 0 para terminar):")
        self.user_data["comorbidities"] = selected_comorbidities

        # P4: Exposición
        while True:
            print("\n" + MESSAGES["exposure_prompt"])
            for i, option in enumerate(OPTIONS["exposure_options"]):
                print(f"{i + 1}. {option}")
            exposure_choice = input("Elige una opción: ")
            if exposure_choice == "1": # ✔️ Sí
                self.user_data["exposure"] = True
                break
            elif exposure_choice == "2": # ❌ No
                self.user_data["exposure"] = False
                break
            else:
                print("Opción inválida. Por favor, elige 1 o 2.")

        print("Datos recopilados:", self.user_data)
        # Aquí se llamaría al algoritmo de evaluación de riesgos
                # self.evaluate_risk()
        self.evaluate_risk()

    def evaluate_risk(self):
        risk_level, risk_message = evaluate_risk(self.user_data)
        print(f"\nNivel de Riesgo: {risk_level}\n{risk_message}")
        self.closing_message()

    def closing_message(self):
        print(MESSAGES["closing"])
        while True:
            for i, option in enumerate(OPTIONS["closing_options"]):
                print(f"{i + 1}. {option}")
            closing_choice = input("Elige una opción: ")
            if closing_choice == "1": # 🔁 Nueva evaluación
                self.user_data = {}
                self.start_chat()
                break
            elif closing_choice == "2": # 📍 Ver hospitales cercanos
                print(get_nearby_hospitals())
            elif closing_choice == "3": # 📚 Consejos de prevención
                print("Aquí irían los consejos de prevención.") # Placeholder
            else:
                print("Opción inválida. Por favor, elige una opción válida.")


