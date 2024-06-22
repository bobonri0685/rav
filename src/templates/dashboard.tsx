import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles.css';

interface Student {
  id: number;
  name: string;
  age: number;
  grade: string;
}

const Dashboard: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [selectedStudent, setSelectedStudent] = useState<number | null>(null);
  const [showModal, setShowModal] = useState<string | null>(null);
  const [studentData, setStudentData] = useState<Student>({ id: 0, name: '', age: 0, grade: '' });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStudents();
  }, []);

  const loadStudents = async () => {
    try {
      const response = await axios.get('/api/students');
      setStudents(response.data);
    } catch (error) {
      setError('Erro ao carregar estudantes. Por favor, tente novamente mais tarde.');
    }
  };

  const handleOpenModal = (mode: string) => {
    setShowModal(mode);
    if (mode === 'edit' && selectedStudent !== null) {
      const student = students.find(s => s.id === selectedStudent);
      if (student) {
        setStudentData(student);
      }
    } else {
      setStudentData({ id: 0, name: '', age: 0, grade: '' });
    }
  };

  const handleCloseModal = () => {
    setShowModal(null);
    setError(null);
  };

  const handleStudentChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedStudent(Number(e.target.value));
  };

  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setStudentData({ ...studentData, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (showModal === 'add') {
        await axios.post('/api/students', studentData);
      } else if (showModal === 'edit') {
        await axios.put(`/api/students/${selectedStudent}`, studentData);
      }
      loadStudents();
      handleCloseModal();
    } catch (error) {
      setError('Erro ao salvar estudante. Por favor, verifique os dados e tente novamente.');
    }
  };

  const handleDelete = async () => {
    try {
      await axios.delete(`/api/students/${selectedStudent}`);
      loadStudents();
      handleCloseModal();
    } catch (error) {
      setError('Erro ao excluir estudante. Por favor, tente novamente mais tarde.');
    }
  };

  return (
    <div>
      <header>
        <h1>Dashboard de Avaliação</h1>
        <nav>
          <button onClick={() => handleOpenModal('add')}>Cadastrar Novo Aluno</button>
          <button onClick={() => handleOpenModal('edit')}>Editar Aluno</button>
          <button onClick={() => setShowModal('delete')}>Excluir Aluno</button>
        </nav>
      </header>

      <main>
        <section id="student-selection">
          <h2>Escolha um Estudante para Avaliar</h2>
          <select id="student-list" onChange={handleStudentChange} value={selectedStudent ?? ''}>
            <option value="" disabled>Selecione um estudante</option>
            {students.map(student => (
              <option key={student.id} value={student.id}>
                {student.name}
              </option>
            ))}
          </select>
        </section>

        <section id="student-details">
          <h2>Detalhes do Estudante</h2>
          <div id="student-info">
            {selectedStudent !== null && (
              <>
                <p>Nome: {students.find(s => s.id === selectedStudent)?.name}</p>
                <p>Idade: {students.find(s => s.id === selectedStudent)?.age}</p>
                <p>Série: {students.find(s => s.id === selectedStudent)?.grade}</p>
              </>
            )}
          </div>
        </section>
      </main>

      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <span className="close-btn" onClick={handleCloseModal}>&times;</span>
            {showModal !== 'delete' ? (
              <>
                <h2>{showModal === 'add' ? 'Adicionar Estudante' : 'Editar Estudante'}</h2>
                <form id="student-form" onSubmit={handleSubmit}>
                  <label htmlFor="student-name">Nome:</label>
                  <input
                    type="text"
                    id="student-name"
                    name="name"
                    value={studentData.name}
                    onChange={handleFormChange}
                    required
                  />
                  <label htmlFor="student-age">Idade:</label>
                  <input
                    type="number"
                    id="student-age"
                    name="age"
                    value={studentData.age}
                    onChange={handleFormChange}
                    required
                  />
                  <label htmlFor="student-grade">Série:</label>
                  <input
                    type="text"
                    id="student-grade"
                    name="grade"
                    value={studentData.grade}
                    onChange={handleFormChange}
                    required
                  />
                  <button type="submit">Salvar</button>
                </form>
                {error && <p className="error">{error}</p>}
              </>
            ) : (
              <>
                <h2>Confirmar Exclusão</h2>
                <p>Tem certeza que deseja excluir este estudante?</p>
                <button onClick={handleDelete}>Excluir</button>
                <button onClick={handleCloseModal}>Cancelar</button>
                {error && <p className="error">{error}</p>}
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
