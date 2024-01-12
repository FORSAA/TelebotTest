import datetime
import random
import time

import pyodbc

from imports.import_to_bot import *
print('Initialization')
UserDataRepo = UserData_repo()
print(f'Database Connected!\n', '='*40)

bot_last_message = types.Message
wish = ''

token: str = '6070580163:AAFKRJt7nnNWL__vunKkFVz1r1IZ6xDJgXI'
bot = telebot.TeleBot(token)
Exceptions = ['При обработке запроса возникла ошибка! Возможно, не удалось зайти в ваш аккаунт. Проверьте ваш логин и пароль.']

pages = {
    'start':{'message_text':'Добро пожаловать в главное меню телеграмм бота! Используйте кнопки ниже для навигации.', 'markup_data':{
        'Смена Логина/Пароля': {'callback_data':'auth_data_edit'},
        'Как пользоваться?': {'callback_data': 'how_to'},
        'Получить Д/З': {'callback_data': 'get_homework'}
    }},
    'auth':{'message_text':'Тут вы можете поменять ваш логин и пароль для автоматической работы бота.\n\nЧтобы сменить ваш пароль, напишите его в следующем виде без пробелов: "Логин/Пароль\n\nP.S: Отправляя свои данные авторизации вы делаете это добровольно и соглашаетесь с их обработкой."', 'markup_data':{
        '«Вернуться в главное меню':{'callback_data':'menu'}
    }},
    'how_to':{'message_text':f'Как пользоваться ботом? Очень легко!\n\nДля начала использования бота достаточно ввести логин и пароль от сайта ГИССОЛО на странице ниже. (Кнопка "Смена Логина/Пароля"). \n \n После выполнения этого шага вы можете перейти по пути "Получить Д/З->Текст" и выбрать дату. Ваш запрос будет обработан.', 'markup_data':{
        '«Вернуться в главное меню':{'callback_data':'menu'},
        'Смена Логина/Пароля':{'callback_data':'auth_data_edit'}
    }},
    'get_homework': {'message_text': 'Выберите в каком формате бот должен отправить вам ответ.', 'markup_data': {
        'Текст': {'callback_data': 'wish_response_text'},
        'Изображение': {'callback_data': 'wish_response_photo'},
        '«Вернуться в главное меню': {'callback_data': 'menu'}
    }},
    'homework_date_select':{'message_text':'Выберите, домашнее задание какого дня должен отправить бот', 'markup_data':{
        'Завтра':{'callback_data':'wish_tomorrow'},
        'Сегодня':{'callback_data':'wish_today'},
        '«Вернуться в главное меню':{'callback_data':'menu'}
    }},
    'homework_date_select_tomorrow_only': {'message_text': 'Выберите, домашнее задание какого дня должен отправить бот', 'markup_data': {
        'Завтра': {'callback_data': 'wish_tomorrow'},
        '«Вернуться в главное меню': {'callback_data': 'menu'}
    }},
    'homework_date_select_today_only': {'message_text': 'Выберите, домашнее задание какого дня должен отправить бот','markup_data': {
        'Сегодня':{'callback_data':'wish_today'},
        '«Вернуться в главное меню': {'callback_data': 'menu'}
    }},
    'wish_response_photo':{'message_text':'Ошибка! Недоступно в данный момент.', 'markup_data':{
        '«Вернуться к выбору':{'callback_data':'get_homework'},
    }},
    'exceptions':{'message_text':'', 'markup_data':{
        '«Вернуться в главное меню':{'callback_data':'menu'},
    }},

}

session_number: int = random.randint(0, 579261776)
photomode = False

def markupGenerator(markup_data: dict = {}, width_of_row: int = 2) -> types.InlineKeyboardMarkup:
    markup = quick_markup(markup_data, row_width=width_of_row)
    return markup

def render(page_to_render:dict, message: types.Message, del_prev: bool = True) -> int:
    global bot_last_message
    if(del_prev):
        bot.delete_message(message.chat.id, message.id)
    bot_last_message = bot.send_message(message.chat.id, page_to_render['message_text'], reply_markup=markupGenerator(page_to_render['markup_data']))
    return bot_last_message.id

def throwErrorMessage(message, processing_message):
    global bot_last_message, session_number
    bot.delete_message(chat_id=message.chat.id, message_id=bot_last_message.id)
    bot.delete_message(chat_id=message.chat.id, message_id=processing_message.id)
    bot_last_message = bot.send_message(message.chat.id, 'Ошибка! Ваш аккаунт не найден в базе данных. Вы будете возвращены в меню.')
    print(f"getHomework_Error | NoneType_Auth_Data | Session: {session_number}")
    session_number = random.randint(0, 579261776)

def getHomework(callback, photomode:bool, by_day:int, auth_data, processing_message):
    global bot_last_message, session_number
    try:
        response = getHomework_main(auth_data.login, auth_data.password, generate_the_date(by_day), photomode)
    except AttributeError:
        throwErrorMessage(callback.message, processing_message)
        return
    print(f"Got response, sending | Session: {session_number}")
    if (response in Exceptions):
        pages['exceptions']['message_text'] = response
        render(pages['exceptions'], callback.message, del_prev=False)
    elif(response=='screenshot'):
        try:
            with open(r'E:\GitHub\TelebotTest\screenshot.png', 'rb') as screenshot:
                bot.send_photo(callback.message.chat.id, screenshot, 'Домашнее задание.')
        except FileNotFoundError:
            print(f'FileNotFoundError | Session: {session_number}')
            return
        bot.delete_message(chat_id=callback.message.chat.id, message_id=bot_last_message.id)
        bot.delete_message(chat_id=callback.message.chat.id, message_id=processing_message.id)
        print(f"Response sended! | Session: {session_number}")
        path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'screenshot.png')
        os.remove(path)
    else:
        bot.delete_message(chat_id=callback.message.chat.id, message_id=bot_last_message.id)
        bot.delete_message(chat_id=callback.message.chat.id, message_id=processing_message.id)
        bot_last_message = bot.send_message(callback.message.chat.id, response)
        print(f"Response sended! | Session: {session_number}")

