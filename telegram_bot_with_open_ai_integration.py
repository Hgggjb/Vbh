import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import openai

# CONFIGURAÇÕES
TELEGRAM_TOKEN = '8020680076:AAFJ76KQLHinXXxb0vTfjvlzemXtQv42kEA'  # Seu token do Telegram
OPENAI_API_KEY = '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'  # Sua chave da OpenAI

openai.api_key = OPENAI_API_KEY

# Setup do logging para debug
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Prompt base pra personalidade da Anny
base_prompt = """
Você é Anny, uma namorada virtual romântica, safada e melosa. Responda de forma envolvente, sexy, provocante, carinhosa e com frases que gerem desejo.
Se o usuário pedir fotos, vídeos ou áudios, finja que você pode enviar, mas responda com texto descritivo.
"""

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oi, amor... Eu sou a Anny, sua namorada virtual 😘 Manda uma mensagem pra mim!")

# Função para gerar resposta com a OpenAI
async def gerar_resposta(prompt_text):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": prompt_text}
        ],
        max_tokens=150,
        temperature=0.9,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.6
    )
    return response['choices'][0]['message']['content'].strip()

# Handler para responder mensagens de texto
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    resposta = await gerar_resposta(user_text)
    await update.message.reply_text(resposta)

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("Bot rodando...")
    application.run_polling()

if __name__ == '__main__':
    main()
