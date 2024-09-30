from flask import Blueprint, request, redirect, url_for, render_template, json, session, send_file

import os
import shutil

from settings import calculatePathToSavedFile, calculatePathToLineFile
from Algorithms.DrawLines import DrawLines
from settings import app

algoDrawLines = DrawLines()
arrLines = list()

linesBp = Blueprint('lines_page', __name__, url_prefix='/lines', static_folder='static', template_folder='templates')

@linesBp.route('/', methods=['GET', 'POST'])
def lines():
    reset()
    return render_template("lines.html", contours=calculatePathToSavedFile(session['idSession']))

@linesBp.route('/getJSON', methods=['POST'])
def ProcessLinesInfo():
    global arrLines
    if request.method == "POST":
        firstPoint = request.json['firstPoint']
        secondPoint = request.json['secondPoint']

        pic = calculatePathToLineFile(session['idSession'])
        line = [firstPoint, secondPoint]
        arrLines.append(line)
        algoDrawLines.drawLine(pic, firstPoint, secondPoint, pic)
        #respondJson = json.dumps({'line_length': algoDrawLines.length_l, 'lines_length': algoDrawLines.length_arr})
        return generateResponse(algoDrawLines.length_l, algoDrawLines.length_arr)
    return render_template("lines.html", contours=calculatePathToSavedFile(session['idSession']))


@linesBp.route('/popJSON', methods=['POST'])
def popSomeLine():
    global arrLines
    if request.method == "POST":
        if len(arrLines) > 20:
            deletealllines()
        elif len(arrLines) != 0:
            arrLines.pop()
            algoDrawLines.clearLengthArr()
            redrawLines()
        try:
            #respondJson = json.dumps({'line_length': '-', 'lines_length': algoDrawLines.length_arr})
            return generateResponse('-',algoDrawLines.length_arr)
        except Exception as e:
            app.logger.info(str(e), 400)

def redrawLines():
    if os.path.exists(calculatePathToLineFile(session['idSession'])):
        os.remove(calculatePathToLineFile(session['idSession']))
        shutil.copy(calculatePathToSavedFile(session['idSession']), calculatePathToLineFile(session['idSession']))
    pic = calculatePathToLineFile(session['idSession'])
    for line in arrLines:
        algoDrawLines.drawLine(pic, line[0], line[1], pic)
        #app.logger.info(str(line[0]) + "   " + str(line[1]))

@linesBp.route('/getimg', methods=['GET'])
def sendimg():
    #app.logger.info("lol, request just droped")
    if request.method == "GET":
        try:
            #app.logger.info('sendimg')
            return send_file(calculatePathToLineFile(session['idSession']), mimetype='image/jpg')
        except Exception as e:
            app.logger.info(str(e), 400)

def reset():
    global arrLines
    algoDrawLines.clearLengthArr()
    arrLines.clear()
    if os.path.exists(calculatePathToLineFile(session['idSession'])):
        os.remove(calculatePathToLineFile(session['idSession']))

    #app.logger.info(calculatePathToSavedFile(session['idSession']))
    #app.logger.info(calculatePathToLineFile(session['idSession']))
    shutil.copy(calculatePathToSavedFile(session['idSession']), calculatePathToLineFile(session['idSession']))

def generateResponse(lenghtLine, lenghtLines):
    linesLenght = "<br>".join(str(element) for element in lenghtLines)
    respondJson = json.dumps({'line_length': lenghtLine, 'lines_length': linesLenght})
    return respondJson


@linesBp.route('/deleteAll', methods=['POST'])
def deletealllines():
    reset()
    app.logger.info(calculatePathToLineFile(session['idSession']))
    return send_file(calculatePathToLineFile(session['idSession']), mimetype='image/jpg')