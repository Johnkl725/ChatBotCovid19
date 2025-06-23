# config.py

# Mensajes del chatbot
MESSAGES = {
    "welcome": "¡Hola 👋! Soy COVI-ALERT 🦠🔍, tu asistente para evaluación preventiva de COVID-19.\n📌 Analizaré tus síntomas en 2 minutos y te diré:\n✓ Nivel de riesgo (✅🟠🔴)\n✓ Recomendaciones personalizadas\n✓ Alertas tempranas\n\n¿Comenzamos? Responde '1' para sí o '2' para salir",
    "age_prompt": "🔢 ¿Qué edad tienes? Esto ayuda a calibrar tu riesgo:",
    "symptoms_prompt": "🌡️ Por favor, indica todos tus síntomas actuales:",
    "comorbidities_prompt": "⚠️ ¿Tienes alguna de estas condiciones?:",
    "exposure_prompt": "🦠 ¿Tuviste contacto con un caso confirmado de COVID-19 en los últimos 5 días?",
    "critical_risk": "🚨 ALERTA ROJA │ Probabilidad alta de COVID-19 grave\n🔺 Acción inmediata:\n\n• Llama al servicio de emergencias (911)\n• Aíslate en área ventilada\n• Monitorea oxigenación si tienes oxímetro\n• NO te automediques\n• Busca atención médica URGENTE\n\n📞 Contactos de emergencia:\n• Emergencias: 911\n• Línea COVID: 113",
    "moderate_risk": "⚠️ Riesgo Intermedio │ Posible infección activa\n📋 Recomendaciones:\n\n• Hazte prueba PCR o antígeno en 24h\n• Aíslate preventivamente\n• Controla temperatura cada 6 horas\n• Mantén hidratación constante\n• Descansa y evita esfuerzos\n• Usa mascarilla siempre\n• Consulta médico si empeoras\n\n📍 Centros de prueba: Busca 'centros COVID cerca de mí'",
    "low_risk": "✅ Bajo riesgo │ Mantén precauciones\n🛡️ Medidas preventivas:\n\n• Mantén vacunación actualizada\n• Usa mascarilla en espacios cerrados\n• Lávate las manos frecuentemente\n• Mantén distancia de 2 metros\n• Ventila espacios cerrados\n• Evita aglomeraciones\n• Monitorea síntomas diariamente\n\n📲 Re-evalúa si aparecen nuevos síntomas",
    "closing": "Gracias por usar COVI-ALERT. Recuerda:\n❗ Esta evaluación no sustituye diagnóstico médico.\n\n¿Deseas:\n1. 🔁 Nueva evaluación\n2. 📍 Ver hospitales cercanos\n3. 📚 Consejos personalizados\n4. 🏠 Cuidados en casa\n5. 🚨 Señales de alarma"
}

# Opciones para preguntas de selección múltiple
OPTIONS = {
    "welcome_options": ["🟢 Sí, evaluarme", "🔴 Salir"],
    "symptoms": [
        "Fiebre >38°C (🔥)",
        "Tos seca persistente (🤧)",
        "Dificultad respiratoria (😮💨)",
        "Dolor/presión torácica (💢)",
        "Pérdida olfato/gusto (👃❌)",
        "Fatiga extrema (😩)"
    ],
    "comorbidities": [
        "Diabetes",
        "Hipertensión",
        "EPOC",
        "Enfermedad cardiaca",
        "Obesidad",
        "Inmunosupresión"
    ],
    "exposure_options": ["✔️ Sí", "❌ No"],
    "closing_options": ["🔁 Nueva evaluación", "📍 Ver hospitales cercanos", "📚 Consejos personalizados", "🏠 Cuidados en casa", "🚨 Señales de alarma"]
}

