# coding: utf-8
from __future__ import unicode_literals
from little_fuctions import *
from database import *
from datetime import datetime

par_task=['id', 'user_id', 'title', 'description', 'deadline', 'performer_id', 'category_id', 'priority', 'step', 'done']

def handle_dialog(request, response, user_storage, database):
    if not user_storage:
        user_storage = {"suggests": ['Помощь']}
    input_message = request.command.lower()

    if request.user_id not in database.get_session(all=True):
        database.add_session(request.user_id)

    if input_message in ['выйти', 'выход']:
        output_message = "Обращайтесь ещё!)"
        user_storage = {'suggests': ['Помощь', 'Войти']}
        database.update_status_system('login', request.user_id)
        return message_return(response, user_storage, output_message)

    if request.is_new_session or input_message in ['войти', 'регистрация']:
        output_message = "Привет! Чтобы увидеть свои задачи введи логин и пароль через пробел."
        user_storage = {'suggests': ['Помощь']}
        database.update_status_system('login', request.user_id)
        return message_return(response, user_storage, output_message)

    if len(input_message.split(' ')) == 2 and database.get_session(request.user_id, 'status_action')[
        0] == 'login':
        input_message = request.command.split(' ')
        user = User.query.filter_by(username=input_message[0]).first()
        print(user, input_message)
        if user:
            if input_message[1] == user.password:
                output_message = f"Добро пожаловать {input_message[0]}"
                user_storage = {'suggests': ['Посмотреть задачи', 'Добавить задачу', 'Помощь', 'Выйти']}
                database.update_status_system(input_message[0], request.user_id, 'user_name')
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

    if input_message == 'помощь':
        database.update_status_system('help', request.user_id, 'status_action')
        output_message = "Привет! Я Адель, Ваш коммуникатор. Я помогу Вам отправить сообщение " \
                         "Вашему другу или разместить его в группе."
        user_storage = {'suggests': ['Мои возможности', 'Команды быстрого ввода', 'Главная']}
        database.update_status_system('working', request.user_id, 'status_action')
        return message_return(response, user_storage, output_message)

    if input_message in ['главная', 'отбой, давай на главную']:
        output_message = "Прошу)"
        if database.get_session(request.user_id, 'status_action')[0] == 'login':
            user_storage = {'suggests': ['Помощь', 'Войти']}
        else:
            database.update_status_system('first', request.user_id)
            user_storage = {
                'suggests': ['Посмотреть задачи', 'Добавить задачу', 'Помощь', 'Выйти']}
        database.update_status_system('first', request.user_id, 'status_action')
        return message_return(response, user_storage, output_message)

    if input_message in ['покажи мои задачи', 'посмотреть задачи']:
        user_name = database.get_session(request.user_id, 'user_name')[0]
        user = User.query.filter_by(username=user_name).first()
        task = Task.query.filter_by(user_id=user.id).all()
        if len(task)>0:
            output_message = "Прошу! Ваши задачи:\n" + '\n'.join(['Название: '+str(x.title)+"\n  Id: "+str(x.id)+"\n  Время выполнения: "+str(x.deadline) for x in task])
            user_storage = {'suggests': ['Помощь', 'Главная']}
            database.update_status_system('monitoring_tasks', request.user_id)
            return message_return(response, user_storage, output_message)
        else:
            output_message = "Прости, но я не нашла ни одной твоей задачи.\nНо ты можешь добавить новую!"
            user_storage = {'suggests': ['Добавить', 'Помощь', 'Главная']}
            database.update_status_system('monitoring_tasks', request.user_id)
            return message_return(response, user_storage, output_message)

    if input_message in ['покажи просроченные задачи', 'посмотреть задачи']:
        user_name = database.get_session(request.user_id, 'user_name')[0]
        user = User.query.filter_by(username=user_name).first()
        task = Task.query.filter_by(user_id=user.id).all()
        task = [x for x in task if datetime.strptime(x.deadline, '%d.%m.%Y %H:%M')<datetime.now()]
        if len(task)>0:
            output_message = "Прошу! Ваши задачи:\n" + '\n'.join(['Название: '+str(x.title)+"\n  Id: "+str(x.id)+"\n  Время выполнения: "+str(x.deadline) for x in task ])
            user_storage = {'suggests': ['Помощь', 'Главная']}
            database.update_status_system('monitoring_tasks', request.user_id)
            return message_return(response, user_storage, output_message)
        else:
            output_message = "Ты натоящий молодец! У тебя ни одной просрочки!!"
            user_storage = {'suggests': ['Добавить', 'Помощь', 'Главная']}
            database.update_status_system('monitoring_tasks', request.user_id)
            return message_return(response, user_storage, output_message)

    if 'назначить задачу номер' in input_message and len(input_message.strip().split(' ')) == 5:
        task_id = int(input_message.strip().split(' ')[3])
        task = Task.query.filter_by(id=task_id).first()
        user = User.query.filter_by(username=input_message.strip().split(' ')[-1]).first()
        if task:
            if user:
                task.performer_id += ';'+str(user.id)
        user_storage = {'suggests': ['Посмотреть задачи', 'Добавить задачу', 'Помощь']}
        database.update_status_system('first', request.user_id)
        return message_return(response, user_storage, output_message)

    if 'покажи задачу номер' in input_message and len(input_message.strip().split(' ')) == 4:
        task_id = int(input_message.strip().split(' ')[-1])
        task = Task.query.filter_by(id=task_id).first()
        output_message = "Прошу! Ваша задача:\n" + '\n'.join(['Название: '+str(task.title), 'Описание: '+str(task.description)[:500], 'Дата выполнения: '+str(task.deadline), 'Исполнители: '+str('; '.join([User.query.filter_by(id=int(x)).first().username for x in task.performer_id.split(';')]))])
        user_storage = {'suggests': ['Посмотреть задачи', 'Добавить задачу', 'Помощь']}
        database.update_status_system('first', request.user_id)
        return message_return(response, user_storage, output_message)

    if input_message in ['добавить', 'добавить задачу']:
        output_message = "Хорошо! Говори название"
        user_storage = {'suggests': ['Отмена', 'Помощь', 'Главная']}
        database.update_status_system('add_task_name', request.user_id)
        return message_return(response, user_storage, output_message)

    if input_message == '' and database.get_session(request.user_id, 'status_action')[0] in []:
        output_message = "Хорошо."
        user_storage = {'suggests': ['Посмотреть задачи', 'Добавить задачу', 'Помощь', 'Главная']}
        database.update_status_system('add_task_finish', request.user_id)
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'add_task_name':
        title = request.command
        user_name = database.get_session(request.user_id, 'user_name')[0]
        user = User.query.filter_by(username=user_name).first()
        task = Task(user_id=user.id, title=title,
                        description='',
                        deadline='',
                        performer_id=user.id,
                        category_id=0)
        db.session.add(task)
        db.session.commit()
        database.update_status_system(Task.query.filter_by(title=title).all()[-1].id, request.user_id, 'id_connect_task')
        output_message = "Хорошо! Говори описание"
        user_storage = {'suggests': ['Отмена', 'Помощь', 'Главная']}
        database.update_status_system('add_task_description', request.user_id)
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'add_task_description':
        description = request.command
        task_id = database.get_session(request.user_id, 'id_connect_task')[0]
        Task.query.filter_by(id=task_id).first().description = description
        db.session.commit()
        output_message = "Хорошо! Говори категорию"
        user_storage = {'suggests': ['Отмена', 'Помощь', 'Главная']+[str(x.category) for x in Category.query.all()]}
        database.update_status_system('add_task_category', request.user_id)
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'add_task_category':
        category_id = Category.query.filter_by(category=request.command).first().id
        task_id = database.get_session(request.user_id, 'id_connect_task')[0]
        Task.query.filter_by(id=task_id).first().category_id = category_id
        db.session.commit()
        output_message = 'Хорошо! Говори дату выполнения в формате "дд.мм.гггг ЧЧ:ММ"'
        user_storage = {'suggests': ['Отмена', 'Помощь', 'Главная']}
        database.update_status_system('add_task_deadline', request.user_id)
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'add_task_deadline':
        deadline = request.command
        task_id = database.get_session(request.user_id, 'id_connect_task')[0]
        Task.query.filter_by(id=task_id).first().deadline = deadline
        db.session.commit()
        output_message = "Готово!"
        user_storage = {'suggests': ['Посмотреть задачи', 'Добавить задачу', 'Помощь', 'Главная']}
        database.update_status_system('add_task_finish', request.user_id)
        return message_return(response, user_storage, output_message)


    buttons, user_storage = get_suggests(user_storage)
    return message_error(response, user_storage,
                         ['Конфуз;) Я ещё в разработке', 'Ой, сейчас исправлю)'
                          ])