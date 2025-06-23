# api_integrations.py

import requests

def get_nearby_hospitals(location=None):
    """Simula la búsqueda de hospitales cercanos con información más útil."""
    if location:
        return (f"🏥 Para encontrar hospitales cercanos a '{location}':\n\n"
               "📱 Opciones rápidas:\n"
               "• Google Maps: busca 'hospitales cerca de mí'\n"
               "• Waze: busca 'hospital' o 'emergencias'\n"
               "• App de tu seguro médico\n\n"
               "📞 Números de emergencia:\n"
               "• Emergencias: 911\n"
               "• Cruz Roja: 132\n"
               "• Bomberos: 119\n\n"
               "💡 Tip: Llama antes de ir para confirmar disponibilidad y protocolos COVID")
    else:
        return ("🏥 Para encontrar hospitales cercanos:\n\n"
               "📱 Opciones rápidas:\n"
               "• Google Maps: busca 'hospitales cerca de mí'\n"
               "• Waze: busca 'hospital' o 'emergencias'\n"
               "• App de tu seguro médico\n\n"
               "📞 Números de emergencia:\n"
               "• Emergencias: 911\n"
               "• Cruz Roja: 132\n"
               "• Bomberos: 119\n\n"
               "💡 Tip: Llama antes de ir para confirmar disponibilidad y protocolos COVID")

def get_personalized_advice(user_data):
    """Genera consejos personalizados basados en los datos del usuario."""
    from config import SYMPTOM_SPECIFIC_ADVICE, PREVENTION_TIPS
    
    age = user_data.get("age", 0)
    symptoms = user_data.get("symptoms", [])
    comorbidities = user_data.get("comorbidities", [])
    
    advice = "🎯 CONSEJOS PERSONALIZADOS PARA TI:\n\n"
    
    # Consejos específicos por síntomas
    if symptoms:
        advice += "💊 CUIDADOS ESPECÍFICOS POR SÍNTOMAS:\n\n"
        for symptom in symptoms:
            if symptom in SYMPTOM_SPECIFIC_ADVICE:
                symptom_advice = SYMPTOM_SPECIFIC_ADVICE[symptom]
                advice += f"🔸 {symptom}:\n"
                for care in symptom_advice["cuidados"]:
                    advice += f"  {care}\n"
                advice += f"⚠️ {symptom_advice['alarma']}\n\n"
    
    # Consejos específicos por edad
    if age >= 65:
        advice += "👴 CUIDADOS ESPECIALES POR EDAD (65+):\n"
        advice += "• Extrema las precauciones de aislamiento\n"
        advice += "• Mantén comunicación diaria con familiares\n"
        advice += "• Ten medicamentos habituales disponibles\n"
        advice += "• Considera telemedicina para consultas\n"
        advice += "• Busca atención médica ante cualquier empeoramiento\n\n"
    elif age < 18:
        advice += "👶 CUIDADOS ESPECIALES PARA MENORES:\n"
        advice += "• Supervisión constante de adultos\n"
        advice += "• Hidratación frecuente en pequeñas cantidades\n"
        advice += "• Consulta pediátrica si hay dudas\n"
        advice += "• Mantén rutinas de sueño regulares\n\n"
    
    # Consejos específicos por comorbilidades
    if comorbidities:
        advice += "🏥 CUIDADOS POR CONDICIONES PREEXISTENTES:\n\n"
        for condition in comorbidities:
            if condition == "Diabetes":
                advice += "🍬 Diabetes:\n"
                advice += "• Monitorea glucosa más frecuentemente\n"
                advice += "• Mantén medicamentos al día\n"
                advice += "• Hidrátate sin azúcares añadidos\n"
                advice += "• Contacta endocrinólogo si hay descontrol\n\n"
            elif condition == "Hipertensión":
                advice += "💓 Hipertensión:\n"
                advice += "• Toma presión arterial diariamente\n"
                advice += "• No suspendas medicamentos antihipertensivos\n"
                advice += "• Reduce consumo de sal\n"
                advice += "• Evita estrés excesivo\n\n"
            elif condition == "EPOC":
                advice += "🫁 EPOC:\n"
                advice += "• Usa inhaladores según prescripción\n"
                advice += "• Evita irritantes respiratorios\n"
                advice += "• Mantén oxímetro disponible\n"
                advice += "• Consulta neumólogo si empeoras\n\n"
            elif condition == "Enfermedad cardiaca":
                advice += "❤️ Enfermedad cardiaca:\n"
                advice += "• Toma medicamentos cardíacos puntualmente\n"
                advice += "• Evita esfuerzos físicos intensos\n"
                advice += "• Monitorea síntomas cardíacos\n"
                advice += "• Ten nitroglicerina disponible si la usas\n\n"
            elif condition == "Obesidad":
                advice += "⚖️ Obesidad:\n"
                advice += "• Mantén alimentación balanceada\n"
                advice += "• Hidrátate adecuadamente\n"
                advice += "• Realiza actividad física ligera cuando te sientas mejor\n"
                advice += "• Monitorea síntomas respiratorios\n\n"
            elif condition == "Inmunosupresión":
                advice += "🛡️ Inmunosupresión:\n"
                advice += "• Extrema medidas de aislamiento\n"
                advice += "• Contacta inmediatamente a tu médico\n"
                advice += "• No suspendas medicamentos sin consultar\n"
                advice += "• Evita contacto con otras personas enfermas\n\n"
    
    # Consejos generales de prevención
    advice += "🛡️ PREVENCIÓN GENERAL:\n\n"
    advice += "🧼 Higiene:\n"
    for tip in PREVENTION_TIPS["higiene"]:
        advice += f"  {tip}\n"
    
    advice += "\n📏 Distanciamiento:\n"
    for tip in PREVENTION_TIPS["distanciamiento"]:
        advice += f"  {tip}\n"
    
    advice += "\n💪 Salud general:\n"
    for tip in PREVENTION_TIPS["salud"]:
        advice += f"  {tip}\n"
    
    return advice

