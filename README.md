# COVI-ALERT - Chatbot COVID-19 🦠🔍

## Descripción

COVI-ALERT es un asistente médico virtual especializado en triaje temprano de COVID-19 con capacidad predictiva. Evalúa riesgo de infección, predice probabilidad de hospitalización, deriva casos críticos y educa en prevención.

## Características Principales

✅ **Evaluación de Riesgo COVID-19**
- Algoritmo basado en síntomas, edad y comorbilidades
- Clasificación en 3 niveles: Crítico, Moderado, Bajo
- Recomendaciones personalizadas

✅ **Interfaz Dual**
- **Interfaz Web**: Moderna y responsiva
- **WhatsApp Business API**: Integración completa

✅ **Consejos Personalizados**
- Cuidados específicos por síntoma
- Recomendaciones según edad y condiciones
- Guía completa de cuidados en casa

✅ **Funcionalidades Avanzadas**
- Procesamiento inteligente de texto
- Manejo de mensajes largos
- Sistema de acciones rápidas
- Señales de alarma médica

## Instalación y Configuración

### Requisitos Previos

- Python 3.11+
- Cuenta de WhatsApp Business API (opcional)
- Servidor web con acceso público (para webhooks)

### Instalación Local

1. **Extraer el proyecto**
```bash
unzip whatsapp_covi_alert.zip
cd whatsapp_covi_alert
```

2. **Activar entorno virtual**
```bash
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar el servidor**
```bash
python src/main.py
```

5. **Acceder a la interfaz**
- Web: http://localhost:5000
- API: http://localhost:5000/api/info

### Configuración de WhatsApp Business API

#### Paso 1: Obtener Credenciales

1. Crear una aplicación en [Meta for Developers](https://developers.facebook.com/)
2. Agregar el producto "WhatsApp Business API"
3. Obtener:
   - `ACCESS_TOKEN`: Token de acceso
   - `PHONE_NUMBER_ID`: ID del número de teléfono
   - `VERIFY_TOKEN`: Token de verificación (crear uno personalizado)

#### Paso 2: Configurar Variables de Entorno

```bash
export WHATSAPP_ACCESS_TOKEN="tu_access_token_aqui"
export WHATSAPP_PHONE_NUMBER_ID="tu_phone_number_id_aqui"
export WHATSAPP_VERIFY_TOKEN="tu_verify_token_aqui"
```

O crear un archivo `.env`:
```
WHATSAPP_ACCESS_TOKEN=tu_access_token_aqui
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id_aqui
WHATSAPP_VERIFY_TOKEN=tu_verify_token_aqui
```

#### Paso 3: Configurar Webhook

1. En la configuración de WhatsApp en Meta for Developers
2. Configurar Webhook URL: `https://tu-dominio.com/webhook`
3. Usar el `VERIFY_TOKEN` que configuraste
4. Suscribirse a eventos: `messages`

#### Paso 4: Probar la Integración

1. Enviar un mensaje de prueba desde WhatsApp
2. Verificar logs del servidor
3. Confirmar respuestas del chatbot

## Estructura del Proyecto

```
whatsapp_covi_alert/
├── src/
│   ├── main.py                 # Servidor Flask principal
│   ├── whatsapp_handler.py     # Manejador de WhatsApp
│   ├── chatbot.py             # Lógica del chatbot original
│   ├── risk_assessment.py     # Algoritmo de evaluación de riesgos
│   ├── api_integrations.py    # Consejos personalizados y APIs
│   ├── utils.py               # Utilidades y validaciones
│   ├── config.py              # Configuración y mensajes
│   └── static/
│       └── index.html         # Interfaz web
├── venv/                      # Entorno virtual
├── requirements.txt           # Dependencias
└── README.md                  # Este archivo
```

## Endpoints Disponibles

### Interfaz Web
- `GET /` - Interfaz web del chatbot
- `POST /api/chat` - API para chat web
- `GET /api/info` - Información del chatbot

### WhatsApp Business API
- `GET /webhook` - Verificación de webhook
- `POST /webhook` - Recepción de mensajes

