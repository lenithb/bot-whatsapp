# 🤖 WhatsApp AI Bot — FastAPI + Groq + Twilio

Bot de WhatsApp con inteligencia artificial que recuerda el contexto de la conversación.

## Stack
- **FastAPI** — tu API en Python
- **Groq** — IA gratuita (LLaMA 3)
- **Twilio** — puente con WhatsApp

---

## 🚀 Paso a paso para correrlo

### 1. Obtener tu API Key de Groq (gratis)
1. Entrá a [console.groq.com](https://console.groq.com)
2. Creá una cuenta
3. Generá una API Key
4. Copiala

### 2. Configurar variables de entorno
```bash
cp .env.example .env
```
Editá el `.env` y completá:
- `GROQ_API_KEY` → la key que copiaste de Groq
- `API_KEY` → inventate una clave larga (ej: `mi-bot-secreto-2024`)

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Correr el servidor
```bash
uvicorn main:app --reload --port 8000
```
Tu API corre en `http://localhost:8000`

---

## 🌐 Publicar en Render (gratis)

1. Subí el proyecto a GitHub (sin el `.env`)
2. Entrá a [render.com](https://render.com) y creá una cuenta
3. **New → Web Service → conectá tu repo**
4. Configuración:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
5. En **Environment Variables** agregá `GROQ_API_KEY` y `API_KEY`
6. Deploy → Render te da una URL pública como `https://tu-bot.onrender.com`

---

## 📱 Conectar con Twilio WhatsApp

1. Creá cuenta en [twilio.com](https://twilio.com)
2. Activá el **WhatsApp Sandbox** (es gratis para probar)
3. En la configuración del Sandbox, en **"When a message comes in"** ponés:
   ```
   https://tu-bot.onrender.com/webhook
   ```
   Método: **POST**
4. Guardá

### Probar el Sandbox
Twilio te da un número de WhatsApp y una frase para unirte al sandbox (ej: `join bright-monkey`). La mandás desde tu WhatsApp y ya podés chatear con tu bot.

---

## 🔒 Seguridad

- Las claves están en variables de entorno, nunca en el código
- El endpoint `/history/{phone}` requiere el header `X-API-Key`
- El `.env` está en `.gitignore` para no subirse a GitHub

---

## 💬 Comandos disponibles en el chat

| Comando | Acción |
|---|---|
| `/reset` | Borra el historial de la conversación |
| `/limpiar` | Igual que /reset |
| `/nuevo` | Igual que /reset |

---

## 📁 Estructura del proyecto

```
whatsapp-bot/
├── main.py          # API principal y webhook de Twilio
├── conversation.py  # Manejo del historial por usuario
├── requirements.txt # Dependencias
├── .env.example     # Template de variables de entorno
├── .env             # Tu config real (NO subir a GitHub)
└── .gitignore
```

---

## 🧪 Probar la API localmente

```bash
# Ver que esté corriendo
curl http://localhost:8000/

# Simular un mensaje de WhatsApp (como lo haría Twilio)
curl -X POST http://localhost:8000/webhook \
  -d "Body=Hola, cómo estás?" \
  -d "From=whatsapp:+5493812345678"
```
# bot-whatsapp
