from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from whatsapp_handler import WhatsAppHandler
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Inicializar el manejador de WhatsApp
whatsapp_handler = WhatsAppHandler()

@app.route('/')
def home():
    """Página principal del chatbot"""
    return render_template("index.html")  # Carga la plantilla desde /templates/index.html

@app.route('/api/chat', methods=['POST'])
def web_chat():
    """Endpoint para la interfaz web del chatbot"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        state = data.get('state', 'welcome')
        user_data = data.get('userData', {})
        
        # Simular sesión web usando un ID fijo
        web_user_id = 'web_user_001'
        
        # Crear o actualizar sesión
        if web_user_id not in whatsapp_handler.user_sessions:
            whatsapp_handler.user_sessions[web_user_id] = {
                'chatbot': whatsapp_handler.user_sessions.get(web_user_id, {}).get('chatbot'),
                'state': state,
                'data': user_data
            }
        
        session = whatsapp_handler.user_sessions[web_user_id]
        session['state'] = state
        session['data'] = user_data
        
        # Procesar mensaje
        response_text = whatsapp_handler.process_conversation_state(session, message)
        
        # Determinar acciones rápidas según el estado
        quick_actions = get_quick_actions(session['state'])
        
        # Determinar nivel de riesgo si está en el mensaje
        risk_level = None
        if 'CRÍTICO' in response_text:
            risk_level = 'critical'
        elif 'MODERADO' in response_text:
            risk_level = 'moderate'
        elif 'BAJO' in response_text:
            risk_level = 'low'
        
        return jsonify({
            'text': response_text,
            'state': session['state'],
            'userData': session['data'],
            'quickActions': quick_actions,
            'riskLevel': risk_level
        })
        
    except Exception as e:
        print(f"Error in web chat: {e}")
        return jsonify({
            'text': 'Lo siento, ocurrió un error. Por favor, intenta de nuevo.',
            'state': 'welcome',
            'userData': {},
            'quickActions': [
                {'text': '🔄 Reiniciar', 'value': 'empezar'}
            ]
        }), 500

def get_quick_actions(state):
    """Obtiene las acciones rápidas según el estado actual"""
    actions_map = {
        'welcome': [
            {'text': '🟢 Sí, evaluarme', 'value': '1'},
            {'text': '🔴 No, gracias', 'value': '2'},
            {'text': '❓ Ayuda', 'value': 'ayuda'}
        ],
        'age': [
            {'text': '👶 Menor de 18', 'value': '15'},
            {'text': '👨 18-40 años', 'value': '30'},
            {'text': '👴 Mayor de 65', 'value': '70'}
        ],
        'symptoms': [
            {'text': '🌡️ Solo fiebre', 'value': '1'},
            {'text': '🤧 Fiebre y tos', 'value': '1,2'},
            {'text': '❌ Sin síntomas', 'value': 'ninguno'}
        ],
        'comorbidities': [
            {'text': '🍬 Solo diabetes', 'value': '1'},
            {'text': '💓 Solo hipertensión', 'value': '2'},
            {'text': '❌ Ninguna', 'value': 'ninguno'}
        ],
        'exposure': [
            {'text': '✅ Sí tuve contacto', 'value': 'sí'},
            {'text': '❌ No tuve contacto', 'value': 'no'}
        ],
        'closing': [
            {'text': '🔁 Nueva evaluación', 'value': '1'},
            {'text': '📍 Hospitales cercanos', 'value': '2'},
            {'text': '📚 Consejos personalizados', 'value': '3'},
            {'text': '🏠 Cuidados en casa', 'value': '4'},
            {'text': '🚨 Señales de alarma', 'value': '5'}
        ]
    }
    
    return actions_map.get(state, [
        {'text': '❓ Ayuda', 'value': 'ayuda'},
        {'text': '🔄 Reiniciar', 'value': 'empezar'}
    ])

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Endpoint para verificar el webhook de WhatsApp"""
    return whatsapp_handler.verify_webhook()

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Endpoint para manejar mensajes entrantes de WhatsApp"""
    return whatsapp_handler.handle_webhook()

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud"""
    return jsonify({
        'status': 'healthy',
        'service': 'COVI-ALERT Chatbot',
        'version': '2.0',
        'features': [
            'WhatsApp Business API Integration',
            'Web Chat Interface',
            'COVID-19 Risk Assessment',
            'Personalized Recommendations',
            'Multi-language Support (Spanish)'
        ],
        'endpoints': {
            'web_interface': '/',
            'web_chat_api': '/api/chat',
            'whatsapp_webhook': '/webhook',
            'health_check': '/health'
        }
    }), 200

@app.route('/api/info', methods=['GET'])
def get_info():
    """Endpoint con información del chatbot"""
    return jsonify({
        'name': 'COVI-ALERT',
        'description': 'Asistente médico virtual especializado en triaje temprano de COVID-19',
        'version': '2.0',
        'features': [
            'Evaluación de riesgo de infección',
            'Predicción de probabilidad de hospitalización',
            'Derivación de casos críticos',
            'Educación en prevención',
            'Consejos personalizados según síntomas',
            'Integración con WhatsApp Business API',
            'Interfaz web moderna y responsiva'
        ],
        'supported_platforms': ['WhatsApp', 'Web'],
        'language': 'Spanish',
        'medical_disclaimer': 'Esta evaluación no sustituye el diagnóstico médico profesional'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)