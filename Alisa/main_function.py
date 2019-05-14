# coding: utf-8
from __future__ import unicode_literals
from little_fuctions import *
from database import *

par_task=['id', 'user_id', 'title', 'description', 'deadline', 'performer_id', 'category_id', 'priority', 'step', 'done']

def handle_dialog(request, response, user_storage, database):
    input_message = request.command.lower()

    if request.user_id not in database.get_session(all=True):
        database.add_session(request.user_id)

    if request.is_new_session or input_message in ['войти', 'регистрация']:
        output_message = "Привет! Чтобы увидеть свои задачи введи логин и пароль через пробел."
        user_storage = {'suggests': ['Помощь']}
        database.update_status_system('login', request.user_id)
        return message_return(response, user_storage, output_message)

    if input_message.split(' ') == 2 and database.get_session(request.user_id, 'status_action')[
        0] == 'login':
        input_message = request.command.split(' ')
        user = User.query.filter_by(username=input_message[0]).first()
        if user:
            if input_message[1] == user.password():
                output_message = f"Добро пожаловать {input_message[0]}"
                user_storage = {'suggests': ['Посмотреть задачи', 'Добавить задачу', 'Помощь']}
                database.add_sessions(request.user_id, input_message[0])
                database.update_status_system('first', request.user_id)
                return message_return(response, user_storage, output_message)
            else:
                output_message = "Неверный пароль"
                user_storage = {'suggests': ['Помощь']}
                return message_return(response, user_storage, output_message)
        else:
            output_message = "Пользователь не найден("
            user_storage = {'suggests': ['Помощь']}
            return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'first':
        if input_message == 'покажи мои задачи':
            user_name = database.get_session(request.user_id, 'user_name')
            user_id = User.query.filter_by(username=user_name).first()
            task = Task.query.filter_by(user_id=user_id)
            output_message = f"Прошу! Ваши задачи:\n" + '\n'.join([str(x.name)+"\n  "+str(x.id)+"\n  "+str(x.deadline) for x in task])
            user_storage = {'suggests': ['Посмотреть задачи', 'Добавить задачу', 'Помощь']}
            database.add_sessions(request.user_id, input_message[0])
            database.update_status_system('first', request.user_id)
            return message_return(response, user_storage, output_message)

        '''if 'покажи задачу номер' in input_message and input_message.strip().split(' ') == 4:
            task_id = input_message.strip().split(' ')[-1]
            task = Task.query.filter_by(id=task_id).first()
            output_message = f"Прошу! Ваша задача:\n" + '\n'.join([str(task.name), str(task.description)[:500], str(task.deadline), str(task.)])
            user_storage = {'suggests': ['Посмотреть задачи', 'Добавить задачу', 'Помощь']}
            database.add_sessions(request.user_id, input_message[0])
            database.update_status_system('first', request.user_id)
            return message_return(response, user_storage, output_message)'''

    buttons, user_storage = get_suggests(user_storage)
    return message_error(response, user_storage,
                         ['Конфуз;) Я ещё в разработке', 'Ой, сейчас исправлю)'
                          ])

