import telebot
import datetime
import time
import threading

# Получите ваш токен от BotFather и вставьте его сюда
API_TOKEN = 'введите токен'
bot = telebot.TeleBot(API_TOKEN)

# Список чатов для рассылки уведомлений
chats = []


# Функция для напоминания пить воду
def reminder():
    while True:
        # Задержка на 3 часа (3 * 60 * 60 секунд)
        time.sleep(3 * 60 * 60)

        # Отправляем напоминание всем пользователям
        for chat_id in chats:
            bot.send_message(chat_id, "Напоминаю: Пей воду! 💧")


# Хендлер команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Добавляем чат в список для получения уведомлений
    if message.chat.id not in chats:
        chats.append(message.chat.id)

    bot.reply_to(message, "Привет! Я напомню тебе пить воду каждые 3 часа. 💧")


# Хендлер команды /time, который покажет текущее время
@bot.message_handler(commands=['time'])
def send_time(message):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    bot.reply_to(message, f"Текущее время: {current_time}")


# Хендлер команды /delay, который выполнит задержку перед ответом
@bot.message_handler(commands=['delay'])
def send_delay(message):
    bot.reply_to(message, "Я подожду немного...")

    def delayed_response():
        time.sleep(5)
        bot.send_message(message.chat.id, "Вот и ответ спустя 5 секунд!")

    threading.Thread(target=delayed_response).start()


# Хендлер на все текстовые сообщения
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Ты написал: {message.text}")


# Запуск потока напоминаний
threading.Thread(target=reminder, daemon=True).start()

# Запуск бота
bot.polling(none_stop=True)
