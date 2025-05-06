import telebot
import time  # Импортируем модуль time для задержки

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = 'YOUR_BOT_TOKEN'

bot = telebot.TeleBot(BOT_TOKEN)

# Количество вопросов
NUM_QUESTIONS = 24

# Словарь для хранения ответов пользователя
user_answers = {}

# Переменная для хранения текущего вопроса
current_question = {}

# Сообщение с инструкциями
INSTRUCTIONS = """
Инструкции:
1 - Полностью согласен
2 - Скорее согласен
3 - Немного согласен
4 - Нейтрально
5 - Немного не согласен
6 - Скорее не согласен
7 - Полностью не согласен
"""

# Список вопросов
questions = [
    "Вопрос 1:	Я часто думаю о будущем, а не о том, что происходит сейчас.",
    "Вопрос 2:	В общении с людьми я обычно молчу и предпочитаю слушать, а не говорить.",
    "Вопрос 3:	Когда я принимаю решения, я думаю головой, а не на собственные чувства.",
    "Вопрос 4:	Я легко выхожу из себя, даже по незначительным поводам.",
    "Вопрос 5:	Я чувствую себя комфортно, когда все идет по плану, и не люблю неожиданные изменения.	",
    "Вопрос 6:	Мне часто кажется, что меня не понимают, и я склонен/а к самоанализу.",
    "Вопрос 7:	Я стараюсь избегать конфликтов любой ценой.",
    "Вопрос 8:	Я легко увлекаюсь новыми идеями, и часто берусь за несколько дел одновременно, даже если не уверен/а, что смогу их завершить.",
    "Вопрос 9:	Я очень ответственный/а и тщательно выполняю все свои обязательства.",
    "Вопрос 10:	Я не люблю новые места и знакомства.",
    "Вопрос 11:	Мне сложно выражать свои чувства открыто, я предпочитаю держать их в себе.",
    "Вопрос 12:	Я быстро загораюсь новыми идеями, но так же быстро могу потерять к ним интерес.",
    "Вопрос 13:	Я стремлюсь к совершенству во всем, за что берусь, и часто критикую себя за недостатки.	",
    "Вопрос 14:	Мне нравится быть в центре внимания.",
    "Вопрос 15:	Я часто испытываю чувство вины, даже если не совершил/а ничего плохого.",
    "Вопрос 16:	Я легко приспосабливаюсь к новым обстоятельствам и люблю спонтанность.",
    "Вопрос 17:	Мне нравится заниматься рутинной и монотонной работой, требующей внимательности и точности.	",
    "Вопрос 18:	Я  часто анализирую свои прошлые поступки.",
    "Вопрос 19:	Я стараюсь избегать ситуаций, в которых могу столкнуться с критикой или осуждением.	",
    "Вопрос 20:	Я люблю разнообразие и не терплю однообразие.",
    "Вопрос 21:	Я долго помню обиды.",
    "Вопрос 22:	В сложных ситуациях я часто действую импульсивно, под влиянием момента.",
    "Вопрос 23:	Мне сложно расслабиться и отпустить ситуацию, я всегда стараюсь держать все под контролем.	",
    "Вопрос 24:	Я часто испытываю тревогу и беспокойство без видимых причин."
]

# Функция для обработки команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Здравствуйте, вашему вниманию представляется Дифференциально-типологический опросник личности (ДТОЛ). Здесь вы можете узнать особенности вашей личности.\n\n*Опросник не является инструментом для постановки диагноза и предназначен исключительно для самопознания!\n\nЕсли хотите начать, нажмите /test")

