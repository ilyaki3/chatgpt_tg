import os

import openai
import telebot
from dotenv import load_dotenv
from openai import InvalidRequestError

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def hello(message: telebot.types.Message):
    bot.send_message(chat_id=message.from_user.id, text='Hello! I am GPTchat. Ask me whatever you want...')


@bot.message_handler(func=lambda _: True)
def handle_message(message: telebot.types.Message):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message.text,
            temperature=0.5,
            max_tokens=4000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
    except InvalidRequestError as request_err:
        print(request_err)
        bot.send_message(chat_id=message.from_user.id, text='Error: maximum request length is 4097 symbols')
    except Exception as ex:
        print(ex)

while True:
    try:
        bot.polling()
    except Exception as ex:
        print(ex)
