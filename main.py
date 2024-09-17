from config import TOKEN
import telebot 
import sys

sys.path.append("./censure")
from censure import Censor
censor_ru = Censor.get(lang="ru")

bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=['id'])
def send_welcome(message):
	bot.reply_to(message, f"Это {message.message_id} сообщение")

@bot.message_handler(content_types=['text'])
def delet_banword(message):

    def check_for_profanity(text):
          line_info = censor_ru.clean_line(text)
          _word = line_info[3][0] if line_info[1] else line_info[4][0] if line_info[2] else None
          return not _word is None, _word,line_info

    origenal_text = message.text

    check_result = check_for_profanity(message.text.lower())

    if check_result[0]:
          print(f"'{origenal_text}' написал это {message.chat.username}")
          bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(content_types=["sticker"])
def delet_all_sticer(message):
    print(f"стикер отправил {message.chat.username}")
    bot.delete_message(message.chat.id, message.message_id)

bot.polling(none_stop=True)