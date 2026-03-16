from flask import Flask
from config import Config
from models import db
from routes.auth import auth
from routes.users import users
from routes.transactions import transactions
from flask_jwt_extended import JWTManager
from extensions import bcrypt,jwt


#configuring the 
app = Flask(__name__)
app.config.from_object(Config) # Loads all settings from config.py

db.init_app(app) #conecting SQLAlchemy to app
bcrypt.init_app(app) #Initializing Bcrypt to app
jwt.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(users)
app.register_blueprint(transactions)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)

