from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Uporabniško ime',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-pošta',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Geslo', validators=[DataRequired()])
    confirm_password = PasswordField('Potrdite geslo',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registracija')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('To uporabniško ime je že zasedeno. Prosimo, izberite drugega.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ta e-pošta je že zasedena. Prosimo, izberite drugo.')


class LoginForm(FlaskForm):
    email = StringField('E-pošta',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Geslo', validators=[DataRequired()])
    remember = BooleanField('Zapomni si me')
    submit = SubmitField('Prijava')


class UpdateAccountForm(FlaskForm):
    username = StringField('Uporabniško ime',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-pošta',
                        validators=[DataRequired(), Email()])
    picture = FileField('Posodobi profilno sliko', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Posodobi')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('To uporabniško ime je že zasedeno. Prosimo, izberite drugega.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Ta e-pošta je že zasedena. Prosimo, izberite drugo.')


class RequestResetForm(FlaskForm):
    email = StringField('E-pošta',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Zahtevaj ponastavitev gesla')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Ni računa s to e-pošto. Najprej se morate registrirati.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Geslo', validators=[DataRequired()])
    confirm_password = PasswordField('Potrdite geslo',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Ponastavi geslo')