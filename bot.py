import threading
import time
import telebot
from datetime import datetime

from emigration_bot.api_keys import TG_TOKEN
from emigration_bot.gpt import get_response
from emigration_bot.question import Question
from emigration_bot.emigration_bot.user import User
from emigration_bot.db_connection import get_user_from_db, insert_user_info, update_user_info, insert_user_additional_questions
from prompt_generator import *
TO_MAIN  = "Повернутися на головну"
WAIT = "Оброблюю ваш запит, зачекайте...."

bot = telebot.TeleBot(TG_TOKEN)
questions_list_all  = [Question(0, "Перш ніж ми розпочнемо, чи бажаете надати деяку додаткову інформацію про Вас, для надання більш ревалентної інформації? (Стать, вік, рід діяльності)",
                                ["Так", "Ні"]),
                       Question(1,
                                "Ваша стать:",
                                ["Чоловіча", "Жіноча"]),
                       Question(2,
                                "Скільки вам років (введіть лише число, 25 наприклад):",
                                []),
                        Question(3,
                                "Напишіть види робіт у яких у вас є досвід:",
                                []),
                        Question(4,
                                "Чи маєте ви неповнолітніх дітей:",
                                ["Так", "Ні"]),
                       Question(5,
                                "Оберіть країну до якої ви емігрували.\nЯкщо її немає в списку напишіть мені в чат цю країну.",
                                ["Польща",  "Німеччина", "Чехія", "Італія", "Іспанія", "Туреччина", "Канада"]),
                        Question(6,
                                "Оберіть категорію за якою ви хочете отримати інформацію",
                                ["1.Юридичні питання", "2.Соціальна та медична допомога", "3.Фінансові питання та робота", "4.Житлові проблеми", "5.Інше"]),
                        Question(7,
                                "1.Найпоширеніші юридичні питання:",
                                ["1.1.Отримання візи та дозволу на проживання:",
                                 "1.2.Статус біженця або політичного притулку",
                                 "1.3.Питання, пов'язані з депортацією",
                                 "1.4.Законодавчі зміни"]),
                       Question(8,
                                "2.Соціальна та медична допомога:",
                                ["2.1.Інтеграція в нове суспільство",
                                 "2.2.Мовні бар'єри",
                                 "2.3.Доступ до освіти",
                                 "2.4.Доступ до медичних послуг"]),
                       Question(9,
                                "3.Фінансові питання та робота:",
                                ["3.1.Фінансова підтримка",
                                 "3.2.Банківські послуги",
                                 "3.3.Податкові обов'язки",
                                 "3.4.Працевлаштування"
                                 ]),
                       Question(10,
                                "4.Житлові проблеми",
                                ["4.1.Ореда житла",
                                 "4.2.Соціальне житло"]),
                        Question(11,
                                "Напишіть власне питання яке вас цікавить",
                                [])
                       ]



