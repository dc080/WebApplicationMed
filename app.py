from flask import Flask, render_template, request, g, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

# import main
from main import Analysis

UPLOAD_FOLDER = 'static/image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///med.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

uploaded_image = ''
pic = UPLOAD_FOLDER + '/' + uploaded_image

# pic = 'static/image/pic.png'
answer = Analysis()
answerS = Analysis()

Border = {
    'light': 150,
    'dark': 150
}


# , Res=answer.FractAnalysis(pic), S=answerS.SquareNLinesAnalysis(pic, light, dark)) - Вывод в алгоритм


# class Article(db.Model):
#    id = db.Columd(db.Integer, primary_key=True)
#   picture = db.Columd(db.Integer)
@app.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('index.html', Res=answer.FractAnalysis(pic))  # answer.SquareNLinesAnalysis(pic, light, dark) +
    if request.method == "POST":
        try:
            file = request.files['file']
            Light = Border['light']
            Dark = Border['dark']
            light = int(Light)
            dark = int(Dark)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            uploaded_image = file.filename
            pic = UPLOAD_FOLDER + '/' + uploaded_image
            return render_template("index.html", pic=UPLOAD_FOLDER + '/' + uploaded_image, light=Border['light'],
                                   dark=Border['dark'],
                                   Res=answer.FractAnalysis(pic), S=answerS.SquareNLinesAnalysis(pic, light, dark))
        except FileNotFoundError:
            return render_template("index.html")
    else:
        return render_template("index.html")


@app.route('/number', methods=['GET', 'POST'])
def number():
    if request.method == 'POST':
        Border['light'] = request.form['light']
        Border['dark'] = request.form['dark']
        return render_template("index.html", light=Border['light'], dark=Border['dark'])
    else:
        return render_template("index.html")


# @app.route('/load', methods=['POST'])
# def load():
#   file = request.files['file']
#  filename = secure_filename(file.filename)
# file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
# uploaded_image = file.filename
#    pic = UPLOAD_FOLDER + '/' + uploaded_image
#   return render_template("index.html", uploaded_image=file.filename, Res=answer,
#                         S=answerS)
# else:


if __name__ == "__main__":
    app.run(debug=False)
