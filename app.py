from flask import Flask, render_template, request, g, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from main import Analysis

UPLOAD_FOLDER = 'static/image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///med.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)

uploaded_image = ''
pic = UPLOAD_FOLDER + '/' + uploaded_image

answer = Analysis()
answerS = Analysis()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        try:
            file = request.files['file']
            Light = request.form['light']
            Dark = request.form['dark']
            light = int(Light)
            dark = int(Dark)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            uploaded_image = file.filename
            pic = UPLOAD_FOLDER + '/' + uploaded_image
            return render_template("index.html", pic=UPLOAD_FOLDER + '/' + uploaded_image, uploaded_image=file.filename,
                                   light=request.form['light'],
                                   dark=request.form['dark'],
                                   Res=answer.FractAnalysis(pic), S=answerS.SquareNLinesAnalysis(pic, light, dark))
        except FileNotFoundError:
            flash('Выберите изображение')
            return render_template("index.html")
        except IsADirectoryError:
            flash('Выберите изображение')
            return render_template("index.html")
        except ValueError:
            flash('Некорректное значение границ')
            return render_template("index.html")


    else:
        files = os.listdir(UPLOAD_FOLDER)
        if len(files) > 50:
            for f in os.listdir(UPLOAD_FOLDER):
                os.remove(os.path.join(UPLOAD_FOLDER, f))
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)

# @app.route('/number', methods=['GET', 'POST'])
# def number():
#   if request.method == 'POST':
#      Border['light'] = request.form['light']
#     Border['dark'] = request.form['dark']
#    return render_template("index.html", light=Border['light'], dark=Border['dark'])
# else:
#    return render_template("index.html")


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

# class Article(db.Model):
#    id = db.Columd(db.Integer, primary_key=True)
#   picture = db.Columd(db.Integer)
