from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    correo = StringField(
        'Correo',
        validators=[
            DataRequired(message="El correo es obligatorio"),
            Email(message="Ingrese un correo válido"),
            Length(max=100, message="El correo no debe exceder los 100 caracteres")
        ]
    )

    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message="La contraseña es obligatoria"),
            Length(min=6, message="La contraseña debe tener al menos 6 caracteres")
        ]
    )

    submit = SubmitField('Iniciar Sesión')
    
class RegistrationForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=2, max=30)])
    apellido = StringField("Apellido", validators=[DataRequired(), Length(min=2, max=30)])
    carrera = StringField("Carrera", validators=[DataRequired(), Length(min=2, max=50)])
    correo = StringField("Correo", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmar Contraseña", validators=[
        DataRequired(),
        EqualTo("password", message="Las contraseñas deben coincidir")
    ])
    estatus = SelectField("Estatus", choices=[
        ("alumno", "Alumno"),
        ("vendedor", "Vendedor")
    ], validators=[DataRequired()])
    submit = SubmitField("Registrar")
    
