from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, UserProfile, Equipment
from app.forms import RegistrationForm, LoginForm, QuestionnaireForm, EquipmentForm

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('main.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():
    form = QuestionnaireForm()
    if form.validate_on_submit():
        profile = UserProfile(
            user_id=current_user.id,
            height=form.height.data,
            weight=form.weight.data,
            activity_level=form.activity_level.data,
            fitness_goal=form.fitness_goal.data
        )
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('main.equipment'))
    return render_template('questionnaire.html', title='Questionnaire', form=form)

@main.route('/equipment', methods=['GET', 'POST'])
@login_required
def equipment():
    form = EquipmentForm()
    if form.validate_on_submit():
        for item in form.equipment.data:
            equipment = Equipment(user_id=current_user.id, name=item)
            db.session.add(equipment)
        db.session.commit()
        flash('Your profile has been updated!')
        return redirect(url_for('main.dashboard'))
    return render_template('equipment.html', title='Equipment', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    # TODO: Implement dashboard logic
    return render_template('dashboard.html', title='Dashboard')
