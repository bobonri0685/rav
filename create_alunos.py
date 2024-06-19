from app import app, db, Aluno

def create_alunos():
    with app.app_context(): 
        alunos = [
            Aluno(nome='João Silva', idade=15, serie='9º ano'),
            Aluno(nome='Maria Souza', idade=14, serie='8º ano'),
            Aluno(nome='Pedro Santos', idade=16, serie='1º ano')
        ]

        db.session.add_all(alunos)
        db.session.commit()

    print("Alunos adicionados com sucesso!")

if __name__ == '__main__':
    create_alunos()