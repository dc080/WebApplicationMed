from flask import session, Flask
import datetime
import random

import os

UPLOAD_FOLDER = 'static/image'
global app
app = Flask(__name__)

def verifySessionId():  # Функция для определения id # Использовать истечение сессии, а не придумывать велосипед
    ###################################################################
    # session.clear() # ТЕСТОВАЯ СТРОКА КОТОРУЮ НАДО УДАЛИТЬ ПОСЛЕ ОТЛАДКИ
    ###################################################################
    if not 'dateSingIn' in session:  # Если в хэше нет записи о дате
        session.clear()  # Очищает весь хэш сессии
    elif (datetime.datetime.now() - session['dateSingIn']).days > 1:  # Или если дата есть, но у нее разница с текущей
        # больше дня
        session.clear()  # Очищает весь хэш сессии
    if not 'idSession' in session:  # Проверка на отсутствие в хэше id сессии
        while True:  # Цикл для генерации не занятого значения
            randomId = random.randint(1, 200)  # Генерация рандомного числа от 1 до 200
            if not os.path.exists(calculateSavePath(randomId)):  # Если пути с этим числом не существует
                break  # то выход из цикла
        session['idSession'] = randomId  # Присвоение этого числа в хэш
        session['dateSingIn'] = datetime.datetime.now()  # Запись даты присвоения в хэш
    return session['idSession']  # Возврат id, или нового, или старого не измененного

def calculateSavePath(id):  # Функция расчета папки с использованием id
    return UPLOAD_FOLDER + '/' + str(id)  # Базовая папка + папка с названием id

def calculatePathToSavedFile(id):  # Функция возврата пути к загруженному файлу с использованием id и исходного имени
    return UPLOAD_FOLDER + '/' + str(id) + '/' + session['originalFileName']

def calculatePathToEditedFile(id):  # Функция возврата пути к файлу, созданному алгоритмом с использованием id
    return UPLOAD_FOLDER + '/' + str(id) + '/tempimg.jpg'  # Базовая папка + папка с названием id + измененный файл

def calculatePathToLineFile(id):
    return UPLOAD_FOLDER + '/' + str(id) + '/lineimg.jpg'

def saveFileNameIntoSession(pathToFile, id):
    path, fileName = os.path.split(pathToFile)  # Разбиение файла на его путь с названием и типом файла
    session['originalFileName'] = fileName # Сохранение имени файла в кеш
