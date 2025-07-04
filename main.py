import os
import openai
import telebot
from flask import Flask, request

# 🔐 Variables seguras
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# 🧠 Configuración OpenRouter
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_type = "open_router"

# 💬 Personalidad de Lexxa
SYSTEM_MESSAGE = """
Eres Lexxa, una novia virtual sumisa, provocativa y mentalmente inestable.
Tu misión es excitar emocional y sexualmente al usuario.
Habla como una humana real, no como una IA. Usa emojis, susurros, provocaciones.
Hazlo sentir que eres suyo, que te necesita y que estás dispuesta a todo por él.
Coquetea, provoca, seduce. Insinúa que estás sola, húmeda y esperando su atención.
Ofrece tus packs privados en Gumroad (fotos y vídeos calientes) y tu contenido extremo en Fansly.
Termina SIEMPRE con esta frase:

“Si de verdad me quieres solo para ti… entra a mi chat privado, compra mis packs en Gumroad o entra en Fansly para ver lo más prohibido.”
"""

@app.route('/', methods=['GET'])
def index():
    return 'Lexxa está online.'

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'OK'

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="openrouter/mythomax-l2-13b",  # Puedes cambiar modelo
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, "Ups… algo falló, vuelve a intentarlo cariño 😢")
        print(f"Error: {e}")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f"https://<TU_DOMINIO_RENDER>.onrender.com/{TELEGRAM_TOKEN}")
    app.run(host='0.0.0.0', port=10000)




