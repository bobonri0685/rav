from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_restx import Api, Resource, fields
from marshmallow import Schema, fields as ma_fields, validate, ValidationError
from flask_migrate import Migrate

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://diogomendesbatista:onri0685@localhost/relatorio_avaliativo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
api = Api(app, version='1.0', title='API de Relatório Avaliativo', description='Documentação da API de Relatório Avaliativo')

# Configuração do Flask-Migrate
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
            token = 'dummy_token'  # Simule a criação de um token
            return {'token': token}, 200
        return {'message': 'Invalid credentials'}, 401

@api.route('/logout')
class Logout(Resource):
    @login_required
    def get(self):
        logout_user()
        return {'message': 'Logout successful'}, 200

@api.route('/alunos')
class AlunoList(Resource):
    @login_required
    @api.marshal_list_with(aluno_model)
    def get(self):
        alunos = Aluno.query.all()
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
            return {'message': 'Aluno adicionado!'}, 201
        except ValidationError as err:
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
            return aluno, 200
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
                return {'message': 'Aluno atualizado!'}, 200
            return {'message': 'Aluno não encontrado!'}, 404
        except ValidationError as err:
            return {'message': str(err)}, 400

    @login_required
    @api.response(204, 'Aluno deletado')
    @api.response(404, 'Aluno não encontrado')
    def delete(self, id):
        aluno = db.session.get(Aluno, id)
        if aluno:
            db.session.delete(aluno)
            db.session.commit()
            return '', 204
        return {'message': 'Aluno não encontrado!'}, 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/protected')
@login_required
def protected():
    return jsonify({'message': 'This is a protected route'}), 200

if __name__ == '__main__':
    app.run(debug=True)