def get_home_care_guide():
    """Proporciona una guía completa de cuidados en casa."""
    return """🏠 GUÍA COMPLETA DE CUIDADOS EN CASA

🛏️ AISLAMIENTO:
• Quédate en una habitación separada
• Usa baño exclusivo si es posible
• Mantén puerta cerrada y ventana abierta
• Usa mascarilla al salir de la habitación
• Evita áreas comunes de la casa

🍽️ ALIMENTACIÓN:
• Come alimentos nutritivos y fáciles de digerir
• Incluye frutas ricas en vitamina C (naranja, kiwi)
• Consume caldos y sopas tibias
• Evita alimentos procesados y azúcar en exceso
• Come en pequeñas porciones frecuentes

💧 HIDRATACIÓN:
• Bebe al menos 8-10 vasos de agua al día
• Incluye tés de hierbas (manzanilla, jengibre)
• Evita alcohol y bebidas con cafeína en exceso
• Agua tibia con limón y miel

😴 DESCANSO:
• Duerme 8-10 horas por noche
• Toma siestas cortas si es necesario
• Mantén horarios regulares de sueño
• Usa almohadas extra para elevar la cabeza

🌡️ MONITOREO:
• Toma temperatura 2 veces al día
• Registra síntomas en un diario
• Usa oxímetro si tienes disponible
• Pesa diariamente si es posible

🧼 HIGIENE:
• Lávate las manos frecuentemente
• Cambia ropa de cama cada 2-3 días
• Desinfecta superficies que tocas
• Usa utensilios exclusivos para comer

👥 COMUNICACIÓN:
• Mantén contacto diario con familiares
• Informa cambios en síntomas
• Ten números de emergencia a mano
• Considera telemedicina para consultas

⏰ DURACIÓN DEL AISLAMIENTO:
• Mínimo 5 días desde inicio de síntomas
• Hasta 24 horas sin fiebre (sin medicamentos)
• Hasta que síntomas mejoren significativamente
• Usa mascarilla 5 días adicionales al salir"""

def get_alarm_signals():
    """Proporciona las señales de alarma que requieren atención médica inmediata."""
    from config import ALARM_SIGNALS
    
    message = "🚨 SEÑALES DE ALARMA - BUSCA ATENCIÓN MÉDICA INMEDIATA:\n\n"
    
    for signal in ALARM_SIGNALS:
        message += f"{signal}\n"
    
    message += "\n📞 QUÉ HACER:\n"
    message += "• Llama al 911 inmediatamente\n"
    message += "• No conduzcas tú mismo al hospital\n"
    message += "• Informa que tienes síntomas de COVID-19\n"
    message += "• Usa mascarilla en todo momento\n"
    message += "• Lleva lista de medicamentos que tomas\n\n"
    message += "⚠️ NO ESPERES - Es mejor prevenir que lamentar"
    
    return message

