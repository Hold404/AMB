#Auto Moderator Bot 4.2 by Hold404

from aiogram import * #импортируем все из библиотеки aiogram
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.types import chat

from fuzzywuzzy import fuzz #импортируем класс из библиотеки нечеткого разспознования
from add_exp import add_exp
import json
import random
import ast

TOKEN = '' #токен бота
GROUP_ID = '' #айди группы
filename = 'lavels.json'
filename2 = 'words.txt'
filename3 = 'settings_names.txt'
admins_id_list = [676940003]

xpMin = 1 #минимальное количство опыта (0.01)
xpMax = 6 #максимальное количество опыта (0.06)

with open(filename2, 'r', encoding="utf-8") as f: #открываем файл с матами в режиме чтения
    string_word_blackList = f.read() #загружаем список слов из файла в строку
    f.close() #закрываем файл

word_blackList = ast.literal_eval(string_word_blackList) #делаем из строки массив

string_word_blackList = string_word_blackList.replace('[', '')
string_word_blackList = string_word_blackList.replace(']', '')
string_word_blackList = string_word_blackList.replace("'", '')

bot = Bot(token=TOKEN) #импортируем токен в бота
dp = Dispatcher(bot) #запускаем токен в диспатчер

wcdo_btn = InlineKeyboardButton('Возможности', callback_data='wcdo_btn')
wlist_btn = InlineKeyboardButton('Список слов', callback_data='wlist_btn')
kb = InlineKeyboardMarkup().add(wcdo_btn, wlist_btn)

#для включения-выключения разных модулей
mdr = None
rnk = None

#settings buttons
with open(filename3, 'r') as f:
    settings_array = f.read()
    f.close()

settings_array = ast.literal_eval(settings_array)

#обработка кнопок
#обработчик кнопки Список слов
@dp.callback_query_handler(text = 'wlist_btn')
async def process_callback_button1(call=types.CallbackQuery):
    await call.message.answer(f'Вот список матных слов: {string_word_blackList}')

#обработчик кнопки Возможности
@dp.callback_query_handler(text = 'wcdo_btn')
async def process_callback_button1(call=types.CallbackQuery):
    await call.message.answer(f'Мои возможности: Защита от плохих слов, подсчет опыта и уровней.')

#обработчик кнопок настроек
@dp.callback_query_handler(text = 's1')
async def process_callback_button1(call=types.CallbackQuery):
    is_admin = False
    print(call)
    for x in admins_id_list:
        if x == call['from']['id']:
            is_admin = True
            break

    if is_admin:
        global mdr
        global settings_array

        await call.message.answer(f'Настройка изменена.')

        if mdr:
            mdr = False
            settings_array[0] = 'False'
        else:
            mdr = True
            settings_array[0] = 'True'

        with open(filename3, 'w') as f:
            f.write(str(settings_array))
            f.close()

    else:
        await bot.send_message(GROUP_ID, 'Вы не являетесь администратором! Эта команда закрыта простым смертным :З')

@dp.callback_query_handler(text = 's2')
async def process_callback_button1(call=types.CallbackQuery):
    is_admin = False

    for x in admins_id_list:
        if x == call['from']['id']:
            is_admin = True
            break

    if is_admin:
        global rnk
        global settings_array

        await call.message.answer(f'Настройка изменена.')

        if rnk:
            rnk = False
            settings_array[1] = 'False'
        else:
            rnk = True
            settings_array[1] = 'True'

        with open(filename3, 'w') as f:
            f.write(str(settings_array))
            f.close()

    else:
        await bot.send_message(GROUP_ID, 'Вы не являетесь администратором! Эта команда закрыта простым смертным :З')

#команда /start
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    if str(msg.chat.id) == GROUP_ID:
        await bot.send_message(GROUP_ID, "Здравствуйте, меня зовут AMB2.0! \nЯ - бот модератор, удалю все плохие слова из предложений \nи буду считать уровень каждого участника беседы.\nЕсли хотите узнать больше напишите: /help")

    else:
        await bot.send_message(msg.chat.id, 'Нельзя использовать бота вне группы, попробуйте ввести команду в группе.')

#команда /help
@dp.message_handler(commands=['help'])
async def help(msg: types.Message):
    if str(msg.chat.id) == GROUP_ID:
        await bot.send_message(GROUP_ID, 'Для того, что-бы посмотреть возможности бота нажмите кнопку: Возможности\nЕсли вы хотите видеть список запрещенных слов - нажмите кнопку: Список слов \nДругие команды бота: \n/rank @имя пользователя\n/add_all_users', reply_markup=kb)
        await bot.send_message(GROUP_ID, 'Так-же я могу посчитать ваши уровни. С каждым сообщением вы будете получать опыт и уровни. \nДля контроля существует 2 команд, это:\n/rank @имя пользователя (уровень пользователя)\n/add_users (добавить пользователей в базу)\n/settings (настройки бота)')

    else:
        await bot.send_message(msg.chat.id, 'Нельзя использовать бота вне группы, попробуйте ввести команду в группе.')

