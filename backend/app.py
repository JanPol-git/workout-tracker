from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
bcrypt = Bcrypt(app)   
jwt = JWTManager(app)   


with app.app_context():
    db.create_all()


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Проверка
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    # Хеширование
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    
    # Сохранение
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()

    # Проверка пароля
    if not user or not bcrypt.check_password_hash(user.password, data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Генерация JWT
    access_token = create_access_token(identity=user.username)
    return jsonify({'token': access_token}), 200

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity() 
    return jsonify({'user': current_user}), 200





if __name__ == '__main__':
    app.run(debug=True)  # Режим отладки

