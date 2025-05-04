from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, User

app = Flask(__name__, template_folder="../frontend/", static_folder="../frontend/")
app.config.from_object(Config)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
bcrypt = Bcrypt(app)   
jwt = JWTManager(app)   
CORS(app, resources={r"/*": {"origins": "*"}})

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()

        # Проверка пароля
        if not user or not bcrypt.check_password_hash(user.password, data.get('password')):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Генерация JWT
        access_token = create_access_token(identity=user.username)
        return jsonify({'token': access_token}), 200
    return render_template('login.html')


@app.route('/profile')
@jwt_required()
def serve_profile_page():
    current_user = get_jwt_identity()
    return render_template('profile.html', user=current_user), 200

@app.route('/')
def redirect_to_login():
    return redirect("/login")


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Режим отладки