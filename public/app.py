from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bobonri:Onri0685@localhost/relatorio_avaliativo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para a tabela 'alunos'
class Aluno(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

# Rota para listar todos os alunos
@app.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    return jsonify([{'id': aluno.id, 'nome': aluno.nome} for aluno in alunos])

# Rota para adicionar um novo aluno
@app.route('/alunos', methods=['POST'])
def add_aluno():
    data = request.json
    nome = data['nome']
    novo_aluno = Aluno(nome=nome)
    db.session.add(novo_aluno)
    db.session.commit()
    return 'Aluno adicionado!', 201

# Rota para atualizar os dados de um aluno específico
@app.route('/alunos/<int:id>', methods=['PUT'])
def update_aluno(id):
    data = request.json
    aluno = Aluno.query.get(id)
    if aluno:
        aluno.nome = data['nome']
        db.session.commit()
        return 'Aluno atualizado!', 200
    return 'Aluno não encontrado!', 404

# Rota para deletar um aluno específico
@app.route('/alunos/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    aluno = Aluno.query.get(id)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
        return 'Aluno deletado!', 200
    return 'Aluno não encontrado!', 404

if __name__ == '__main__':
    app.run(debug=True)