# Consejos específicos según síntomas
SYMPTOM_SPECIFIC_ADVICE = {
    "Fiebre >38°C (🔥)": {
        "cuidados": [
            "🌡️ Controla tu temperatura cada 4-6 horas",
            "💊 Puedes usar paracetamol (acetaminofén) según indicaciones del envase",
            "🧊 Aplica compresas frías en frente y muñecas",
            "💧 Aumenta la ingesta de líquidos (agua, caldos, tés)",
            "🛏️ Descansa en ambiente fresco y ventilado",
            "👕 Usa ropa ligera y transpirable"
        ],
        "alarma": "Si la fiebre supera 39.5°C o persiste más de 3 días, busca atención médica"
    },
    "Tos seca persistente (🤧)": {
        "cuidados": [
            "🍯 Toma miel pura (1 cucharada) para calmar la garganta",
            "☕ Bebe líquidos tibios (té con limón, caldos)",
            "💨 Inhala vapor de agua caliente (ducha o bowl con toalla)",
            "🚭 Evita irritantes como humo y perfumes fuertes",
            "😷 Usa mascarilla para proteger a otros",
            "🛏️ Duerme con la cabeza elevada"
        ],
        "alarma": "Si la tos produce sangre o empeora significativamente, consulta médico"
    },
    "Dificultad respiratoria (😮💨)": {
        "cuidados": [
            "🧘 Practica respiración lenta y profunda",
            "🪑 Siéntate derecho o inclínate hacia adelante",
            "🌬️ Mantén ambiente bien ventilado",
            "😌 Evita esfuerzos físicos",
            "📱 Ten teléfono cerca para emergencias"
        ],
        "alarma": "⚠️ BUSCA ATENCIÓN MÉDICA INMEDIATA si tienes dificultad severa para respirar"
    },
    "Dolor/presión torácica (💢)": {
        "cuidados": [
            "🛏️ Descansa en posición cómoda",
            "🧊 Aplica calor suave en el pecho",
            "🧘 Practica técnicas de relajación",
            "📱 Mantén comunicación con familiares"
        ],
        "alarma": "🚨 EMERGENCIA: Si el dolor es severo o se irradia al brazo/mandíbula, llama al 911"
    },
    "Pérdida olfato/gusto (👃❌)": {
        "cuidados": [
            "🌹 Practica entrenamiento olfativo con aromas fuertes",
            "🧄 Usa especias y condimentos para estimular el gusto",
            "🍋 Prueba sabores intensos como limón o menta",
            "⏰ Ten paciencia, puede tardar semanas en recuperarse",
            "🔥 Ten cuidado con gas y alimentos en mal estado"
        ],
        "alarma": "Si no hay mejoría después de 2 semanas, consulta con especialista"
    },
    "Fatiga extrema (😩)": {
        "cuidados": [
            "😴 Duerme 8-10 horas diarias",
            "🍎 Mantén alimentación nutritiva y balanceada",
            "💧 Hidrátate constantemente",
            "🚶 Haz actividad física muy ligera cuando te sientas mejor",
            "🧘 Practica meditación o relajación",
            "⏰ Respeta los tiempos de tu cuerpo"
        ],
        "alarma": "Si la fatiga es extrema y no mejora con descanso, consulta médico"
    }
}

# Consejos generales de prevención
PREVENTION_TIPS = {
    "higiene": [
        "🧼 Lávate las manos frecuentemente con agua y jabón por 20 segundos",
        "🤲 Usa gel antibacterial con al menos 60% alcohol",
        "👁️ Evita tocarte ojos, nariz y boca con manos sucias",
        "🧽 Desinfecta superficies frecuentemente tocadas"
    ],
    "distanciamiento": [
        "📏 Mantén distancia de 2 metros con otras personas",
        "😷 Usa mascarilla en espacios cerrados y transporte público",
        "🏠 Evita reuniones en espacios cerrados mal ventilados",
        "🚶 Prefiere actividades al aire libre"
    ],
    "salud": [
        "💉 Mantén tu esquema de vacunación completo",
        "🍎 Consume alimentación balanceada rica en vitaminas",
        "💧 Mantente bien hidratado",
        "😴 Duerme 7-8 horas diarias",
        "🏃 Realiza ejercicio regular moderado",
        "🚭 Evita fumar y consumo excesivo de alcohol"
    ]
}

# Señales de alarma que requieren atención médica inmediata
ALARM_SIGNALS = [
    "🫁 Dificultad severa para respirar o falta de aire",
    "💙 Labios o cara azulados",
    "💢 Dolor persistente o presión en el pecho",
    "🧠 Confusión mental o dificultad para mantenerse despierto",
    "🌡️ Fiebre alta persistente (>39.5°C) que no baja con medicamentos",
    "🤮 Vómitos persistentes que impiden retener líquidos",
    "😵 Mareos severos o desmayos",
    "🩸 Tos con sangre",
    "🔥 Empeoramiento súbito de síntomas"
]