def generate_next_question(user, answer=None):
    user.previous_question = user.current_question
    if answer is not None:
        if int(answer.split('_')[1]) == -2:
            user.current_question = questions_list_all[6]
            if answer is not None and user.previous_question.id == 5:
                user.country = user.previous_question.answers[int(answer.split('_')[1])]

            markup = telebot.types.InlineKeyboardMarkup()
            for i in range(len(user.current_question.answers)):
                button = telebot.types.InlineKeyboardButton(text=user.current_question.answers[i],
                                                            callback_data=str(
                                                                user.current_question.id) + "_" + str(i))
                markup.add(button)
            send_message_to_user(user.id, user.current_question.question, markup)

    if user.current_question.id == 0:
        if int(answer.split('_')[1]) == 0:
            user.additional_info = True
            user.current_question = questions_list_all[1]
            markup = telebot.types.InlineKeyboardMarkup()
            for i in range(len(user.current_question.answers)):
                button = telebot.types.InlineKeyboardButton(text=user.current_question.answers[i],
                                                            callback_data=str(
                                                                user.current_question.id) + "_" + str(i))
                markup.add(button)
            send_message_to_user(user.id, user.current_question.question, markup)
        else:
            user.additional_info = False
            user.current_question = questions_list_all[5]
            bot.send_message(user.id, "Добре, тож розпочнемо")
            time.sleep(1.5)
            markup = telebot.types.InlineKeyboardMarkup()
            for i in range(len(user.current_question.answers)):
                button = telebot.types.InlineKeyboardButton(text=user.current_question.answers[i],
                                                            callback_data=str(
                                                                user.current_question.id) + "_" + str(i))
                markup.add(button)
            send_message_to_user(user.id, user.current_question.question, markup)
    elif user.current_question.id == 1:
        user.current_question = questions_list_all[2]
        if int(answer.split('_')[1]) == 0:
            user.gender = "M"
        else:
            user.gender = "W"
        send_message_to_user(user.id, user.current_question.question)

    elif user.current_question.id == 4:
        user.current_question = questions_list_all[5]
        bot.send_message(user.id, "Добре, тож розпочнемо")
        if int(answer.split('_')[1]) == 0:
            user.children = True

        markup = telebot.types.InlineKeyboardMarkup()
        for i in range(len(user.current_question.answers)):
            button = telebot.types.InlineKeyboardButton(text=user.current_question.answers[i],
                                                        callback_data=str(
                                                            user.current_question.id) + "_" + str(i))
            markup.add(button)
        send_message_to_user(user.id, user.current_question.question, markup, delay=1.5)

    elif user.current_question.id == 5:
        user.current_question = questions_list_all[6]
        if answer is not None:
            user.country = user.previous_question.answers[int(answer.split('_')[1])]

        markup = telebot.types.InlineKeyboardMarkup()
        for i in range(len(user.current_question.answers)):
            button = telebot.types.InlineKeyboardButton(text=user.current_question.answers[i],
                                                        callback_data=str(
                                                            user.current_question.id) + "_" + str(i))
            markup.add(button)
        send_message_to_user(user.id, user.current_question.question, markup, delay=1)

    elif user.current_question.id == 7:
        if int(answer.split('_')[1]) == 0:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user, "Напиши яким чином можна отримати візу та дозвіл на проживання. Які документи та дії для цього необхідні?"))
            send_response(user, response)
        elif int(answer.split('_')[1]) == 1:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "Опиши послідовність дій щоб отримати статус біженця або політичний притулок. Які документи та дії для цього необхідні"))
            send_response(user, response)
        elif int(answer.split('_')[1]) == 2:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "Опиши випадки в яких мене можуть депортувати з країни, та дії які можуть запобігти цьому."))
            send_response(user, response)
        elif int(answer.split('_')[1]) == 3:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "Опиши які зміни в законодавстві відбулися в останній час та стосуються емігрантів, та як це вплине на мене."))
            send_response(user, response)
    elif user.current_question.id == 8:
        if int(answer.split('_')[1]) == 0:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "Напиши які є варіанти соціальної інтеграції в нове суспільство, та який варіант може підійти саме для мене."))
            send_response(user, response)
        elif int(answer.split('_')[1]) == 1:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "Опиши як можна в найкоротші терміни подолати мовні бар'єри в незнайомій країні. Які соціальні програми наявні в цій країні?"))
            send_response(user, response)
        elif int(answer.split('_')[1]) == 2:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "Напиши чи є в цій країні можливіть емігрантам отримати доступ до освіти, отрмати нову спеціальність. Напиши які тут є програми то що потрібно зробити щоб ними скоритстатися.?"))
            send_response(user, response)
        elif int(answer.split('_')[1]) == 3:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "Як мені отримати доступ до медичних послуг? Опиши варіанти отримання медичних послуг в даній країні"))
            send_response(user, response)
    elif user.current_question.id == 9:
        if int(answer.split('_')[1]) == 0:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "Опиши які є наявні варіанти та програми в даній країні для отримання фінасової пдтримки для емігрантів. Та куди потрібно звертатися за такою допомогою, та які документи мати?"))
            send_response(user, response)
        elif int(answer.split('_')[1]) == 1:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "Як відкрити банківський рахунок в даній країні, які документи необхідно мати та скільки приблизно часу це займе?"))
            send_response(user, response)
        elif int(answer.split('_')[1]) == 2:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "знайди та напиши які податкові зобов'язання є на даний момент в цій країні для емігрантів, згідно чинного законодавства."))
            send_response(user, response)
        elif int(answer.split('_')[1]) == 3:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "Напиши які є варіанти для пошуку офіційної роботи в даній країні з та без знання місцевої мови?"))
            send_response(user, response)
    elif user.current_question.id == 10:
        if int(answer.split('_')[1]) == 0:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "Опиши процедуру оренди житла в даній країні, які є осбливості аренди, які документи необхідні, та де можна знайти аредодавців?"))
            send_response(user, response)
        elif int(answer.split('_')[1]) == 1:
            send_wait_message_in_thread(user)
            response = get_response(create_prompt(user,
                                                  "Чи є можливість в даній країні отримати соціальне житло, які документи необхідно мати та куди необхідно звертатися?"))
            send_response(user, response)

    elif user.current_question.id == 6:
        if answer is not None:
            choose_int = int(answer.split('_')[1])
            if choose_int == 0:
                user.current_question = questions_list_all[7]
                markup = telebot.types.InlineKeyboardMarkup()
                for i in range(len(user.current_question.answers)):
                    button = telebot.types.InlineKeyboardButton(text=user.current_question.answers[i],
                                                                callback_data=str(
                                                                    user.current_question.id) + "_" + str(i))
                    markup.add(button)
                markup.add(add_menu_button(user.current_question.id))
                bot.send_message(user.id, user.current_question.question, reply_markup=markup)
            elif choose_int == 1:
                user.current_question = questions_list_all[8]
                markup = telebot.types.InlineKeyboardMarkup()
                for i in range(len(user.current_question.answers)):
                    button = telebot.types.InlineKeyboardButton(text=user.current_question.answers[i],
                                                                callback_data=str(
                                                                    user.current_question.id) + "_" + str(i))
                    markup.add(button)
                markup.add(add_menu_button(user.current_question.id))
                bot.send_message(user.id, user.current_question.question, reply_markup=markup)
            elif choose_int == 2:
                user.current_question = questions_list_all[9]
                markup = telebot.types.InlineKeyboardMarkup()
                for i in range(len(user.current_question.answers)):
                    button = telebot.types.InlineKeyboardButton(text=user.current_question.answers[i],
                                                                callback_data=str(
                                                                    user.current_question.id) + "_" + str(i))
                    markup.add(button)
                markup.add(add_menu_button(user.current_question.id))
                bot.send_message(user.id, user.current_question.question, reply_markup=markup)
            elif choose_int == 3:
                user.current_question = questions_list_all[10]
                markup = telebot.types.InlineKeyboardMarkup()
                for i in range(len(user.current_question.answers)):
                    button = telebot.types.InlineKeyboardButton(text=user.current_question.answers[i],
                                                                callback_data=str(
                                                                    user.current_question.id) + "_" + str(i))
                    markup.add(button)
                markup.add(add_menu_button(user.current_question.id))
                bot.send_message(user.id, user.current_question.question, reply_markup=markup)
            elif choose_int == 4:
                user.current_question = questions_list_all[11]
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(add_menu_button(user.current_question.id))
                bot.send_message(user.id, user.current_question.question, reply_markup=markup)

    update_user_info(user)


