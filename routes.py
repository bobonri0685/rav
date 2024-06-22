from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from models import Aluno, db
from schemas import AlunoSchema

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

aluno_schema = AlunoSchema()

aluno_model = api.model('Aluno', {
    'id': fields.Integer(readOnly=True, description='ID do aluno'),
    'nome': fields.String(required=True, description='Nome do aluno'),
    'idade': fields.Integer(required=True, description='Idade do aluno'),
    'serie': fields.String(required=True, description='Série do aluno')
})

@api.route('/alunos')
class AlunoList(Resource):
    @jwt_required()
    @api.marshal_list_with(aluno_model)
    def get(self):
        alunos = Aluno.query.all()
        return alunos

    @jwt_required()
    @api.expect(aluno_model, validate=True)
    @api.response(201, 'Aluno adicionado')
    @api.response(400, 'Validation Error')
    def post(self):
        try:
            data = request.json
            aluno_schema.load(data)  # Validação dos dados
            novo_aluno = Aluno(nome=data['nome'], idade=data['idade'], serie=data['serie'])
            db.session.add(novo_aluno)
            db.session.commit()
            return {'message': 'Aluno adicionado!'}, 201
        except ValidationError as err:
            return {'message': str(err)}, 400

@api.route('/alunos/<int:id>')
class AlunoResource(Resource):
    @jwt_required()
    @api.marshal_with(aluno_model)
    @api.response(200, 'Success')
    @api.response(404, 'Aluno não encontrado')
    def get(self, id):
        aluno = Aluno.query.get(id)
        if aluno:
            return aluno_schema.dump(aluno), 200
        return {'message': 'Aluno não encontrado'}, 404

    @jwt_required()
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
                return {'message': 'Aluno atualizado!'}, 200
            return {'message': 'Aluno não encontrado!'}, 404
        except ValidationError as err:
            return {'message': str(err)}, 400

    @jwt_required()
    @api.response(204, 'Aluno deletado')
    @api.response(404, 'Aluno não encontrado')
    def delete(self, id):
        aluno = db.session.get(Aluno, id)
        if aluno:
            db.session.delete(aluno)
            db.session.commit()
            return '', 204
        return {'message': 'Aluno não encontrado!'}, 404
