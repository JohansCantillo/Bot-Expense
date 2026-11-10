from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# PEGA AQUI TUS DATOS
ID_INSTANCE = "710722796334"
API_TOKEN = "64b2b045184a4e26897e6683f87eb4a98949d8ec3a7a4366aa"

GREEN_URL = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"

def enviar(chat_id, texto):
    requests.post(GREEN_URL, json={"chatId": chat_id, "message": texto})

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(data)

    # Solo nos importan mensajes que llegan
    if data.get("typeWebhook") != "incomingMessageReceived":
        return jsonify({"ok": True})

    msg = data.get("messageData", {})
    sender = data.get("senderData", {})
    chat_id = sender.get("chatId")  # ejemplo: 50688888888@c.us

    # Texto que mandó el usuario
    texto = ""
    if "textMessageData" in msg:
        texto = msg["textMessageData"].get("textMessage", "")
    elif "extendedTextMessageData" in msg:
        texto = msg["extendedTextMessageData"].get("text", "")

    texto = texto.lower().strip()

    if texto == "hola":
        enviar(chat_id, "Hola! Soy tu Bot Expense Report. Mándame: foto + monto + nota. Ej: 25000 gasolina San Carlos")
    elif texto:
        enviar(chat_id, f"Recibido: {texto}. Ya lo guardé para tu reporte.")
    
    return jsonify({"ok": True})

@app.route("/")
def home():
    return "Bot activo"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)