#команда /settings
@dp.message_handler(commands=['settings'])
async def settings(msg: types.Message):
    if str(msg.chat.id) == GROUP_ID:
        is_admin = False

        for x in admins_id_list:
            if x == msg.from_user['id']:
                is_admin = True
                break

        if is_admin:
            settings_text1 = ''
            settings_text2 = ''

            if settings_array[0] == 'True':
                mdr = True
                settings_text1 = 'Авто-модерация: Включена'

            elif settings_array[0] == 'False':
                mdr = False
                settings_text1 = 'Авто-модерация: Выключена'

            if settings_array[1] == 'True':
                rnk = True
                settings_text2 = 'Подсчет уровней: Включен'

            elif settings_array[1] == 'False':
                rnk = False
                settings_text2 = 'Подсчет уровней: Выключен'

            #создание кнопок
            settings1 = InlineKeyboardButton(settings_text1, callback_data='s1')
            settings2 = InlineKeyboardButton(settings_text2, callback_data='s2')

            settings_kb = InlineKeyboardMarkup().add(settings1, settings2)

            await bot.send_message(GROUP_ID, 'Для изменения значений нажмите на кнопку. (Для того, что-бы увидить измененения напишите команду: /settings снова)', reply_markup=settings_kb)

        else:
            await bot.send_message(GROUP_ID, 'Вы не являетесь администратором! Эта команда закрыта простым смертным :З')

    else:
        await bot.send_message(msg.chat.id, 'Нельзя использовать бота вне группы, попробуйте ввести команду в группе.')

#команда /add_users
@dp.message_handler(commands=['add_users'])
async def add_all_users(msg: types.Message):
    if str(msg.chat.id) == GROUP_ID:
        is_admin = False

        for x in admins_id_list:
            if x == msg.from_user['id']:
                is_admin = True
                break

        if is_admin:
            ts = msg.text #записываем текст сообщения в отдельную переменную
            ts = ts.replace('/add_users ', '')
            ts = ts.split(', ') #делаем из стркои список

            with open(filename, 'r') as f: #открываем файл на чтение
                current_list = f.read() #получаем строку из джейсона
                f.close() #закрываем файл

            current_list = json.loads(current_list) #делаем из строки словарь

            for x in ts: #запускаем цикл для чтение всех пользователей из массива ts
                current_list[x] = [0, 0] #загружаем их в словарь

            with open(filename, 'w') as f: #открываем файл в режиме записи
                json.dump(current_list, f) #загружаем изменения
                f.close() #закрываем файл

        else:
            await bot.send_message(GROUP_ID, 'Вы не являетесь администратором! Эта команда закрыта простым смертным :З')

    else:
        await bot.send_message(msg.chat.id, 'Нельзя использовать бота вне группы, попробуйте ввести команду в группе.')

#команда /rank
@dp.message_handler(commands=['rank'])
async def rank(msg: types.Message):
    if str(msg.chat.id) == GROUP_ID:
        if rnk:
            a = False #создаем системную переменныю
            author = msg.from_user['username'] #получаем автора сообщения
            author = f'@{author}' #добавляем символ собаки к сообщению

            with open(filename, 'r') as f: #открываем файл, достаем информацию о уровнях
                ar = f.read()
                f.close()

            ar = json.loads(ar) #преобразорвываем информацию из строки в словарь

            message = list(msg.text) #разбиваем сообщение на массив

            try:
                for x in range(1, 7):
                    message.pop(0) #достаем имя пользователя, если его нет то:

            except IndexError:
                st = f'Ваш уровень: {ar[author][1]}.' #отображаем уровень пользователя отправившего сообщение
                a = True #переводим системную переменную

            mesg = ''.join(message) #соеденяем имя автора из массива в строку

            try:
                st = f'{mesg} имеет: {ar[mesg][1]} уровень.' #если пользователь есть в базе выводим его уровень

            except KeyError:
                if a == False: #если пользователь был указан но его нет в базе отправляем это:
                    st = f'Пользователь не найден! Ваш уровень равен: {ar[author][1]}.'

                #если пользователь не был указан то отправляем данные о авторе сообщения

            await bot.send_message(GROUP_ID, st) #высылаем информацию в сообщения

        else:
            await bot.send_message(GROUP_ID, 'Команда отключена в настройках.')

    else:
        await bot.send_message(msg.chat.id, 'Нельзя использовать бота вне группы, попробуйте ввести команду в группе.')

#основная функция модерирования
@dp.message_handler() #создаем хендлер
async def process_start_command(msg: types.Message): #создаем функцию
    if str(msg.chat.id) == GROUP_ID:
        if rnk:
            author = msg.from_user['username'] #получаем ник автора
            author_with_symmbol = f'@{author}'

            a = random.randint(xpMin, xpMax)
            a = a * 0.01
            n_lvl = add_exp(author_with_symmbol, a, filename)

            if type(n_lvl) == type(1):
                await bot.send_message(GROUP_ID, f'Пользователь: {author_with_symmbol} апнул уровень: {n_lvl}! 🥳')

            message = msg.text.split() #разбиваем предложение на слова

        if mdr:
            for x in word_blackList: #запускаем цикл проверки на плохие слова
                for y in message: #запускаем цикл для сравнения слов в предложении со словами из списка
                    if fuzz.WRatio(x, y) >= 91: #если слова совпадают больше чем на 90%
                        logString = f'[Log] Удаленно сообщение: {msg.text}\n[Log] Автор: {author_with_symmbol}' #формируем строку логов
                        await bot.delete_message(GROUP_ID, msg.message_id) #удаляем сообщение
                        await bot.send_message(GROUP_ID, logString) #отправляем логи
    else:
        await bot.send_message(msg.chat.id, 'Нельзя использовать бота вне группы, попробуйте ввести команду в группе.')

if __name__ == '__main__': #проверяем запущен ли файл (или он импортируеться)
    executor.start_polling(dp) #запускаем бота
