# Guía de Configuración WhatsApp Business API para COVI-ALERT

## Introducción

Esta guía te ayudará a configurar la integración de WhatsApp Business API con el chatbot COVI-ALERT paso a paso.

## Requisitos Previos

✅ Cuenta de Facebook Business  
✅ Número de teléfono dedicado (no registrado en WhatsApp personal)  
✅ Sitio web verificado  
✅ Servidor con dominio público (para webhooks)  

## Paso 1: Crear Aplicación en Meta for Developers

### 1.1 Acceder a Meta for Developers
1. Ve a [developers.facebook.com](https://developers.facebook.com)
2. Inicia sesión con tu cuenta de Facebook Business
3. Haz clic en "Mis Apps" → "Crear App"

### 1.2 Configurar la Aplicación
1. Selecciona "Empresa" como tipo de aplicación
2. Completa la información:
   - **Nombre de la app**: COVI-ALERT Bot
   - **Email de contacto**: tu-email@dominio.com
   - **Cuenta de Business**: Selecciona tu cuenta business

### 1.3 Agregar WhatsApp Business
1. En el dashboard de tu app, busca "WhatsApp"
2. Haz clic en "Configurar" en WhatsApp Business
3. Acepta los términos y condiciones

## Paso 2: Configurar WhatsApp Business Account (WABA)

### 2.1 Crear WABA
1. En la sección WhatsApp → "Introducción"
2. Haz clic en "Crear cuenta de WhatsApp Business"
3. Completa la información:
   - **Nombre de la cuenta**: COVI-ALERT
   - **Categoría**: Salud
   - **Descripción**: Asistente médico virtual COVID-19

### 2.2 Agregar Número de Teléfono
1. Ve a "Números de teléfono"
2. Haz clic en "Agregar número de teléfono"
3. Ingresa tu número dedicado
4. Verifica el número mediante SMS o llamada
5. **Importante**: Guarda el `PHONE_NUMBER_ID` que aparece

## Paso 3: Obtener Tokens de Acceso

### 3.1 Token de Acceso Temporal
1. Ve a "Introducción" en la sección WhatsApp
2. Copia el "Token de acceso temporal" (válido 24 horas)
3. **Guarda este token**: `WHATSAPP_ACCESS_TOKEN`

### 3.2 Token de Acceso Permanente
1. Ve a "Configuración" → "Básica"
2. Copia el "ID de la app" y "Clave secreta de la app"
3. Genera un token permanente usando la API:

```bash
curl -X GET "https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=TU_APP_ID&client_secret=TU_APP_SECRET"
```

### 3.3 Crear Token de Verificación
1. Crea un token personalizado (ej: `covi_alert_verify_2025`)
2. **Guarda este token**: `WHATSAPP_VERIFY_TOKEN`

## Paso 4: Configurar Webhook

### 4.1 Preparar tu Servidor
1. Asegúrate de que tu servidor esté ejecutando COVI-ALERT
2. Tu dominio debe ser accesible públicamente (HTTPS requerido)
3. El endpoint debe ser: `https://tu-dominio.com/webhook`

### 4.2 Configurar Webhook en Meta
1. Ve a WhatsApp → "Configuración"
2. En "Webhook", haz clic en "Configurar"
3. Completa:
   - **URL de callback**: `https://tu-dominio.com/webhook`
   - **Token de verificación**: Tu `WHATSAPP_VERIFY_TOKEN`
4. Haz clic en "Verificar y guardar"

### 4.3 Suscribirse a Eventos
1. En la misma sección de Webhook
2. Haz clic en "Administrar"
3. Suscríbete a:
   - ✅ `messages`
   - ✅ `message_deliveries` (opcional)
   - ✅ `message_reads` (opcional)

## Paso 5: Configurar Variables de Entorno

### 5.1 En tu Servidor
Crea un archivo `.env` o configura las variables:

```bash
# Tokens de WhatsApp
export WHATSAPP_ACCESS_TOKEN="EAAxxxxxxxxxxxxx"
export WHATSAPP_PHONE_NUMBER_ID="123456789012345"
export WHATSAPP_VERIFY_TOKEN="covi_alert_verify_2025"

# Configuración del servidor
export PORT="5000"
export DEBUG="False"
```

### 5.2 En el Código
El chatbot ya está configurado para leer estas variables automáticamente.

## Paso 6: Probar la Integración

### 6.1 Verificar Webhook
1. En Meta for Developers, ve a WhatsApp → "Configuración"
2. Verifica que el webhook muestre "✅ Conectado"
3. Si hay errores, revisa los logs de tu servidor

### 6.2 Enviar Mensaje de Prueba
1. Desde tu teléfono, envía un WhatsApp al número configurado
2. Escribe: "Hola"
3. Deberías recibir la respuesta de bienvenida de COVI-ALERT

### 6.3 Verificar Logs
```bash
# En tu servidor
tail -f logs/app.log

# O si usas systemd
journalctl -u covi-alert -f
```

## Paso 7: Configuración Avanzada

### 7.1 Plantillas de Mensajes (Opcional)
Para mensajes proactivos, necesitas crear plantillas:

1. Ve a WhatsApp → "Plantillas de mensajes"
2. Crea plantillas para:
   - Recordatorios de seguimiento
   - Alertas de salud
   - Confirmaciones de citas

### 7.2 Configurar Rate Limits
WhatsApp tiene límites de mensajes:
- **Nivel 1**: 1,000 conversaciones/24h
- **Nivel 2**: 10,000 conversaciones/24h
- **Nivel 3**: 100,000 conversaciones/24h

### 7.3 Monitoreo y Analytics
1. Ve a WhatsApp → "Analytics"
2. Configura alertas para:
   - Errores de webhook
   - Límites de tasa
   - Calidad de mensajes

## Solución de Problemas Comunes

### Error: "Webhook verification failed"
```bash
# Verificar que el VERIFY_TOKEN coincida
echo $WHATSAPP_VERIFY_TOKEN

# Verificar que el endpoint responda
curl "https://tu-dominio.com/webhook?hub.mode=subscribe&hub.verify_token=tu_token&hub.challenge=test"
```

### Error: "Invalid access token"
```bash
# Verificar token
curl -H "Authorization: Bearer $WHATSAPP_ACCESS_TOKEN" \
     "https://graph.facebook.com/v17.0/me"
```

### Error: "Phone number not found"
```bash
# Verificar PHONE_NUMBER_ID
curl -H "Authorization: Bearer $WHATSAPP_ACCESS_TOKEN" \
     "https://graph.facebook.com/v17.0/$WHATSAPP_PHONE_NUMBER_ID"
```

### Mensajes no se envían
1. Verificar que el número esté verificado
2. Revisar límites de tasa
3. Verificar formato del mensaje
4. Comprobar logs del servidor

## Mejores Prácticas

### Seguridad
- ✅ Usar HTTPS siempre
- ✅ Validar firmas de webhook
- ✅ Rotar tokens regularmente
- ✅ No exponer tokens en logs

### Performance
- ✅ Implementar rate limiting
- ✅ Usar conexiones persistentes
- ✅ Cachear respuestas comunes
- ✅ Monitorear latencia

### Compliance
- ✅ Respetar políticas de WhatsApp
- ✅ Obtener consentimiento de usuarios
- ✅ Implementar opt-out
- ✅ Proteger datos médicos

## Escalamiento

### Para Alto Volumen
1. **Load Balancer**: Distribuir carga entre servidores
2. **Base de Datos**: Migrar de memoria a PostgreSQL/MongoDB
3. **Queue System**: Usar Redis/RabbitMQ para mensajes
4. **Monitoring**: Implementar Prometheus/Grafana

### Múltiples Números
1. Configurar múltiples WABA
2. Implementar routing inteligente
3. Balancear carga por región/idioma

## Costos

### WhatsApp Business API
- **Conversaciones iniciadas por empresa**: $0.005 - $0.09 USD
- **Conversaciones iniciadas por usuario**: Gratis primeras 1,000/mes
- **Plantillas de mensajes**: Costo por envío

### Infraestructura
- **Servidor VPS**: $10-50 USD/mes
- **Dominio SSL**: $10-20 USD/año
- **Monitoreo**: $0-30 USD/mes

## Soporte

### Recursos Oficiales
- [Documentación WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Políticas de WhatsApp Business](https://www.whatsapp.com/legal/business-policy)
- [Soporte Meta for Developers](https://developers.facebook.com/support)

### Comunidad
- [WhatsApp Business API Community](https://www.facebook.com/groups/whatsappbusinessapi)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/whatsapp-business-api)

---

**¡Listo!** Tu chatbot COVI-ALERT ahora está integrado con WhatsApp Business API. Los usuarios pueden interactuar con él directamente desde WhatsApp.

**Próximos pasos recomendados:**
1. Probar con usuarios reales
2. Monitorear métricas de uso
3. Optimizar respuestas basado en feedback
4. Considerar expansión a otros idiomas

