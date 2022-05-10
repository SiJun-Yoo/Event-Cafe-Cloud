from flask import Flask
import jwt
from database import DB

app = Flask(__name__)
DB()

from controller import auth_controller, main_controller, cafe_controller, user_controller

app.register_blueprint(auth_controller.bp)
app.register_blueprint(main_controller.bp)
app.register_blueprint(cafe_controller.bp)
app.register_blueprint(user_controller.bp)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

