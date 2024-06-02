document.addEventListener('DOMContentLoaded', function() {
    const classList = document.querySelector('.class-list');

    // Exemplo de dados. Em um cenário real, você buscaria isso de uma API.
    const classes = [
        {
            name: 'Turma A',
            students: ['Aluno 1', 'Aluno 2', 'Aluno 3']
        },
        {
            name: 'Turma B',
            students: ['Aluno 4', 'Aluno 5', 'Aluno 6']
        }
        // Adicione mais turmas e alunos aqui
    ];

    // Função para criar os elementos da turma e dos alunos
    function renderClasses() {
        classes.forEach(classData => {
            const classItem = document.createElement('li');
            classItem.classList.add('class-item');

            const classTitle = document.createElement('h3');
            classTitle.textContent = classData.name;
            classItem.appendChild(classTitle);

            const studentList = document.createElement('ul');
            studentList.classList.add('student-list');
            classData.students.forEach(student => {
                const studentItem = document.createElement('li');
                studentItem.textContent = student;
                studentList.appendChild(studentItem);
            });

            classItem.appendChild(studentList);
            classList.appendChild(classItem);
        });
    }

    renderClasses();
});
