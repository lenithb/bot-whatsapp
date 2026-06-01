from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq
import os
from dotenv import load_dotenv
from conversation import get_history, save_message, clear_history

load_dotenv()

app = FastAPI(title="WhatsApp AI Bot")

# Clientes
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── Seguridad: API Key propia ──────────────────────────────────────────────────
API_KEY = os.getenv("API_KEY")

def verify_api_key(request: Request):
    """Valida la API Key en el header para endpoints protegidos."""
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")

# ── Endpoint de salud ──────────────────────────────────────────────────────────
@app.get("/")
def health():
    return {"status": "ok", "bot": "WhatsApp AI Bot activo 🤖"}

# ── Webhook de Twilio (WhatsApp) ───────────────────────────────────────────────
@app.post("/webhook", response_class=PlainTextResponse)
async def webhook(request: Request):
    """
    Twilio manda aquí cada mensaje de WhatsApp.
    Respondemos con TwiML (XML que Twilio entiende).
    """
    form = await request.form()
    incoming_msg = form.get("Body", "").strip()
    sender = form.get("From", "")      # Ej: "whatsapp:+5493812345678"

    if not incoming_msg:
        return PlainTextResponse(str(resp), media_type="text/xml")

    # Comando especial: borrar historial
    if incoming_msg.lower() in ["/reset", "/limpiar", "/nuevo"]:
        clear_history(sender)
        resp = MessagingResponse()
        resp.message("✅ Historial borrado. ¡Empecemos de nuevo!")
        return PlainTextResponse(str(resp), media_type="text/xml")

    # Obtener historial de conversación
    history = get_history(sender)

    # Llamar a Groq con el historial completo
    history.append({"role": "user", "content": incoming_msg})

    completion = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente útil y amigable que responde por WhatsApp. "
                    "Tus respuestas son concisas (máximo 3 párrafos), claras y en el mismo idioma del usuario. "
                    "Usás emojis con moderación para ser más expresivo."
                )
            },
            *history
        ],
        max_tokens=512,
    )

    ai_reply = completion.choices[0].message.content

    # Guardar en historial
    save_message(sender, "user", incoming_msg)
    save_message(sender, "assistant", ai_reply)

    # Responder a Twilio
    resp = MessagingResponse()
    resp.message(ai_reply)
    return PlainTextResponse(str(resp), media_type="text/xml")

# ── Endpoint protegido: limpiar historial manualmente ───────────_──────────────
@app.delete("/history/{phone}", dependencies=[Depends(verify_api_key)])
def delete_history(phone: str):
    """Borra el historial de un número. Requiere X-API-Key header."""
    clear_history(f"whatsapp:{phone}")
    return {"message": f"Historial de {phone} borrado"}