def send_response(user, response):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(add_menu_button(user.current_question.id))
    send_message_to_user(user.id, response, delay=1)
    send_message_to_user(user.id, TO_MAIN, markup, delay=1)

def send_wait_message_in_thread(user):
    threading.Thread(target=send_message_to_user, args=(user.id, WAIT, None, 3,)).start()

def add_menu_button(current_question_id):
    return telebot.types.InlineKeyboardButton(text="🏠 Назад",
                                                callback_data=str(current_question_id) + "_" + str(-2))

@bot.message_handler(commands=['start'])
def send_start_question(message):
    current_user = get_user_from_db(message.chat.id)
    if current_user is  None:
        insert_user_info(current_user)
        current_user = get_user_from_db(message.chat.id)
    current_user = User(message.chat.id)

    dt_obj = datetime.fromtimestamp(message.date)

    mess= "Доброго ранку " if  4 <dt_obj.hour < 10 else "Доброго дня " if  10 <dt_obj.hour < 16  else "Добрий вечір "  if 22 <dt_obj.hour <4 else "Доброї ночі "

    bot.send_message(message.chat.id, mess + message.chat.first_name + ",\n" + "Вас вітає бот для підбору та пошуку інформаційного контенту для емігрантів.")
    current_user.current_question = questions_list_all[0]
    time.sleep(1)
    if current_user.current_question.answers:
        markup = telebot.types.InlineKeyboardMarkup()
        for i in range(len(current_user.current_question.answers)):
            button = telebot.types.InlineKeyboardButton(text=current_user.current_question.answers[i],
                                                        callback_data=str(current_user.current_question.id) + "_" + str(i))
            markup.add(button)
        bot.send_message(message.chat.id, current_user.current_question.question, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, current_user.current_question.question)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    bot.answer_callback_query(call.id, "✅")
    user_c = get_user_from_db(call.from_user.id)
    generate_next_question(user_c, call.data)


@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    user_c = get_user_from_db(message.chat.id)
    if user_c.current_question.id == 2:
        try:
            age = int(message.text)
            user_c.age = age
            user_c.previous_question = user_c.current_question
            user_c.current_question = questions_list_all[3]
            time.sleep(1)
            bot.send_message(user_c.id, user_c.current_question.question)
        except:
            bot.send_message(user_c.id, user_c.current_question.question)
    elif user_c.current_question.id == 3:
        profession = message.text if len(message.text) > 3 else None
        if profession is not None:
            user_c.profession = profession
        user_c.previous_question = user_c.current_question
        user_c.current_question = questions_list_all[4]
        time.sleep(1)
        markup = telebot.types.InlineKeyboardMarkup()
        for i in range(len(user_c.current_question.answers)):
            button = telebot.types.InlineKeyboardButton(text=user_c.current_question.answers[i],
                                                        callback_data=str(
                                                            user_c.current_question.id) + "_" + str(i))
            markup.add(button)
        bot.send_message(user_c.id, user_c.current_question.question, reply_markup=markup)
    elif user_c.current_question.id == 5:
            user_c.country = message.text
            time.sleep(1)
            generate_next_question(user_c, None)
            # user_c.previous_question = user_c.current_question
            # user_c.current_question = questions_list_all[6]
    elif user_c.current_question.id == 11:
        send_wait_message_in_thread(user_c)
        response = get_response(create_prompt(user_c, message.text))
        send_response(user_c, response)
        insert_user_additional_questions(user_c.id, message.text, response)



def send_message_to_user(user_id, text, markup=None, delay=0.0):
    time.sleep(delay)
    bot.send_message(user_id, text, reply_markup=markup)



bot.polling(none_stop=True)
