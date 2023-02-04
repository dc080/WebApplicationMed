import datetime
import random
import shutil

from flask import Flask, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

import os

# import main
from Algorithms.FindFractNumber import FindFractNumber # Библиотека для фрактального числа
from Algorithms.FindSquareCrystals import FindSquareCrystals # Библиотека для поиска площади кристаллов

UPLOAD_FOLDER = 'static/image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///med.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'someRandomKey' # Какой-то секретный ключ, без которого нихера не работает
app.config['SESSION_TYPE'] = 'filesystem' # Тип подключение сессии

Session(app) # Запуск сессии в приложении

db = SQLAlchemy(app)

algoFract = FindFractNumber()
algoSquare = FindSquareCrystals()

def verifySessionId(): # Функция для определения id
    if not 'dateSingIn' in session: # Если в хэше нет записи о дате
        session.clear() # Очищает весь хэш сессии
    elif (datetime.datetime.now() - session['dateSingIn']).days > 1: # Или если дата есть, но у нее разница с текущей
        # больше дня
        session.clear() # Очищает весь хэш сессии
    if not 'idSession' in session: # Проверка на отсутствие в хэше id сессии
        while True: # Цикл для генерации не занятого значения
            randomId = random.randint(1, 200) # Генерация рандомного числа от 1 до 200
            if not os.path.exists(calculateSavePath(randomId)): # Если пути с этим числом не существует
                break # то выход из цикла
        session['idSession'] = randomId # Присвоение этого числа в хэш
        session['dateSingIn'] = datetime.datetime.now() # Запись даты присвоения в хэш
    return session['idSession'] # Возврат id, или нового, или старого не измененного


def calculateSavePath(id): # Функция расчета папки с использованием id
    return UPLOAD_FOLDER + '/' + str(id) # Базовая папка + папка с названием id


def calculatePathToSavedFile(id, extention): # Функция возврата пути к загруженному файлу с использованием id,
    # и типом файла
    return UPLOAD_FOLDER + '/' + str(id) + '/input' + extention # Базовая папка + папка с названием id + тип файла


def calculatePathToEditedFile(id): # Функция возврата пути к файлу, созданному алгоритмом с использованием id,
    # и типом файла
    return UPLOAD_FOLDER + '/' + str(id) + '/tempimg.jpg' # Базовая папка + папка с названием id + измененный файл


def renameFile(filename, id):
    fileName, fileExtension = os.path.splitext(filename) # Разбиение файла на его путь с названием и типом файла
    pathToNewFile = calculatePathToSavedFile(id, fileExtension) # Расчет нового пути к переименованному файлу
    if os.path.isfile(pathToNewFile): # Проверка на существующий файл, в который хотим переименовывать
        os.remove(pathToNewFile) # Удаляем если есть
    os.rename(filename, pathToNewFile) # Переименование загруженного файла на файл с
    # необходимым названием и исходным типом файла
    return fileExtension # Возврат типа файла (Вроде это костыль с моей стороны)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        try:
            if "load" in request.form: # Если нажата кнопка загрузки
                idSession = verifySessionId() # Присвоение ID, если это надо
                file = request.files['file'] # Запрос файла
                savePath = calculateSavePath(idSession) # Обозначение пути до загруженного файла
                if not os.path.exists(savePath): # Если пути нет
                    os.makedirs(savePath) # Создать его
                savedFile = os.path.join(savePath, file.filename) # Путь до сохраняемого файла с его исходным названием
                file.save(savedFile) # Сохранение файла
                extention = renameFile(savedFile, idSession) # Переименовка файла
                pic = calculatePathToSavedFile(idSession, extention) # Путь до сохраненного файла с новым названием
                algoSquare.loadImage(pic) # Загрузка изображения в алгоритм
                session['fractalNumber'] = algoFract.resolveFractNumber(pic) # Сохранение результата алгоритма в хэш
                return render_template("index.html", uploaded_image=file.filename, contours=pic,
                                   Res=session['fractalNumber'], light=algoSquare.light, dark=algoSquare.dark) # Отрисовка веб-страницы

            elif "edit" in request.form: # Если нажата кнопка изменения
                light = int(request.form['light']) # Считывание значения ползунков
                dark = int(request.form['dark']) # -/-
                algoSquare.light = light # Занесение значений в алгоритм
                algoSquare.dark = dark # -/-
                algoSquare.editImage() # Обработка изображения
                return render_template("index.html", contours=calculatePathToEditedFile(session['idSession']), light=request.form['light'],
                                   dark=request.form['dark'], Res=session['fractalNumber']) # Отрисовка веб-страницы

            elif "runAlgo" in request.form: # Если нажата кнопка запуска алгоритма
                light = int(request.form['light']) # Считывание значения ползунков
                dark = int(request.form['dark']) # -/-
                algoSquare.light = light # Занесение значений в алгоритм
                algoSquare.dark = dark # -/-
                algoSquare.editImage() # Обработка изображения
                session['squareNumber'] = algoSquare.resolveSquare() # Занесение значения площади в хэш
                return render_template("index.html", contours=calculatePathToEditedFile(session['idSession']),
                                   light=request.form['light'], dark=request.form['dark'],
                                   Res=session['fractalNumber'], S=session['squareNumber']) # Отрисовка веб-страницы
            elif "orig" in request.form:
                savePath = calculateSavePath(session['idSession'])
                return render_template("index.html", contours=savePath + "/input.png", light=algoSquare.light, dark=algoSquare.dark)
            elif "modifed" in request.form:
                return render_template("index.html", contours=calculatePathToEditedFile(session['idSession']), light=algoSquare.light, dark=algoSquare.dark)

        except FileNotFoundError:
            flash('Выберите изображение')
            return render_template("index.html", light=algoSquare.light, dark=algoSquare.dark)
        except IsADirectoryError:
            flash('Выберите изображение')
            return render_template("index.html", light=algoSquare.light, dark=algoSquare.dark)
        except ValueError:
            savePath = calculateSavePath(session['idSession'])
            flash('Некорректное значение границ')
            return render_template("index.html", contours=savePath + "/input.png", light=algoSquare.light, dark=algoSquare.dark)
        except Exception:
            flash('Сначала загрузите изображение')
            return render_template("index.html", light=algoSquare.light, dark=algoSquare.dark)

        else:

            return render_template("index.html") # Отрисовка веб-страницы
    else:
        files = os.listdir(UPLOAD_FOLDER)
        if len(files) > 1:
            shutil.rmtree(UPLOAD_FOLDER)
            os.mkdir(UPLOAD_FOLDER)
        return render_template("index.html", light=algoSquare.light, dark=algoSquare.dark)  # Отрисовка веб-страницы


if __name__ == "__main__":
    app.run(debug=True, threaded=True)#, host='0.0.0.0') # Запуск веб-приложения, с многопоточностью и с возможностью
    # слушать все внешние ip