### Utilidades
- `GET /health` - Estado del servidor

## Uso del Chatbot

### Flujo de Conversación

1. **Bienvenida**: Presentación y opciones iniciales
2. **Edad**: Solicitud de edad del usuario
3. **Síntomas**: Selección de síntomas actuales
4. **Comorbilidades**: Condiciones médicas preexistentes
5. **Exposición**: Contacto con casos COVID-19
6. **Evaluación**: Análisis de riesgo y recomendaciones
7. **Opciones**: Consejos, hospitales, nueva evaluación

### Comandos Especiales

- `ayuda` / `help` - Mostrar menú de ayuda
- `empezar` / `reiniciar` - Nueva evaluación
- `1,2,3` - Selección múltiple de opciones

## Personalización

### Modificar Mensajes

Editar `src/config.py`:
```python
MESSAGES = {
    "welcome": "Tu mensaje personalizado...",
    # ... otros mensajes
}
```

### Agregar Nuevos Síntomas

En `src/config.py`:
```python
OPTIONS = {
    "symptoms": [
        "Nuevo síntoma (🔥)",
        # ... otros síntomas
    ]
}
```

### Personalizar Algoritmo de Riesgo

Modificar `src/risk_assessment.py`:
```python
def evaluate_risk(user_data):
    # Tu lógica personalizada
    pass
```

## Despliegue en Producción

### Opción 1: Servidor VPS

1. **Configurar servidor**
```bash
sudo apt update
sudo apt install python3 python3-pip nginx
```

2. **Clonar proyecto**
```bash
git clone tu-repositorio
cd whatsapp_covi_alert
```

3. **Configurar Nginx**
```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

4. **Usar Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

### Opción 2: Heroku

1. **Crear Procfile**
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT src.main:app
```

2. **Configurar variables de entorno en Heroku**
```bash
heroku config:set WHATSAPP_ACCESS_TOKEN=tu_token
heroku config:set WHATSAPP_PHONE_NUMBER_ID=tu_id
heroku config:set WHATSAPP_VERIFY_TOKEN=tu_verify_token
```

### Opción 3: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 5000

CMD ["python", "src/main.py"]
```

## Monitoreo y Logs

### Logs del Servidor
```bash
tail -f logs/app.log
```

### Métricas de WhatsApp
- Mensajes enviados/recibidos
- Tiempo de respuesta
- Errores de API

### Salud del Sistema
```bash
curl http://localhost:5000/health
```

## Solución de Problemas

### Error: "Module not found"
```bash
# Verificar entorno virtual
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Webhook verification failed"
```bash
# Verificar VERIFY_TOKEN
echo $WHATSAPP_VERIFY_TOKEN
```

### Error: "Failed to send message"
```bash
# Verificar ACCESS_TOKEN y permisos
curl -H "Authorization: Bearer $WHATSAPP_ACCESS_TOKEN" \
     https://graph.facebook.com/v17.0/me
```

## Limitaciones y Consideraciones

⚠️ **Importante**: Este chatbot es una herramienta de apoyo y NO sustituye el diagnóstico médico profesional.

### Limitaciones Técnicas
- Almacenamiento en memoria (no persistente)
- Sin autenticación de usuarios
- Límites de tasa de WhatsApp API

### Consideraciones Médicas
- Basado en síntomas autoreportados
- No incluye exámenes físicos
- Requiere validación médica

## Soporte y Contribuciones

### Reportar Problemas
- Crear issue en el repositorio
- Incluir logs y pasos para reproducir

### Contribuir
1. Fork del repositorio
2. Crear rama feature
3. Commit cambios
4. Pull request

## Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para detalles.

## Contacto

- **Desarrollado por**: Manus AI
- **Fecha**: Junio 2025
- **Versión**: 2.0

---

**Disclaimer Médico**: Esta herramienta es solo para fines informativos y educativos. No debe usarse como sustituto del consejo, diagnóstico o tratamiento médico profesional. Siempre consulte a un profesional de la salud calificado para cualquier pregunta sobre una condición médica.

