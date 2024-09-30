from flask_sqlalchemy import SQLAlchemy
from flask_session import Session


from settings import app, UPLOAD_FOLDER
from index import indexBp
from lines import linesBp
from algorithms import algorithmsBp

#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///med.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'someRandomKey'  # Какой-то секретный ключ, без которого нихера не работает
app.config['SESSION_TYPE'] = 'filesystem'  # Тип подключение сессии

Session(app)  # Запуск сессии в приложении
db = SQLAlchemy(app)

app.register_blueprint(indexBp)
app.register_blueprint(linesBp)
app.register_blueprint(algorithmsBp)

#@app.route('/lines/test', methods = ['POST'])
#def processLinesInfo():
#    global line
#    output = request.get_json()
#    print(output)
#    print(type(output))
#    result = json.loads(output)
#    print(result)
#    print(type(result))
#    line = str
#    return result

if __name__ == "__main__":
    app.run(debug=False, threaded=True, host='0.0.0.0')  # Запуск веб-приложения, с многопоточностью и с возможностью
    # слушать все внешние ip
