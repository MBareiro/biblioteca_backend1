from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20ff7'

login_manager = LoginManager(app)
login_manager.login_view = "login"

CORS(app)

# Configurar la base de datos
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/biblioteca'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://upmccthrkujatdmu:VBD9SeGJRSOyLYbzlf6J@beebvr4gtvujymlza7qh-mysql.services.clever-cloud.com:3306/beebvr4gtvujymlza7qh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate()
migrate.init_app(app, db) 
# Define las rutas utilizando el controlador de usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def hello():
    return jsonify(message='¡Hola mundo!')

#Comentar en pythonanywhere
from controllers.reset_password import *

# Descomentar en pythonanywhere 

from controllers import usuario_controller, login_controller, proveedor_controller, beneficiary_controller, book_controller, author_controller, reset_password, genre_controller, editorial_controller, loan_controller, suscription_controller

if __name__ == '__main__':    
    app.run(host='0.0.0.0')
