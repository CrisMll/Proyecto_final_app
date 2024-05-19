from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
import re

class PasswordCheck:
    def __init__(self, message=None):
        if not message:
            message = 'Introduce al menos un número y una letra mayúscula.'
        self.message = message

    def __call__(self, form, field):
        password = field.data
        if not re.search(r'\d', password) or not re.search(r'[A-Z]', password):
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    passwrd = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6), PasswordCheck()])
    confirm_passwrd = PasswordField('Confirmar Contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')
    
    def validate(self, **kwargs):

        initial_validation = super(RegistrationForm, self).validate(**kwargs)

        if self.passwrd.data != self.confirm_passwrd.data:
            self.confirm_passwrd.errors.append('Las contraseñas no coinciden')
            return False

        return initial_validation