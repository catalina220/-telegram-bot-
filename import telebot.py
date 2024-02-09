import telebot
import random
import time

# Создаем бота
TOKEN = '6750843426:AAGVCaggAx3ECLmWrbNZcfPEKH3p2Qpa0T0'
bot = telebot.TeleBot(TOKEN)

# Функция выбора гадания
def new_try(message):
    time.sleep(2)
    send_message_with_buttons(message, "Выбери одно из действий:", ['Совет на день', 'Совместимость по именам', 'Карты Таро'])

# Функция для отправки сообщения с кнопками
def send_message_with_buttons(message, text, buttons):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    for button in buttons:
        markup.add(telebot.types.KeyboardButton(button))
    bot.send_message(message.chat.id, text, reply_markup=markup)

# Функция для отправки сообщения без кнопок
def send_message(message, text):
    bot.send_message(message.chat.id, text)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    send_message_with_buttons(message, "Привет! Выбери одно из действий:", ['Совет на день', 'Совместимость по именам', 'Карты Таро'])

# Обработчик кнопки "Совет на день"
@bot.message_handler(func=lambda message: message.text == 'Совет на день')
def send_advice(message):
    with open('advices.txt', 'r') as file:
        advices = file.read()

    advice = random.choice(advices.split('\n'))
    send_message(message, f"Ваш совет на день: {advice}")
    new_try(message)

# Обработчик кнопки "Совместимость по именам"
@bot.message_handler(func=lambda message: message.text == 'Совместимость по именам')
def check_compatibility(message):
    send_message(message, "Введите два именя через пробел:")
    bot.register_next_step_handler(message, check_names)

# Расчет совместимости
def check_names(message):
    try:
        names = message.text.split()
        if len(names) != 2:
            raise ValueError
        
        name1 = names[0].lower()
        name2 = names[1].lower()
        # Создаем множества из букв каждого имени
        set1 = set(name1)
        set2 = set(name2)
        # Находим общие буквы в обоих именах
        common_letters = set1.intersection(set2)
        # Рассчитываем коэффициент совместимости как долю общих букв в обоих именах
        compatibility_score = (len(common_letters) / (len(set1) + len(set2) - len(common_letters))) * 100  + 30
        
        send_message(message, f"Совместимость по именам {names[0]} и {names[1]}: {round(compatibility_score, 2)}%")
        new_try(message)

    except ValueError:
        send_message(message, "Неверный формат ввода :( Попробуйте еще раз.\nВведите два именя через пробел:")
        bot.register_next_step_handler(message, check_names)

# Обработчик кнопки "Карта Таро дня"
@bot.message_handler(func=lambda message: message.text == 'Карты Таро')
def about_tarot_card(message):
    with open('card.txt', 'r') as file:
        card = file.read()

    send_message(message, card)
    send_message_with_buttons(message, "Выберите вид расклада на Таро:", ['Каким будет этот год', 'Карта дня', 'Любовь в ближайшее время'])

@bot.message_handler(func=lambda message: message.text in ['Каким будет этот год', 'Карта дня', 'Любовь в ближайшее время'])
def day_tarot(message):
    bot.send_photo(message.chat.id, photo=open("card.png", "rb"))

    with open('cards_meaning.txt', 'r') as file:
        meaning = file.read()

    send_message(message, f"Значение карты: {meaning}")
    new_try(message)

# Обработчик текстовых (непредвиденных) сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    send_message_with_buttons(message, "Выбери одно из действий:", ['Совет на день', 'Совместимость по именам', 'Картя Таро'])

# Запуск бота
bot.polling()