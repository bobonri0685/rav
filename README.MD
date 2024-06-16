# Documentação da API

## Introdução
Esta documentação descreve as rotas disponíveis na API e como usá-las. A API foi desenvolvida utilizando Flask 
e PostgreSQL como banco de dados.

## Rotas

### 1. Rota de Autenticação

#### Registro de Usuário
- **Endpoint:** `/api/register`
- **Método:** `POST`
- **Descrição:** Registra um novo usuário.
- **Parâmetros:**
  - `username` (string): Nome de usuário.
  - `password` (string): Senha do usuário.
- **Exemplo de Requisição:**
  ```sh
  curl -X POST http://localhost:5000/api/register -H "Content-Type: application/json" -d '{"username": 
"example", "password": "examplepassword"}'

## Logins de usuarios
curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d '{"username": "example", 
"password": "examplepassword"}'

## Rota de dados do estudante
curl -X GET http://localhost:5000/api/students

## Adicionar novo estudante
curl -X POST http://localhost:5000/api/students -H "Content-Type: application/json" -d '{"name": "John Doe", 
"age": 12, "grade": "7th"}'

## Destalhe de um estudante
curl -X GET http://localhost:5000/api/students/1

## Atualizar informacao de um estudante
curl -X PUT http://localhost:5000/api/students/1 -H "Content-Type: application/json" -d '{"name": "John Doe", 
"age": 13, "grade": "8th"}'

## Deletar um estudante
curl -X DELETE http://localhost:5000/api/students/1
