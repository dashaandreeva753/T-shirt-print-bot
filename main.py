import telebot
from telebot import types
import json

TOKEN = "7367185406:AAHsojbYXXLCAm0kVgO8WUVtd_g9wmgup_I"

bot = telebot.TeleBot(TOKEN)

user_data = {}


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Это бот для технической поддержки пользователей. Мы создаём принты"
                                      " для футболок. Для начала рекомендую ознакомиться с нашими командами и заполнить"
                                      " данные о себе. Удачных вам покупок!")


@bot.message_handler(commands=["recording_data"])
def handle_recording_data(message):
    user_data[message.chat.id] = {}
    msg = bot.send_message(message.chat.id, "Введите ваше имя: ")
    bot.register_next_step_handler(msg, get_name)


def get_name(message):
    user_data[message.chat.id]["name"] = message.text
    msg = bot.send_message(message.chat.id, "Ваше имя сохранено. Теперь введите ваш номер телефона: ")
    bot.register_next_step_handler(msg, callback=get_phone)


def get_phone(message):
    user_data[message.chat.id]["phone"] = message.text
    add_client(message, user_data[message.chat.id]["name"], user_data[message.chat.id]["phone"])
    bot.send_message(message.chat.id, f"Ваше имя {user_data[message.chat.id]['name']} сохранено. "
                     f"Ваш номер телефона {user_data[message.chat.id]['phone']} сохранён ")


