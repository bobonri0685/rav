// scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const formAvaliacao = document.getElementById('formAvaliacao');
    const evaluationList = document.getElementById('evaluations');

    formAvaliacao.addEventListener('submit', function(event) {
        event.preventDefault();

        const studentName = document.getElementById('studentName').value;
        const subject = document.getElementById('subject').value;
        const grade = document.getElementById('grade').value;

        if (validateEvaluationForm(studentName, subject, grade)) {
            const evaluation = {
                studentName,
                subject,
                grade
            };

            addEvaluationToList(evaluation);
            clearEvaluationForm();
        }
    });

    function validateEvaluationForm(studentName, subject, grade) {
        if (!studentName) {
            alert('Por favor, preencha o nome do estudante.');
            return false;
        }
        if (!subject) {
            alert('Por favor, preencha a disciplina.');
            return false;
        }
        if (!grade || isNaN(grade) || grade < 0 || grade > 10) {
            alert('Por favor, preencha a nota com um número válido entre 0 e 10.');
            return false;
        }
        return true;
    }

    function addEvaluationToList(evaluation) {
        const li = document.createElement('li');
        li.textContent = `Nome: ${evaluation.studentName}, Disciplina: ${evaluation.subject}, Nota: ${evaluation.grade}`;
        evaluationList.appendChild(li);
    }

    function clearEvaluationForm() {
        document.getElementById('studentName').value = '';
        document.getElementById('subject').value = '';
        document.getElementById('grade').value = '';
    }
});
// scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const formCadastro = document.getElementById('formCadastro');
    const studentList = document.getElementById('students');

    formCadastro.addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const age = document.getElementById('age').value;
        const className = document.getElementById('class').value;

        if (validateStudentForm(name, age, className)) {
            const student = {
                name,
                age,
                className
            };

            addStudentToList(student);
            clearForm();
        }
    });

    function validateStudentForm(name, age, className) {
        if (!name) {
            alert('Por favor, preencha o nome do estudante.');
            return false;
        }
        if (!age || isNaN(age) || age <= 0) {
            alert('Por favor, preencha a idade do estudante com um número válido.');
            return false;
        }
        if (!className) {
            alert('Por favor, preencha a turma do estudante.');
            return false;
        }
        return true;
    }

    function addStudentToList(student) {
        const li = document.createElement('li');
        li.textContent = `Nome: ${student.name}, Idade: ${student.age}, Turma: ${student.className}`;
        studentList.appendChild(li);
    }

    function clearForm() {
        document.getElementById('name').value = '';
        document.getElementById('age').value = '';
        document.getElementById('class').value = '';
    }
});
