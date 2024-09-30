from flask import Blueprint, render_template, request, session,send_file, redirect, url_for, flash

import os
import shutil

from settings import verifySessionId, UPLOAD_FOLDER, calculateSavePath, calculatePathToSavedFile, saveFileNameIntoSession, calculatePathToEditedFile
from settings import app, calculatePathToSavedFile
#UPLOAD_FOLDER удалить?

indexBp = Blueprint('index_page', __name__, url_prefix='', template_folder='templates')

@indexBp.route('/', methods=['GET', 'POST'])
def index():
    if not os.path.exists(UPLOAD_FOLDER):  # Если пути нет
        os.makedirs(UPLOAD_FOLDER)  # Создать его
    verifySessionId()

    if request.method == "POST":
        try:
            return render_template("index.html")
        except Exception as e:
            app.logger.info(str(e))

    return render_template("index.html")  # Отрисовка веб-страницы


def saveImage(file):
    savePath = calculateSavePath(session['idSession'])
    if not os.path.exists(savePath):  # Если пути нет
        os.makedirs(savePath)  # Создать его
    else:
        files = os.listdir(UPLOAD_FOLDER + '/' + str(session['idSession']))
        if len(files) >= 1:
            shutil.rmtree(UPLOAD_FOLDER + '/' + str(session['idSession']))
            os.makedirs(savePath)  # Создать его

    session['originalFileName'] = file.filename
    fileToSave = os.path.join(savePath, file.filename)
    file.save(fileToSave)

@indexBp.route('/loadImageToAlgorithms', methods=['POST'])
def loadImageToAlgos(): #Проверки на наличие файла, ебаклак
    if request.method == "POST":
        saveImage(request.files['file'])
        return redirect(url_for('algorithms_page.algorithm'))
    #return render_template("index2.html", light=algoSquare.light, dark=algoSquare.dark)



