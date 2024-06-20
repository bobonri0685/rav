import React, { useState } from 'react';
import axios from 'axios';

const Cadastro: React.FC = () => {
  const [nome, setNome] = useState('');
  const [idade, setIdade] = useState('');
  const [serie, setSerie] = useState('');
  const [mensagem, setMensagem] = useState('');
  const [erro, setErro] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await axios.post('/api/alunos', { nome, idade: parseInt(idade), serie });
      setMensagem(response.data.message);
      setErro(''); // Limpa a mensagem de erro
      // Limpar o formulário após o cadastro
      setNome('');
      setIdade('');
      setSerie('');
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        setErro(error.response.data.message);
      } else {
        setErro('Erro ao cadastrar aluno.');
      }
      setMensagem(''); // Limpa a mensagem de sucesso
    }
  };

  return (
    <div>
      <h2>Cadastro de Aluno</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="nome">Nome:</label>
          <input type="text" id="nome" value={nome} onChange={(e) => setNome(e.target.value)} required />
        </div>
        <div>
          <label htmlFor="idade">Idade:</label>
          <input type="number" id="idade" value={idade} onChange={(e) => setIdade(e.target.value)} required />
        </div>
        <div>
          <label htmlFor="serie">Série:</label>
          <input type="text" id="serie" value={serie} onChange={(e) => setSerie(e.target.value)} required />
        </div>
        <button type="submit">Cadastrar</button>
      </form>
      {mensagem && <p className="success">{mensagem}</p>}
      {erro && <p className="error">{erro}</p>}
    </div>
  );
};

export default Cadastro;