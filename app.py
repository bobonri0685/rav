from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect, CSRFError  # Importa CSRFError
from flask_restx import Api, Resource, fields
from marshmallow import Schema, fields as ma_fields, validate, ValidationError
from flask_migrate import Migrate
from src.forms import LoginForm
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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua_chave_secreta_padrao')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index' 

api = Api(app, version='1.0', title='API de Relatório Avaliativo', 
          description='Documentação da API de Relatório Avaliativo', doc='/api/docs')

migrate = Migrate(app, db)


# Modelos
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    serie = db.Column(db.String(100), nullable=False)

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
    idade = ma_fields.Integer(required=True, validate=validate.Range(min=1))
    serie = ma_fields.String(required=True, validate=validate.Length(min=1))  

aluno_schema = AlunoSchema()

# Modelos para Swagger
aluno_model = api.model('Aluno', {
    'id': fields.Integer(readOnly=True, description='ID do aluno'),
    'nome': fields.String(required=True, description='Nome do aluno'),
    'idade': fields.Integer(required=True, description='Idade do aluno'),
    'serie': fields.String(required=True, description='Série do aluno')
})

user_model = api.model('User', {
    'username': fields.String(required=True, description='Nome de usuário'),
    'password': fields.String(required=True, description='Senha')
})

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/public/<path:filename>')
def serve_public(filename):
    return send_from_directory('public', filename)

# Adicionando rotas para renderizar templates HTML
@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()  # Crie uma instância do formulário
    return render_template('index.html', form=form)  # Passe o formulário para o template
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Usa validate_on_submit para verificar o token CSRF
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            logger.warning(f'Falha no login para o usuário {username}.')
            return render_template('index.html', form=form, error='Credenciais inválidas.')
    else:
        return render_template('index.html', form=form)

   
# Rota do Dashboard (protegida)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

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
    @csrf.exempt
    def post(self):
        try:
            data = request.json
            aluno_schema.load(data)  # Validação dos dados
            novo_aluno = Aluno(nome=data['nome'], idade=data['idade'], serie=data['serie'])
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
        try:
            aluno = Aluno.query.get(id)
            if aluno:
                logger.info(f'Aluno encontrado (ID: {id}, Nome: {aluno.nome})')
                return aluno_schema.dump(aluno), 200
            else:
                logger.warning(f'Aluno não encontrado (ID: {id})')
                return {'message': 'Aluno não encontrado'}, 404
        except Exception as e:
            logger.error(f'Erro ao buscar aluno (ID: {id}): {e}', exc_info=True)  
            return {'message': 'Erro interno do servidor'}, 500

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
                aluno.idade = data['idade']
                aluno.serie = data['serie']
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

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f'Erro inesperado: {error}', exc_info=True)
    if isinstance(error, ValidationError):
        return jsonify({'error': 'Validation Error', 'messages': error.messages}), 400
    elif isinstance(error, IntegrityError):
        return jsonify({'error': 'Integrity Error'}), 400
    else:
        return jsonify({'error': 'Internal Server Error'}), 500

    
@app.route('/protected')
@login_required
def protected():
    logger.debug(f'Usuário {current_user.username} acessou a rota protegida.')
    return jsonify({'message': 'This is a protected route'}), 200

def create_admin_user():
    admin_username = 'admin'
    admin_password = 'onri0685'
    if not User.query.filter_by(username=admin_username).first():
        admin_user = User(username=admin_username)
        admin_user.password = admin_password
        db.session.add(admin_user)
        db.session.commit()
        logger.info('Usuário admin criado com sucesso.')
    else:
        logger.info('Usuário admin já existe.')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
    logger.info('Iniciando a aplicação Flask.')
    app.run(debug=True)
