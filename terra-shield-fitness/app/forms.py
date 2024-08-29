from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class QuestionnaireForm(FlaskForm):
    height = FloatField('Height (cm)', validators=[DataRequired()])
    weight = FloatField('Weight (kg)', validators=[DataRequired()])
    activity_level = SelectField('Activity Level', choices=[
        ('sedentary', 'Sedentary'),
        ('lightly_active', 'Lightly Active'),
        ('moderately_active', 'Moderately Active'),
        ('very_active', 'Very Active')
    ])
    fitness_goal = SelectField('Fitness Goal', choices=[
        ('lose_weight', 'Lose Weight'),
        ('build_muscle', 'Build Muscle'),
        ('improve_endurance', 'Improve Endurance'),
        ('maintain_fitness', 'Maintain Fitness')
    ])
    submit = SubmitField('Next')

class EquipmentForm(FlaskForm):
    equipment_choices = [
        ('dumbbells', 'Dumbbells'),
        ('barbell', 'Barbell'),
        ('resistance_bands', 'Resistance Bands'),
        ('pull_up_bar', 'Pull-up Bar'),
        ('bench', 'Bench'),
        ('treadmill', 'Treadmill'),
        ('exercise_bike', 'Exercise Bike'),
        ('kettlebell', 'Kettlebell'),
        ('yoga_mat', 'Yoga Mat'),
    ]
    equipment = SelectMultipleField('Available Equipment', choices=equipment_choices)
    submit = SubmitField('Generate Workout')