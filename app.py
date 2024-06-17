from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_restx import Api, Resource, fields
from marshmallow import Schema, fields as ma_fields, validate, ValidationError
from flask_migrate import Migrate
import os
import logging

# Configuração do logging
from src.logging_config import setup_logging
setup_logging()

logger = logging.getLogger(__name__)

# Criação da aplicação Flask
app = Flask(__name__, template_folder='src/templates', static_folder='src/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://diogomendesbatista:onri0685@localhost/relatorio_avaliativo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Armazene a chave secreta em uma variável de ambiente
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua_chave_secreta_padrao') 

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

api = Api(app, version='1.0', title='API de Relatório Avaliativo', 
          description='Documentação da API de Relatório Avaliativo', doc='/api/docs')

migrate = Migrate(app, db)

# Modelos
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Schemas
class AlunoSchema(Schema):
    nome = ma_fields.String(required=True, validate=validate.Length(min=1))
    other_required_field = ma_fields.String(required=True)

aluno_schema = AlunoSchema()

# Modelos para Swagger
aluno_model = api.model('Aluno', {
    'id': fields.Integer(readOnly=True, description='ID do aluno'),
    'nome': fields.String(required=True, description='Nome do aluno')
})

user_model = api.model('User', {
    'username': fields.String(required=True, description='Nome de usuário'),
    'password': fields.String(required=True, description='Senha')
})

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Adicionando rotas para renderizar templates HTML
@app.route('/index')
def index():
    return render_template('index.html')
    
@api.route('/login')
class Login(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'Success')
    @api.response(401, 'Invalid credentials')
    def post(self):
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and user.verify_password(data['password']):
            login_user(user)
            token = 'dummy_token' 
            logger.info(f'Usuário {user.username} logado com sucesso.')
            return {'token': token}, 200
        logger.warning('Tentativa de login com credenciais inválidas.')
        return {'message': 'Invalid credentials'}, 401


    def get(self):  # Adiciona o método GET para exibir o formulário
        return render_template('index.html') 

@api.route('/logout')
class Logout(Resource):
    @login_required
    def get(self):
        logout_user()
        logger.info(f'Usuário {current_user.username} deslogado com sucesso.')
        return {'message': 'Logout successful'}, 200

@api.route('/alunos')
class AlunoList(Resource):
    @login_required
    @api.marshal_list_with(aluno_model)
    def get(self):
        alunos = Aluno.query.all()
        logger.debug(f'{len(alunos)} alunos encontrados.')
        return alunos

    @login_required
    @api.expect(aluno_model, validate=True)
    @api.response(201, 'Aluno adicionado')
    @api.response(400, 'Validation Error')
    def post(self):
        try:
            data = request.json
            aluno_schema.load(data)  # Validação dos dados
            novo_aluno = Aluno(nome=data['nome'])
            db.session.add(novo_aluno)
            db.session.commit()
            logger.info(f'Aluno {data["nome"]} adicionado com sucesso.')
            return {'message': 'Aluno adicionado!'}, 201
        except ValidationError as err:
            logger.error(f'Erro de validação ao adicionar aluno: {err}')
            return {'message': str(err)}, 400

@api.route('/alunos/<int:id>')
class AlunoResource(Resource):
    @login_required
    @api.marshal_with(aluno_model)
    @api.response(200, 'Success')
    @api.response(404, 'Aluno não encontrado')
    def get(self, id):
        aluno = db.session.get(Aluno, id)
        if aluno:
            logger.debug(f'Aluno encontrado: {aluno.nome}')
            return aluno, 200
        logger.warning(f'Aluno com ID {id} não encontrado.')
        return {'message': 'Aluno não encontrado'}, 404

    @login_required
    @api.expect(aluno_model, validate=True)
    @api.response(200, 'Aluno atualizado')
    @api.response(404, 'Aluno não encontrado')
    @api.response(400, 'Validation Error')
    def put(self, id):
        try:
            data = request.json
            aluno = db.session.get(Aluno, id)
            if aluno:
                aluno_schema.load(data)  # Validação dos dados
                aluno.nome = data['nome']
                db.session.commit()
                logger.info(f'Aluno {id} atualizado com sucesso.')
                return {'message': 'Aluno atualizado!'}, 200
            logger.warning(f'Aluno com ID {id} não encontrado.')
            return {'message': 'Aluno não encontrado!'}, 404
        except ValidationError as err:
            logger.error(f'Erro de validação ao atualizar aluno: {err}')
            return {'message': str(err)}, 400

    @login_required
    @api.response(204, 'Aluno deletado')
    @api.response(404, 'Aluno não encontrado')
    def delete(self, id):
        aluno = db.session.get(Aluno, id)
        if aluno:
            db.session.delete(aluno)
            db.session.commit()
            logger.info(f'Aluno {id} deletado com sucesso.')
            return '', 204
        logger.warning(f'Aluno com ID {id} não encontrado.')
        return {'message': 'Aluno não encontrado!'}, 404

@app.errorhandler(404)
def not_found(error):
    logger.error('Erro 404: Página não encontrada.')
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(403)
def forbidden(error):
    logger.error('Erro 403: Acesso proibido.')
    return jsonify({'error': 'Forbidden'}), 403

@app.errorhandler(500)
def internal_error(error):
    logger.error('Erro 500: Erro interno do servidor.', exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/protected')
@login_required
def protected():
    logger.debug(f'Usuário {current_user.username} acessou a rota protegida.')
    return jsonify({'message': 'This is a protected route'}), 200

if __name__ == '__main__':
    logger.info('Iniciando a aplicação Flask.')
    app.run(debug=True)