def add_client(message, client_name, client_phone):
    try:
        # открытие файл и чтения
        with open("name.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"clients": [], "embroidery": [], "sizes": []}
        print("Файл не найден")

    # добавление новой записи в "clients"
    new_client = {"id": str(message.chat.id), "name": client_name, "phone": client_phone}

    for client in data["clients"]:
        if client.get("id") == str(message.chat.id):
            client["name"] = client_name
            client["phone"] = client_phone
            break
    else:
        data["clients"].append(new_client)

    # сохранения в файл json новые записи
    with open("name.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@bot.message_handler(commands=["complaint"])
def handle_complaint(message):
    user_data[message.chat.id] = {}
    msg = bot.send_message(message.chat.id, "Оставьте ваш отзыв")
    bot.register_next_step_handler(msg, get_complaint)


def get_complaint(message):
    user_data[message.chat.id]["complaint"] = message.text
    add_complaint(message, user_data[message.chat.id]["complaint"])
    bot.send_message(message.chat.id, "Спасибо за ваш отзыв, мы обязательно всё просмотрим")


def add_complaint(message, complaint):
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"clients": []}
        print("Файл не найден")

    new_client = {"id": str(message.chat.id), "complaint": complaint}
    data["clients"].append(new_client)

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@bot.message_handler(commands=["services"])
def handle_services(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "📌Стандартная печать: Печать на футболках методом шелкографии. "
                                      "Идеально подходит для больших тиражей.\n📌Цифровая печать: Позволяет печатать "
                                      "изображения высокого качества прямо на футболку. Отлично подходит для "
                                      "фотографий и детализированных изображений.\n📌Термотрансферная печать: "
                                      "Используется для печати на футболках из синтетических материалов. Идеальный "
                                      "вариант для спортивной формы.\n📌Прямая печать на ткани (DTG): Позволяет "
                                      "печатать непосредственно на футболке без предварительной подготовки. Отличается "
                                      "высокой стойкостью и качеством изображения.\n📌Вышивка: Добавьте ваш логотип или "
                                      "дизайн на футболку с помощью вышивки для дополнительного шарма и изысканности.")
    msg = bot.send_message(message.chat.id, "Выберите вид печати, который вам понравился 😊")
    bot.register_next_step_handler(msg, callback=get_embroidery)


def get_embroidery(message):
    user_data[message.chat.id]["embroidery"] = message.text
    add_embroidery(message, user_data[message.chat.id]["embroidery"])
    bot.send_message(message.chat.id, "Отличный выбор! Я уверен, что вам очень понравится!")


def add_embroidery(message, embroidery_text):
    try:
        # открытие файл и чтения
        with open("name.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"clients": [], "embroidery": [], "sizes": []}
        print("Файл не найден")

    # добавление новой записи в "embroidery"
    new_client = {"id": str(message.chat.id), "embroidery": embroidery_text}

    for client in data["embroidery"]:
        if client.get("id") == str(message.chat.id):
            client["embroidery"] = embroidery_text
            break
    else:
        data["clients"].append(new_client)

    # сохранения в файл json новые записи
    with open("name.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@bot.message_handler(commands=["sizes"])
def handle_sizes(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "📌XS: 88 см (обхват груди), 68 см (длина)\n📌S: 94 см (обхват груди), 70 см "
                                      "(длина)\n📌M: 100 см (обхват груди), 72 см (длина)\n📌L: 106 см (обхват груди), "
                                      "74 см (длина)\n📌XL: 112 см (обхват груди), 76 см (длина)\n📌XXL: 118 см "
                                      "(обхват груди), 78 см (длина)")
    msg = bot.send_message(message.chat.id, "Выберите размер, который вам подойдёт 📝")
    bot.register_next_step_handler(msg, get_sizes)


def get_sizes(message):
    user_data[message.chat.id]["sizes"] = message.text
    add_sizes(message, user_data[message.chat.id]["sizes"])
    bot.send_message(message.chat.id, f"Хорошо, ваш размер {user_data[message.chat.id]['sizes']} сохранён")


def add_sizes(message, sizes_text):
    try:
        with open("name.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"clients": [], "embroidery": [], "sizes": []}
        print("Файл не найден")

    new_client = {"id": str(message.chat.id), "sizes": sizes_text}

    for client in data["sizes"]:
        if client.get("id") == str(message.chat.id):
            client["sizes"] = sizes_text
            break
    else:
        data["sizes"].append(new_client)

    with open("name.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@bot.message_handler(commands=["questions"])
def handle_questions(message):
    keyboard = generate_questions()
    bot.send_message(message.chat.id, "Выберите вопрос: ", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    chat_id = call.message.chat.id

    if call.data.startswith("Как сделать"):
        bot.send_message(chat_id, "Чтобы сделать заказ, выберите услугу в разделе /services, определите подходящий "
                                  "размер в разделе /sizes и отправьте нам дизайн по почте example@gmail.com. Мы "
                                  "свяжемся с вами для подтверждения заказа.", reply_markup=generate_questions())
    elif call.data.startswith("Можно ли"):
        bot.send_message(chat_id, "Да, вы можете заказать печать с любым дизайном. Пожалуйста, убедитесь, что ваш "
                                  "дизайн соответствует нашим требованиям к качеству.",
                         reply_markup=generate_questions())
    elif call.data.startswith("Сколько времени"):
        bot.send_message(chat_id, "Стандартное время выполнения заказа — от 3 до 5 рабочих дней. Сроки могут "
                                  "варьироваться в зависимости от сложности и объёма заказа.",
                         reply_markup=generate_questions())
    elif call.data.startswith("Какие способы"):
        bot.send_message(chat_id, "Мы принимаем банковские карты, электронные переводы и наличные при получении.",
                         reply_markup=generate_questions())
    elif call.data.startswith("Есть ли"):
        bot.send_message(chat_id, "Да, в случае производственного брака или если финальный продукт значительно "
                                  "отличается от вашего дизайна, вы можете вернуть товар в течение 14 дней после "
                                  "получения.", reply_markup=generate_questions())


def generate_questions():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton(text="Как сделать заказ на печать футболки?", callback_data="Как сделать")
    button2 = types.InlineKeyboardButton(text="Можно ли заказать печать с собственным дизайном?",
                                         callback_data="Можно ли")
    button3 = types.InlineKeyboardButton(text="Сколько времени занимает выполнение заказа?",
                                         callback_data="Сколько времени")
    button4 = types.InlineKeyboardButton(text="Какие способы оплаты доступны?", callback_data="Какие способы")
    button5 = types.InlineKeyboardButton(text="Есть ли возможность возврата, если товар не подошёл?",
                                         callback_data="Есть ли")
    keyboard.add(button1, button2, button3, button4, button5)
    return keyboard


if __name__ == "__main__":
    bot.polling(non_stop=True)