@indexBp.route('/loadImageToLines', methods=['POST'])
def loadImageToLines(): #Проверки на наличие файла, ебаклак
    if request.method == "POST":
        saveImage(request.files['file'])
        return redirect(url_for('lines_page.lines'))




    #return render_template("index2.html", light=algoSquare.light, dark=algoSquare.dark)

    #         if "load" in request.form:  # Если нажата кнопка загрузки
    #             idSession = verifySessionId()  # Присвоение ID, если это надо
    #             savePath = calculateSavePath(idSession)  # Обозначение пути до загруженного файла
    #             if not os.path.exists(savePath):  # Если пути нет
    #                 os.makedirs(savePath)  # Создать его
    #             else:
    #                 files = os.listdir(UPLOAD_FOLDER + '/' + str(idSession))
    #                 if len(files) >= 1:
    #                     shutil.rmtree(UPLOAD_FOLDER + '/' + str(idSession))
    #                     os.makedirs(savePath)  # Создать его
    #             file = request.files['file']  # Запрос файла
    #             savedFile = os.path.join(savePath, file.filename)  # Путь до сохраняемого файла с его исходным названием
    #
    #             file.save(savedFile)  # Сохранение файла
    #             saveFileNameIntoSession(savedFile, idSession)  # Переименовка файла
    #             pic = calculatePathToSavedFile(idSession)  # Путь до сохраненного файла с новым названием
    #             #algoSquare.loadImage(pic)  # Загрузка изображения в алгоритм
    #             #if 'squareNumber' in session:  # Очистка результатов прошлых изображений
    #             #    session.pop('squareNumber')  # Удалить результат
    #             #if 'fractalNumber' in session:  # Очистка результатов прошлых изображений
    #             #    session.pop('fractalNumber')  # Удалить результат
    #             #session['fractalNumber'] = algoFract.resolveFractNumber(pic)  # Сохранение результата алгоритма в хэш
    #             return render_template("index2.html", uploaded_image=file.filename, contours=pic,
    #                                    #Res=session['fractalNumber'],
    #                                    light=algoSquare.light,
    #                                    dark=algoSquare.dark)  # Отрисовка веб-страницы
    #
    #         elif "edit" in request.form:  # Если нажата кнопка изменения
    #             light = int(request.form['light'])  # Считывание значения ползунков
    #             dark = int(request.form['dark'])  # -/-
    #             algoSquare.light = light  # Занесение значений в алгоритм
    #             algoSquare.dark = dark  # -/-
    #             algoSquare.editImage()  # Обработка изображения
    #             if 'squareNumber' in session:
    #                 session.pop('squareNumber')
    #             return render_template("index2.html", contours=calculatePathToEditedFile(session['idSession']),
    #                                    light=request.form['light'],
    #                                    dark=request.form['dark'],
    #                                    Res=session['fractalNumber'])  # Отрисовка веб-страницы
    #
    #         elif "runAlgo" in request.form:  # Если нажата кнопка запуска алгоритма
    #             light = int(request.form['light'])  # Считывание значения ползунков
    #             dark = int(request.form['dark'])  # -/-
    #             algoSquare.light = light  # Занесение значений в алгоритм
    #             algoSquare.dark = dark  # -/-
    #             algoSquare.editImage()  # Обработка изображения
    #             session['squareNumber'] = algoSquare.resolvePercent()  # Занесение значения площади в хэш
    #             return render_template("index2.html", contours=calculatePathToEditedFile(session['idSession']),
    #                                    light=request.form['light'], dark=request.form['dark'],
    #                                    Res=session['fractalNumber'],
    #                                    S=session['squareNumber'])  # Отрисовка веб-страницы
    #
    #         elif "orig" in request.form:  # Если нажата "радио"кнопка оригинала
    #             files = os.listdir(UPLOAD_FOLDER + '/' + str((session['idSession'])))
    #             if len(files) > 0:
    #                 savePath = calculatePathToSavedFile(session['idSession'])  # Путь к оригинальному файлу
    #                 if not 'fractalNumber' in session and not 'squareNumber' in session:  # Если нет результатов
    #                     return render_template("index2.html", contours=savePath, light=algoSquare.light,
    #                                            # Рендер без результатов
    #                                            dark=algoSquare.dark)
    #                 elif not 'squareNumber' in session:  # Если нет только площадей
    #                     return render_template("index2.html", contours=savePath, light=algoSquare.light,
    #                                            dark=algoSquare.dark,
    #                                            Res=session['fractalNumber'])  # Рендер с фрактальной
    #                 else:  # Есть все результаты
    #                     return render_template("index2.html", contours=savePath, light=algoSquare.light,
    #                                            dark=algoSquare.dark, Res=session['fractalNumber'],
    #                                            S=session['squareNumber'])  # Есть все результаты, рендер их
    #             else:
    #                 return render_template("index.html", contours="/static/static_image/not_found.png",
    #                                        light=algoSquare.light,
    #                                        dark=algoSquare.dark, )
    #
    #         elif "modifed" in request.form:  # Если нажата "радио"кнопка измененного
    #             files = os.listdir(UPLOAD_FOLDER + '/' + str((session['idSession'])))
    #             if len(files) > 1:
    #                 showPath = calculatePathToEditedFile(session['idSession'])  # Путь к измененному файлу
    #                 if not 'squareNumber' in session:  # Если нет площадей
    #                     return render_template("index2.html", contours=showPath, light=algoSquare.light,
    #                                            dark=algoSquare.dark,
    #                                            Res=session['fractalNumber'])  # Рендер с фрактальной
    #                 else:  # Есть все результаты
    #                     return render_template("index2.html", contours=showPath, light=algoSquare.light,
    #                                            dark=algoSquare.dark,
    #                                            Res=session['fractalNumber'],
    #                                            S=session['squareNumber'])  # Есть все результаты, рендер их
    #             else:
    #                 return render_template("index2.html", contours="/static/static_image/not_found.png",
    #                                        light=algoSquare.light,
    #                                        dark=algoSquare.dark)  # Рендер пустой страницы
    #
    #         elif "lines" in request.form:  # Если нажата "радио"кнопка линий
    #             return redirect(url_for('lines_page.lines', contours=calculatePathToSavedFile(session['idSession'])))
    #
    #
    #     except FileNotFoundError:
    #         flash('Выберите изображение')
    #         return render_template("index2.html", light=algoSquare.light, dark=algoSquare.dark)
    #     except IsADirectoryError:
    #         flash('Ошибка директории')
    #         return render_template("index2.html", light=algoSquare.light, dark=algoSquare.dark)
    #     except ValueError:
    #         savePath = calculatePathToSavedFile(session['idSession'])
    #         flash('Некорректное значение границ')
    #         if not 'squareNumber' in session:  # Если нет площадей
    #             return render_template("index2.html", contours=savePath, light=algoSquare.light, dark=algoSquare.dark,
    #                                    Res=session['fractalNumber'])  # Рендер с фрактальной
    #         else:  # Есть все результаты
    #             return render_template("index2.html", contours=savePath, light=algoSquare.light, dark=algoSquare.dark,
    #                                    Res=session['fractalNumber'],
    #                                    S=session['squareNumber'])  # Есть все результаты, рендер их
    #     #except Exception:
    #     #    flash('Что-то произошло')
    #     #    return render_template("index.html", light=algoSquare.light, dark=algoSquare.dark)
    #
    #     else:
    #         return render_template("index2.html")  # Отрисовка веб-страницы
    # else:
    #     files = os.listdir(UPLOAD_FOLDER)
    #     if len(files) > 150:  # Уже число близкое к реальному (Количество сейвов 200)
    #         shutil.rmtree(UPLOAD_FOLDER)
    #         os.mkdir(UPLOAD_FOLDER)