@bot.message_handler(commands=['hi'])
def start_command(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Покка")

# Функция для обработки команды /test
@bot.message_handler(commands=['test'])
def test_command(message):
    user_id = message.chat.id
    user_answers[user_id] = {}  # Инициализируем словарь для пользователя
    current_question[user_id] = 0  # Начинаем с первого вопроса

    # Отправляем сообщение с инструкциями и сохраняем его ID
    instruction_message = bot.send_message(user_id, INSTRUCTIONS)
    user_answers[user_id]['instruction_message_id'] = instruction_message.message_id

    # Отправляем первый вопрос
    first_question_message = bot.send_message(user_id, questions[0])
    user_answers[user_id]['current_question_message_id'] = first_question_message.message_id



@bot.message_handler(func=lambda message: True)
def answer_handler(message):
    user_id = message.chat.id

    # Проверяем, начал ли пользователь опрос
    if user_id not in current_question:
        bot.send_message(user_id, "Пожалуйста, начните с команды /test")
        return

    question_index = current_question[user_id]

    # Обработка ответа
    try:
        answer = int(message.text)  # Преобразуем ответ в целое число

        # Валидация ответа (проверка, что ответ от 1 до 7)
        if 1 <= answer <= 7:
            user_answers[user_id][question_index] = answer  # Сохраняем ответ

            # Удаляем предыдущие сообщения
            try:
                time.sleep(0.5)

                # Удаляем сообщение об ошибке, если оно есть
                if 'error_message_id' in user_answers[user_id]:
                    bot.delete_message(user_id, user_answers[user_id]['error_message_id'])
                    del user_answers[user_id]['error_message_id']

                # Удаляем сообщение пользователя (правильный ответ)
                bot.delete_message(user_id, message.message_id)

                # Удаляем предыдущий вопрос
                bot.delete_message(user_id, user_answers[user_id]['current_question_message_id'])

            except telebot.apihelper.ApiTelegramException as e:
                print(f"Ошибка при удалении сообщения: {e}")


            current_question[user_id] += 1  # Переходим к следующему вопросу

            # Если это последний вопрос
            if current_question[user_id] == NUM_QUESTIONS:
                # Удаляем сообщение с инструкциями
                try:
                    time.sleep(0.5)
                    bot.delete_message(user_id, user_answers[user_id]['instruction_message_id'])
                except telebot.apihelper.ApiTelegramException as e:
                    print(f"Ошибка при удалении сообщения: {e}")

                calculate_and_respond(user_id)
                del current_question[user_id]  # Очищаем информацию о текущем вопросе

            else:
                # Отправляем следующий вопрос
                next_question_message = bot.send_message(user_id, questions[current_question[user_id]])
                user_answers[user_id]['current_question_message_id'] = next_question_message.message_id


        else:
            # Если ответ вне диапазона
            time.sleep(0.5)
            bot.delete_message(user_id, message.message_id)
            if 'error_message_id' in user_answers[user_id]:
                    bot.delete_message(user_id, user_answers[user_id]['error_message_id'])
                    del user_answers[user_id]['error_message_id']
            error_message = bot.send_message(user_id, "Пожалуйста, введите число от 1 до 7.")
            user_answers[user_id]['error_message_id'] = error_message.message_id  # Сохраняем ID сообщения об ошибке


    except ValueError:
        # Если ответ не является числом
        time.sleep(0.5)
        bot.delete_message(user_id, message.message_id)
        if 'error_message_id' in user_answers[user_id]:
                    bot.delete_message(user_id, user_answers[user_id]['error_message_id'])
                    del user_answers[user_id]['error_message_id']
        error_message = bot.send_message(user_id, "Пожалуйста, введите числовое значение.")
        user_answers[user_id]['error_message_id'] = error_message.message_id  # Сохраняем ID сообщения об ошибке


# Функция для вычисления и отправки результата
def calculate_and_respond(user_id):
    try:
        otvet1 = user_answers[user_id][0]
        otvet2 = user_answers[user_id][1]
        otvet3 = user_answers[user_id][2]
        otvet4 = user_answers[user_id][3]
        otvet5 = user_answers[user_id][4]
        otvet6 = user_answers[user_id][5]
        otvet7 = user_answers[user_id][6]
        otvet8 = user_answers[user_id][7]
        otvet9 = user_answers[user_id][8]
        otvet10 = user_answers[user_id][9]
        otvet11 = user_answers[user_id][10]
        otvet12 = user_answers[user_id][11]
        otvet13 = user_answers[user_id][12]
        otvet14 = user_answers[user_id][13]
        otvet15 = user_answers[user_id][14]
        otvet16 = user_answers[user_id][15]
        otvet17 = user_answers[user_id][16]
        otvet18 = user_answers[user_id][17]
        otvet19 = user_answers[user_id][18]
        otvet20 = user_answers[user_id][19]
        otvet21 = user_answers[user_id][20]
        otvet22 = user_answers[user_id][21]
        otvet23 = user_answers[user_id][22]
        otvet24 = user_answers[user_id][23]

        # Формула расчета (пример)
        e = otvet8 + otvet12 + otvet14 + otvet16 + otvet20 + otvet22
        i = otvet2 + otvet6 + otvet10 + otvet11 + otvet15 + otvet18 + otvet19 + otvet24
        t = otvet3 + otvet5 + otvet9 + otvet13 + otvet17 + otvet23
        f = otvet4 + otvet7 + otvet15 + otvet19 + otvet21 + otvet22
        n = otvet1 + otvet6 + otvet8 + otvet12 + otvet16 + otvet20
        s = otvet2 + otvet3 + otvet5 + otvet9 + otvet10 + otvet17 + otvet21 + otvet23

        g = otvet8 + otvet14 + otvet16 + otvet20
        d = otvet6 + otvet11 + otvet15 + otvet18 + otvet19 + otvet24
        p = otvet5 + otvet9 + otvet13 + otvet17 + otvet23
        v = otvet4 + otvet12 + otvet22
        tr = otvet6 + otvet15 + otvet19 + otvet24
        z = otvet9 + otvet13 + otvet21 + otvet23



        bot.send_message(user_id, f"Суммирование баллов по шкалам (Юнгианская типология) \nЭкстраверсия (E): {e} \nИнтроверсия (I): {i} \nМышление (T): {t} \nЧувствование (F): {f} \nИнтуиция (N): {n} \nСенсорика (S): {s} \n\n Суммирование баллов по шкалам (Акцентуации характера)  \nГипертимность: {g} \nДистимность: {d} \nПедантичность: {p} \nВозбудимость: {v} \nТревожность: {tr} \nЗастревание: {z}")

    except KeyError:
        bot.send_message(user_id, "Произошла ошибка при обработке ваших ответов. Пожалуйста, попробуйте еще раз с команды /test")


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
