
import telebot
import time  # Импортируем модуль time для задержки

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = 'Token'

bot = telebot.TeleBot(BOT_TOKEN)

# Количество вопросов
NUM_QUESTIONS = 3

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
    "Вопрос 1: Я люблю проводить время на природе.",
    "Вопрос 2: Я часто чувствую себя уставшим.",
    "Вопрос 3: Мне нравится общаться с новыми людьми.",
]

# Функция для обработки команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Привет, я 'Тест Бот'\nЗдесь вы можете пройти краткий тест, чтобы узнать о себе.\nЕсли хотите начать, нажмите /test")

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

            # Собираем ID сообщений для удаления
            messages_to_delete = []

            # Добавляем все сообщения об ошибках, если они есть
            if 'error_message_ids' in user_answers[user_id]:
                messages_to_delete.extend(user_answers[user_id]['error_message_ids'])

            # Добавляем ответ пользователя
            messages_to_delete.append(message.message_id)

            # Добавляем предыдущий вопрос
            messages_to_delete.append(user_answers[user_id].get('current_question_message_id'))


            # Удаляем все сообщения одновременно
            try:
                time.sleep(1)  # Задержка перед удалением

                for message_id in messages_to_delete:
                   try:  # Добавляем еще один уровень try-except для каждого удаления
                        bot.delete_message(user_id, message_id)
                   except telebot.apihelper.ApiTelegramException as e:
                        if e.description == "Bad Request: message to delete not found":
                            print(f"Сообщение {message_id} уже удалено или не существует.")
                        else:
                            print(f"Ошибка при удалении сообщения {message_id}: {e}")

                # Очищаем error_message_ids, если они были удалены
                if 'error_message_ids' in user_answers[user_id]:
                    del user_answers[user_id]['error_message_ids']



            except telebot.apihelper.ApiTelegramException as e:
                print(f"Ошибка при удалении сообщения: {e}")


            current_question[user_id] += 1  # Переходим к следующему вопросу

            # Если это последний вопрос
            if current_question[user_id] == NUM_QUESTIONS:
                # Собираем ID сообщений для удаления
                messages_to_delete = []

                # Добавляем все сообщения об ошибках, если они есть
                if 'error_message_ids' in user_answers[user_id]:
                    messages_to_delete.extend(user_answers[user_id]['error_message_ids'])

                # Добавляем ответ пользователя
                messages_to_delete.append(message.message_id)

                # Добавляем предыдущий вопрос
                messages_to_delete.append(user_answers[user_id].get('current_question_message_id'))


                try:
                     time.sleep(1)  # Задержка перед удалением

                     for message_id in messages_to_delete:
                          try:  # Добавляем еще один уровень try-except для каждого удаления
                              bot.delete_message(user_id, message_id)
                          except telebot.apihelper.ApiTelegramException as e:
                               if e.description == "Bad Request: message to delete not found":
                                   print(f"Сообщение {message_id} уже удалено или не существует.")
                               else:
                                   print(f"Ошибка при удалении сообщения {message_id}: {e}")


                     # Очищаем error_message_ids, если они были удалены
                     if 'error_message_ids' in user_answers[user_id]:
                         del user_answers[user_id]['error_message_ids']


                except telebot.apihelper.ApiTelegramException as e:
                    print(f"Ошибка при удалении сообщения: {e}")

                # Удаляем сообщение с инструкциями
                try:
                    time.sleep(1)
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
            error_message = bot.send_message(user_id, "Пожалуйста, введите число от 1 до 7.")

            # Сохраняем ID сообщения об ошибке в список
            if 'error_message_ids' not in user_answers[user_id]:
                user_answers[user_id]['error_message_ids'] = []
            user_answers[user_id]['error_message_ids'].append(error_message.message_id)


    except ValueError:
        # Если ответ не является числом
        error_message = bot.send_message(user_id, "Пожалуйста, введите числовое значение.")

        # Сохраняем ID сообщения об ошибке в список
        if 'error_message_ids' not in user_answers[user_id]:
            user_answers[user_id]['error_message_ids'] = []
        user_answers[user_id]['error_message_ids'].append(error_message.message_id)


# Функция для вычисления и отправки результата
def calculate_and_respond(user_id):
    try:
        otvet1 = user_answers[user_id][0]
        otvet2 = user_answers[user_id][1]
        otvet3 = user_answers[user_id][2]

        # Формула расчета (пример)
        i = otvet1 + otvet3 - otvet2

        # Логика вывода сообщения (пример)
        if i > 10:
            result_text = "Вы, скорее всего, оптимист!"
        elif 5 <= i <= 10:
            result_text = "Вы, вероятно, реалист."
        else:
            result_text = "Вы, возможно, пессимист."

        bot.send_message(user_id, f"Вы: {result_text}")

    except KeyError:
        bot.send_message(user_id, "Произошла ошибка при обработке ваших ответов. Пожалуйста, попробуйте еще раз с команды /test")


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
