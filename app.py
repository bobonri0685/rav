import logging
import os

from flask import Flask, send_from_directory, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, CSRFError

# Importações do projeto
from auth import auth_bp, create_admin_user
from models import db, Aluno, User
from routes import api_bp
from src.py.logging_config import setup_logging

# Configuração do logging
setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='build/static')


# Configurações
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://diogomendesbatista:onri0685@localhost/relatorio_avaliativo_db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))  # Gera uma chave aleatória se não estiver definida
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', os.urandom(24))  # Gera uma chave aleatória se não estiver definida


# Inicialização de extensões
db.init_app(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
jwt = JWTManager(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

api = Api(app, version='1.0', title='API de Relatório Avaliativo',
          description='Documentação da API de Relatório Avaliativo', doc='/api/docs')

migrate = Migrate(app, db)

app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Adicionando rotas para renderizar templates HTML

# Rota para servir o frontend React
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("build/" + path):
        return send_from_directory('build', path)
    else:
        return send_from_directory('build', 'index.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return send_from_directory('build', 'index.html') # Renderiza a pagina raiz do react, que deverá ter o tratamento de erro 404

@app.errorhandler(403)
def forbidden(error):
    return send_from_directory('build', 'index.html') # Renderiza a pagina raiz do react, que deverá ter o tratamento de erro 403

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return send_from_directory('build', 'index.html') # Renderiza a pagina raiz do react, que deverá ter o tratamento de erro CSRFError

@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f'Erro inesperado: {error}', exc_info=True)
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    logger.info('Iniciando a aplicação Flask.')
    app.run(debug=True)

CORS(app, resources={r"/alunos/*": {"origins": "http://localhost:3000"}})
