from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, ValidationError
from app.models import User

# Validação customizada para verificar nome único
def UniqueName(message=None):
    def _validate_name(form, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(message or 'Este nome já está registrado.')
    return _validate_name

# Validação customizada para verificar prontuário único
def UniqueProntuario(message=None):
    def _validate_prontuario(form, field):
        if User.query.filter_by(prontuario=field.data).first():
            raise ValidationError(message or 'Este prontuário já está registrado.')
    return _validate_prontuario

# Validação customizada para verificar e-mail único
def UniqueEmail(message=None):
    def _validate_email(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(message or 'Este e-mail já está registrado.')
    return _validate_email

class NameForm(FlaskForm):
    # Campo para o nome do usuário
    name = StringField(
        'Qual é o seu nome?',
        validators=[DataRequired(message="O campo de nome é obrigatório."),
                    UniqueName(message="Este nome já está registrado.")],
        render_kw={"placeholder": "Digite seu nome completo"}
    )

    # Campo para o prontuário com validação de formato
    prontuario = StringField(
        'Digite seu prontuário',
        validators=[
            DataRequired(message="O campo de prontuário é obrigatório."),
            Regexp(
                r'^[a-zA-Z]{3}\d{7}$',
                message='O prontuário deve ter 3 letras seguidas de 7 números. Exemplo: ABC1234567'
            ),
            UniqueProntuario(message="Este prontuário já está registrado.")  # Validação para prontuário único
        ],
        render_kw={"placeholder": "Exemplo: ABC1234567"}
    )

    email = StringField(
        'Digite seu email',
        validators=[DataRequired(message="O campo de email é obrigatório."),
                    Email(message="Insira um e-mail válido."),
                    UniqueEmail(message="Este e-mail já está registrado.")],
        render_kw={"placeholder": "Digite seu email"}
    )

    submit = SubmitField('Enviar')
