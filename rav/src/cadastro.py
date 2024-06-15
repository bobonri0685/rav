# src/cadastro.py

def validate_student_form(name, age, className):
    if not name or not isinstance(age, int) or age <= 0 or not className:
        return False
    return True
