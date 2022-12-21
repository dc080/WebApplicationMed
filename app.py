from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

import main
from main import Analysis

UPLOAD_FOLDER = 'styles/image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///med.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

pic = 'styles/image/pic.png'

light = 200
dark = 150

answer = Analysis()





# class Article(db.Model):
#    id = db.Columd(db.Integer, primary_key=True)
#   picture = db.Columd(db.Integer)
@app.route('/', methods=['GET', 'POST'])
def index():
    return answer.SquareNLinesAnalysis(pic, light, dark) + answer.FractAnalysis(pic)
    #if request.method == 'POST':
      #  file = request.files['file']
        #filename = secure_filename(file.filename)
      #  file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
     #   return render_template("index.html", uploaded_image=file.filename)
    #else:
     #   return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)
