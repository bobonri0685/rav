import pytest

@pytest.mark.usefixtures("setup_user")
def test_get_alunos(client):
    response = client.get('/alunos')
    assert response.status_code == 200

@pytest.mark.usefixtures("setup_user")
def test_add_aluno(client):
    aluno_data = {'nome': 'New Student', 'other_required_field': 'value'}
    response = client.post('/alunos', json=aluno_data)
    assert response.status_code == 201, response.data

@pytest.mark.usefixtures("setup_user")
def test_update_aluno(client):
    aluno_data = {'nome': 'Initial Student', 'other_required_field': 'value'}
    response = client.post('/alunos', json=aluno_data)
    updated_data = {'nome': 'Updated Student', 'other_required_field': 'new_value'}
    response = client.put('/alunos/1', json=updated_data)
    assert response.status_code == 200, response.data

@pytest.mark.usefixtures("setup_user")
def test_delete_aluno(client):
    aluno_data = {'nome': 'Student to Delete', 'other_required_field': 'value'}
    response = client.post('/alunos', json=aluno_data)
    response = client.delete('/alunos/1')
    assert response.status_code == 204, response.data

@pytest.mark.usefixtures("setup_user")
def test_login(client):
    login_data = {'username': 'testuser', 'password': 'testpass'}
    response = client.post('/login', json=login_data)
    assert response.status_code == 200, response.data
    token = response.json.get('token')
    assert token is not None

@pytest.mark.usefixtures("setup_user")
def test_protected_route(client):
    login_response = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    token = login_response.json.get('token')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/protected', headers=headers)
    assert response.status_code == 200, response.data
