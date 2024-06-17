import pytest
from app import app, db, User

@pytest.fixture(scope='function')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def setup_user(client):
    with app.app_context():
        user = User(username='testuser', password='testpass')  # Verifique a lógica de hashing da senha se necessário
        db.session.add(user)
        db.session.commit()
        login_data = {'username': 'testuser', 'password': 'testpass'}
        response = client.post('/login', json=login_data)
        assert response.status_code == 200, response.data
        token = response.json.get('token')
        client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
