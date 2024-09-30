from flask import Blueprint, render_template, session, request, send_file, json

import os
import shutil

from settings import calculatePathToSavedFile, calculatePathToEditedFile, app
from Algorithms.FindFractNumber import FindFractNumber
from Algorithms.FindSquareCrystals import FindSquareCrystals

algoFract = FindFractNumber()
algoSquare = FindSquareCrystals()

algorithmsBp = Blueprint('algorithms_page', __name__, url_prefix='/algorithms', static_folder='static', template_folder='templates')

@algorithmsBp.route('/', methods=['GET', 'POST'])
def algorithm():
    reset()
    return render_template("algorithms.html", img=calculatePathToSavedFile(session['idSession']), light=algoSquare.light, dark=algoSquare.dark)


@algorithmsBp.route('/getOrigImg', methods=['GET'])
def sendOrigImg():
    if request.method == "GET":
        return send_file(calculatePathToSavedFile(session['idSession']), mimetype='image/jpg')

@algorithmsBp.route('/getEditImg', methods=['GET'])
def sendEditImg():
    if request.method == "GET":
        return send_file(calculatePathToEditedFile(session['idSession']), mimetype='image/jpg')

@algorithmsBp.route('/editImage', methods=['POST'])
def editImage():
    light = int(request.json['light'])
    dark = int(request.json['dark'])
    algoSquare.light = light
    algoSquare.dark = dark
    algoSquare.editImage()
    return "succ"

@algorithmsBp.route('/runAlgorithm', methods=['POST'])
def runAlgorithms():
    light = int(request.json['light'])
    dark = int(request.json['dark'])
    algoSquare.light = light
    algoSquare.dark = dark
    algoSquare.editImage()
    borders = [light, dark]
    app.logger.info('startSquare')
    persentSquare = algoSquare.resolvePercent()
    app.logger.info('endSquareStartFract')
    fractNumber = algoFract.resolveFractNumber(calculatePathToSavedFile(session['idSession']))
    app.logger.info('endFract')
    respondJson = json.dumps({'Borders': borders, 'fractNumber': fractNumber, 'percentSquare': persentSquare})
    return respondJson

def reset():
    algoSquare.light = 150
    algoSquare.dark = 200
    algoSquare.loadImage(calculatePathToSavedFile(session['idSession']))
    if os.path.exists(calculatePathToEditedFile(session['idSession'])):
        os.remove(calculatePathToEditedFile(session['idSession']))
    shutil.copy(calculatePathToSavedFile(session['idSession']), calculatePathToEditedFile(session['idSession']))