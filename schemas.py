from marshmallow import Schema, fields as ma_fields, validate

class AlunoSchema(Schema):
    nome = ma_fields.String(required=True, validate=validate.Length(min=1))
    idade = ma_fields.Integer(required=True, validate=validate.Range(min=1))
    serie = ma_fields.String(required=True, validate=validate.Length(min=1))
