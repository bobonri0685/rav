# tests/test_cadastro.py
import pytest
from src.cadastro import validate_student_form

def test_validate_student_form():
    assert validate_student_form('João', 10, '5A') == True
    assert validate_student_form('', 10, '5A') == False
    assert validate_student_form('João', -1, '5A') == False
    assert validate_student_form('João', 10, '') == False
