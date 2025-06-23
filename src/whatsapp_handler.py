# whatsapp_handler.py

import requests
import json
import os
from flask import request, jsonify
from chatbot import CoviAlertChatbot

class WhatsAppHandler:
    def __init__(self):
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN', 'YOUR_ACCESS_TOKEN_HERE')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID', 'YOUR_PHONE_NUMBER_ID_HERE')
        self.verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN', 'YOUR_VERIFY_TOKEN_HERE')
        self.api_url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"
        
        # Almacenamiento en memoria para el estado de las conversaciones
        # En producción, esto debería ser una base de datos
        self.user_sessions = {}

    def verify_webhook(self):
        """Verifica el webhook de WhatsApp"""
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == self.verify_token:
            return challenge
        else:
            return 'Forbidden', 403

    def handle_webhook(self):
        """Maneja los mensajes entrantes del webhook de WhatsApp"""
        try:
            data = request.get_json()
            
            if 'entry' in data:
                for entry in data['entry']:
                    if 'changes' in entry:
                        for change in entry['changes']:
                            if 'value' in change and 'messages' in change['value']:
                                for message in change['value']['messages']:
                                    self.process_message(message, change['value'])
            
            return jsonify({'status': 'success'}), 200
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return jsonify({'status': 'error'}), 500

    def process_message(self, message, value):
        """Procesa un mensaje individual"""
        sender = message['from']
        message_text = message.get('text', {}).get('body', '')
        
        # Obtener o crear sesión del usuario
        if sender not in self.user_sessions:
            self.user_sessions[sender] = {
                'chatbot': CoviAlertChatbot(),
                'state': 'welcome',
                'data': {}
            }
        
        session = self.user_sessions[sender]
        
        # Procesar el mensaje según el estado actual
        response = self.process_conversation_state(session, message_text)
        
        # Enviar respuesta
        if response:
            # Si la respuesta es muy larga, dividirla en múltiples mensajes
            if len(response) > 1600:
                self.send_long_message(sender, response)
            else:
                self.send_message(sender, response)

    def process_conversation_state(self, session, message_text):
        """Procesa el estado de la conversación y genera una respuesta"""
        chatbot = session['chatbot']
        state = session['state']
        
        # Manejar comandos especiales en cualquier momento
        if message_text.lower() in ['ayuda', 'help', 'menu']:
            return self.get_help_menu()
        elif message_text.lower() in ['reiniciar', 'restart', 'empezar']:
            session['state'] = 'welcome'
            session['data'] = {}
            from config import MESSAGES
            return MESSAGES["welcome"]
        
        if state == 'welcome':
            if message_text.lower() in ['1', 'si', 'sí', 'evaluar', 'comenzar', 'empezar']:
                session['state'] = 'age'
                return "🔢 ¿Qué edad tienes? Esto ayuda a calibrar tu riesgo:\n\n💡 Escribe solo el número (ej: 25)"
            else:
                return "Gracias por tu visita. ¡Cuídate! 🙏\n\nEscribe 'empezar' si cambias de opinión."
        
        elif state == 'age':
            from utils import validate_age
            is_valid, result = validate_age(message_text)
            if is_valid:
                session['data']['age'] = result
                session['state'] = 'symptoms'
                return ("🌡️ Por favor, indica todos tus síntomas actuales:\n\n"
                       "1️⃣ Fiebre >38°C (🔥)\n"
                       "2️⃣ Tos seca persistente (🤧)\n"
                       "3️⃣ Dificultad respiratoria (😮💨)\n"
                       "4️⃣ Dolor/presión torácica (💢)\n"
                       "5️⃣ Pérdida olfato/gusto (👃❌)\n"
                       "6️⃣ Fatiga extrema (😩)\n\n"
                       "💡 Responde con los números separados por comas\n"
                       "Ejemplo: 1,2,5\n"
                       "Si no tienes síntomas, escribe: ninguno")
            else:
                return f"❌ {result}\n\n💡 Por favor, escribe solo tu edad en números (ej: 25)"
        
        elif state == 'symptoms':
            symptoms = self.parse_symptoms(message_text)
            session['data']['symptoms'] = symptoms
            session['state'] = 'comorbidities'
            
            # Mostrar síntomas seleccionados para confirmación
            if symptoms:
                symptoms_text = "✅ Síntomas registrados:\n"
                for i, symptom in enumerate(symptoms, 1):
                    symptoms_text += f"{i}. {symptom}\n"
                symptoms_text += "\n"
            else:
                symptoms_text = "✅ Sin síntomas registrados\n\n"
            
            return (symptoms_text +
                   "⚠️ ¿Tienes alguna de estas condiciones médicas?:\n\n"
                   "1️⃣ Diabetes\n"
                   "2️⃣ Hipertensión\n"
                   "3️⃣ EPOC (enfermedad pulmonar)\n"
                   "4️⃣ Enfermedad cardiaca\n"
                   "5️⃣ Obesidad\n"
                   "6️⃣ Inmunosupresión\n\n"
                   "💡 Responde con los números separados por comas\n"
                   "Ejemplo: 1,3\n"
                   "Si no tienes ninguna, escribe: ninguno")
        
        elif state == 'comorbidities':
            comorbidities = self.parse_comorbidities(message_text)
            session['data']['comorbidities'] = comorbidities
            session['state'] = 'exposure'
            
            # Mostrar condiciones seleccionadas para confirmación
            if comorbidities:
                conditions_text = "✅ Condiciones registradas:\n"
                for i, condition in enumerate(comorbidities, 1):
                    conditions_text += f"{i}. {condition}\n"
                conditions_text += "\n"
            else:
                conditions_text = "✅ Sin condiciones preexistentes registradas\n\n"
            
            return (conditions_text +
                   "🦠 ¿Tuviste contacto cercano con un caso confirmado de COVID-19 en los últimos 5 días?\n\n"
                   "💡 Responde:\n"
                   "• 'sí' o '1' si tuviste contacto\n"
                   "• 'no' o '2' si no tuviste contacto\n\n"
                   "ℹ️ Contacto cercano = menos de 2 metros por más de 15 minutos")
        
        elif state == 'exposure':
            exposure = message_text.lower() in ['si', 'sí', '1', 'yes', 'contacto']
            session['data']['exposure'] = exposure
            
            # Evaluar riesgo
            from risk_assessment import evaluate_risk
            risk_level, risk_message = evaluate_risk(session['data'])
            
            # Agregar resumen de datos
            summary = self.generate_summary(session['data'])
            
            session['state'] = 'closing'
            return (f"📊 RESUMEN DE TU EVALUACIÓN:\n{summary}\n\n"
                   f"🎯 RESULTADO:\n"
                   f"Nivel de Riesgo: {risk_level}\n\n{risk_message}\n\n"
                   "Gracias por usar COVI-ALERT. Recuerda:\n"
                   "❗ Esta evaluación no sustituye diagnóstico médico.\n\n"
                   "¿Qué necesitas ahora?\n"
                   "1️⃣ 🔁 Nueva evaluación\n"
                   "2️⃣ 📍 Ver hospitales cercanos\n"
                   "3️⃣ 📚 Consejos personalizados\n"
                   "4️⃣ 🏠 Cuidados en casa\n"
                   "5️⃣ 🚨 Señales de alarma")
        
        elif state == 'closing':
            if message_text == '1':
                # Reiniciar sesión
                session['state'] = 'welcome'
                session['data'] = {}
                from config import MESSAGES
                return MESSAGES["welcome"]
            elif message_text == '2':
                from api_integrations import get_nearby_hospitals
                return get_nearby_hospitals()
            elif message_text == '3':
                from api_integrations import get_personalized_advice
                return get_personalized_advice(session['data'])
            elif message_text == '4':
                from api_integrations import get_home_care_guide
                return get_home_care_guide()
            elif message_text == '5':
                from api_integrations import get_alarm_signals
                return get_alarm_signals()
            else:
                return ("❓ Opción no válida. Por favor, elige:\n\n"
                       "1️⃣ 🔁 Nueva evaluación\n"
                       "2️⃣ 📍 Ver hospitales cercanos\n"
                       "3️⃣ 📚 Consejos personalizados\n"
                       "4️⃣ 🏠 Cuidados en casa\n"
                       "5️⃣ 🚨 Señales de alarma\n\n"
                       "💡 Escribe solo el número de la opción")
        
        return "🤔 Lo siento, no entendí tu mensaje.\n\n💡 Escribe 'ayuda' para ver el menú de opciones o 'empezar' para una nueva evaluación."

    def generate_summary(self, user_data):
        """Genera un resumen de los datos del usuario"""
        age = user_data.get("age", 0)
        symptoms = user_data.get("symptoms", [])
        comorbidities = user_data.get("comorbidities", [])
        exposure = user_data.get("exposure", False)
        
        summary = f"👤 Edad: {age} años\n"
        
        if symptoms:
            summary += f"🌡️ Síntomas: {len(symptoms)} reportados\n"
            for symptom in symptoms:
                summary += f"  • {symptom}\n"
        else:
            summary += "🌡️ Síntomas: Ninguno reportado\n"
        
        if comorbidities:
            summary += f"⚠️ Condiciones: {len(comorbidities)} reportadas\n"
            for condition in comorbidities:
                summary += f"  • {condition}\n"
        else:
            summary += "⚠️ Condiciones: Ninguna reportada\n"
        
        summary += f"🦠 Contacto COVID: {'Sí' if exposure else 'No'}\n"
        
        return summary

    def get_help_menu(self):
        """Proporciona el menú de ayuda"""
        return ("📋 MENÚ DE AYUDA - COVI-ALERT\n\n"
               "🔍 COMANDOS DISPONIBLES:\n"
               "• 'empezar' - Nueva evaluación\n"
               "• 'ayuda' - Mostrar este menú\n"
               "• 'reiniciar' - Volver al inicio\n\n"
               "🎯 FUNCIONES PRINCIPALES:\n"
               "1️⃣ Evaluación de riesgo COVID-19\n"
               "2️⃣ Consejos personalizados\n"
               "3️⃣ Guía de cuidados en casa\n"
               "4️⃣ Señales de alarma\n"
               "5️⃣ Ubicación de hospitales\n\n"
               "💡 TIPS:\n"
               "• Responde con números cuando se solicite\n"
               "• Sé específico en tus respuestas\n"
               "• Esta herramienta NO reemplaza consulta médica\n\n"
               "¿Qué necesitas? Escribe 'empezar' para comenzar.")

    def parse_symptoms(self, message_text):
        """Parsea la selección de síntomas del usuario"""
        from config import OPTIONS
        symptoms = []
        
        if message_text.lower() in ['ninguno', 'ninguna', '0', 'no', 'sin sintomas', 'sin síntomas']:
            return symptoms
        
        try:
            # Limpiar el texto y extraer números
            clean_text = message_text.replace(' ', '').replace('.', ',')
            numbers = [int(x.strip()) for x in clean_text.split(',') if x.strip().isdigit()]
            
            for num in numbers:
                if 1 <= num <= len(OPTIONS['symptoms']):
                    symptoms.append(OPTIONS['symptoms'][num - 1])
        except:
            # Si no se pueden parsear números, buscar palabras clave
            text_lower = message_text.lower()
            if any(word in text_lower for word in ['fiebre', 'temperatura', 'calentura']):
                symptoms.append(OPTIONS['symptoms'][0])
            if any(word in text_lower for word in ['tos', 'toser']):
                symptoms.append(OPTIONS['symptoms'][1])
            if any(word in text_lower for word in ['respirar', 'aire', 'ahogo', 'falta']):
                symptoms.append(OPTIONS['symptoms'][2])
            if any(word in text_lower for word in ['pecho', 'torax', 'dolor']):
                symptoms.append(OPTIONS['symptoms'][3])
            if any(word in text_lower for word in ['olfato', 'gusto', 'sabor', 'oler']):
                symptoms.append(OPTIONS['symptoms'][4])
            if any(word in text_lower for word in ['cansancio', 'fatiga', 'agotado']):
                symptoms.append(OPTIONS['symptoms'][5])
        
        return symptoms

    def parse_comorbidities(self, message_text):
        """Parsea la selección de comorbilidades del usuario"""
        from config import OPTIONS
        comorbidities = []
        
        if message_text.lower() in ['ninguno', 'ninguna', '0', 'no', 'sin condiciones']:
            return comorbidities
        
        try:
            # Limpiar el texto y extraer números
            clean_text = message_text.replace(' ', '').replace('.', ',')
            numbers = [int(x.strip()) for x in clean_text.split(',') if x.strip().isdigit()]
            
            for num in numbers:
                if 1 <= num <= len(OPTIONS['comorbidities']):
                    comorbidities.append(OPTIONS['comorbidities'][num - 1])
        except:
            # Si no se pueden parsear números, buscar palabras clave
            text_lower = message_text.lower()
            if any(word in text_lower for word in ['diabetes', 'diabetico', 'azucar']):
                comorbidities.append(OPTIONS['comorbidities'][0])
            if any(word in text_lower for word in ['hipertension', 'presion', 'tension']):
                comorbidities.append(OPTIONS['comorbidities'][1])
            if any(word in text_lower for word in ['epoc', 'pulmonar', 'pulmones']):
                comorbidities.append(OPTIONS['comorbidities'][2])
            if any(word in text_lower for word in ['cardiaca', 'corazon', 'cardiaco']):
                comorbidities.append(OPTIONS['comorbidities'][3])
            if any(word in text_lower for word in ['obesidad', 'sobrepeso', 'obeso']):
                comorbidities.append(OPTIONS['comorbidities'][4])
            if any(word in text_lower for word in ['inmuno', 'defensas', 'cancer']):
                comorbidities.append(OPTIONS['comorbidities'][5])
        
        return comorbidities

    def send_message(self, recipient, message):
        """Envía un mensaje a través de la API de WhatsApp"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messaging_product': 'whatsapp',
            'to': recipient,
            'type': 'text',
            'text': {
                'body': message
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            if response.status_code == 200:
                print(f"Message sent successfully to {recipient}")
            else:
                print(f"Failed to send message: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def send_long_message(self, recipient, message):
        """Divide y envía mensajes largos en múltiples partes"""
        # Dividir el mensaje en partes de máximo 1600 caracteres
        max_length = 1600
        parts = []
        
        while len(message) > max_length:
            # Buscar el último salto de línea antes del límite
            split_point = message.rfind('\n', 0, max_length)
            if split_point == -1:
                split_point = max_length
            
            parts.append(message[:split_point])
            message = message[split_point:].lstrip('\n')
        
        if message:
            parts.append(message)
        
        # Enviar cada parte con un pequeño delay
        for i, part in enumerate(parts):
            if i > 0:
                part = f"📄 Continuación ({i+1}/{len(parts)}):\n\n{part}"
            elif len(parts) > 1:
                part = f"📄 Mensaje largo (1/{len(parts)}):\n\n{part}"
            
            self.send_message(recipient, part)
            
            # Pequeño delay entre mensajes para evitar límites de tasa
            import time
            time.sleep(1)

