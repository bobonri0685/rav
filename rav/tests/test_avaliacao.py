# tests/test_avaliacao.py
import pytest
from src.avaliacao import validate_evaluation_form

def test_validate_evaluation_form():
    assert validate_evaluation_form('João', 'Matemática', 8) == True
    assert validate_evaluation_form('', 'Matemática', 8) == False
    assert validate_evaluation_form('João', '', 8) == False
    assert validate_evaluation_form('João', 'Matemática', -1) == False
    assert validate_evaluation_form('João', 'Matemática', 11) == False