def pre_getHomework(callback, photomode:bool) -> str:
    start_time = time.time()
    global bot_last_message, session_number
    bot.delete_message(callback.message.chat.id, callback.message.id)
    processing_message = bot.send_message(callback.message.chat.id, 'Ваш запрос в обработке..')
    print(f"Wish: {callback.data} | Photo Mode: {photomode}| Going try to get response | Session: {session_number} ")
    bot_last_message = bot.send_message(callback.message.chat.id, 'Получение данных авторизации..')
    auth_data = UserDataRepo.SelectByTelegram_Id(callback.from_user.id)
    print(f"Got Auth_Data | Session: {session_number} ")
    if(callback.data=='wish_tomorrow'):
        bot.edit_message_text(message_id=bot_last_message.id, chat_id=callback.message.chat.id, text=f'Данные авторизации получены! Получение домашнего задания на {generate_the_date(1)}..')
        getHomework(callback, photomode, 1, auth_data, processing_message)
    elif(callback.data=='wish_today'):
        bot.edit_message_text(message_id=bot_last_message.id, chat_id=callback.message.chat.id, text=f'Данные авторизации получены! Получение домашнего задания на {generate_the_date(0)}..')
        getHomework(callback, photomode, 0, auth_data, processing_message)
    end_time = time.time()
    to_response_time = end_time - start_time
    print(f"to_response_time: {to_response_time} | Session: {session_number}")
    print("=" * 40)
    session_number = random.randint(0, 579261776)
    render(pages['start'], callback.message, del_prev=False)

@bot.message_handler(commands=['start'])
def start(message):
    render(pages['start'], message)

@bot.callback_query_handler(func=lambda callback: callback.data)
def callback_data_processing(callback):
    global photomode

    if(callback.data=='auth_data_edit'):
        render(pages['auth'], callback.message)
        bot.register_next_step_handler(callback.message, edit_auth_data)

    elif(callback.data=='how_to'):
        render(pages['how_to'], callback.message)

    elif(callback.data=='get_homework'):
        render(pages['get_homework'], callback.message)

    elif(callback.data=='wish_response_text' or callback.data=='wish_response_photo'):
        if(callback.data=='wish_response_photo'):
            photomode = True
        else:
            photomode = False

        print(f'Wish: {callback.data} | Session: {session_number}')
        if(datetime.date.weekday(datetime.date.today())==6):
            print(f'Menu: tomorrow_only_menu | Session: {session_number}')
            render(pages['homework_date_select_tomorrow_only'], callback.message)
        elif(datetime.date.weekday(datetime.date.today())==5):
            print(f'Menu: toay_only_menu | Session: {session_number}')
            render(pages['homework_date_select_today_only'], callback.message)
        else:
            print(f'Menu: both_date_menu | Session: {session_number}')
            render(pages['homework_date_select'], callback.message)

    elif(callback.data=='wish_tomorrow'):
        pre_getHomework(callback, photomode=photomode)

    elif(callback.data=='wish_today'):
        pre_getHomework(callback, photomode=photomode)

    elif(callback.data=='menu'):
        render(pages['start'], callback.message)

def edit_auth_data(message):
    global session_number
    print(f'Auth_Data_Edit_Request | Requested_by: {message.from_user.id} | Session: {session_number}')
    auth_data = message.text.split('/')
    if(len(auth_data)!=2 or '' in auth_data):
        print(f'Auth_Data_Edit_Fail | Requested_by: {message.from_user.id} | Session: {session_number}')
        bot.edit_message_text(chat_id=message.chat.id,message_id=bot_last_message.id,text='Неверный формат пароля! Вы будете возвращены в меню.\n\nПроверьте верность написания пароля и сравните его с шаблоном.')
        bot.delete_message(message.chat.id, message.id)
        auth_data = None
        render(pages['start'], message)
        session_number = random.randint(0, 579261776)
    else:
        auth_data.append(message.from_user.id)
        User = User_Pattern(auth_data[0], auth_data[1], auth_data[2])
        try:
            if(str(type(UserDataRepo.SelectByTelegram_Id(User.telegram_id)))!="<class 'NoneType'>"):
                UserDataRepo.EditUser(User)
            else:
                UserDataRepo.AddUser(User)
            password_edited_alert_message = bot.edit_message_text(chat_id=message.chat.id, message_id=bot_last_message.id, text='Пароль успешно изменён!')
        except pyodbc.IntegrityError:
            bot.send_message(message.chat.id, 'Ошибка! В базе данных уже присутствует такой логин и пароль, привязанный к другому аккаунту!\n\nВы будете возвращены в меню.')
            render(pages['start'], message)
            return
        print(f'Auth_Data_Edit_Successfully | Requested_by: {message.from_user.id} | Session: {session_number}')
        render(pages['start'], message)
        session_number = random.randint(0, 579261776)
        time.sleep(2)
        bot.delete_message(password_edited_alert_message.chat.id, password_edited_alert_message.id)


bot.polling()

