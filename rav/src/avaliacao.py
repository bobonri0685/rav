# src/avaliacao.py

def validate_evaluation_form(student_name, subject, grade):
    if not student_name or not subject or not isinstance(grade, (int, float)) or grade < 0 or grade > 10:
        return False
    return True
