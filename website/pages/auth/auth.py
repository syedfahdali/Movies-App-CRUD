from flask import Blueprint, render_template, request, flash, redirect, url_for
from database.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user as current_logged_in_user
from website.forms.forms import RegistrationForm, LoginForm, ChangePasswordForm
from urllib.parse import urlsplit
from database.database import db

auth_bp = Blueprint(
    'auth_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/auth',
)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_logged_in_user.is_authenticated:
        flash("You're already logged in.")
        return redirect(url_for('home_page_bp.home_page'))
    
    form = LoginForm(request.form)
    
    if request.method == 'POST' and form.validate():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        
        if user is None:
            flash('User name password combination does not exist, try again.', category='error')
            return redirect(url_for('auth_bp.login'))
        
        if check_password_hash(user.password, form.password.data):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            next_page = request.args.get('next')
            
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('home_page_bp.home_page')
                
            return redirect(next_page)
        else:
            flash('User name password combination does not exist, try again.', category='error')

    return render_template("login.html", user=current_logged_in_user, form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_logged_in_user.is_authenticated:
        flash("You're already logged in, sign out first!")
        return redirect(url_for('home_page_bp.home_page'))

    form = RegistrationForm(request.form)
    
    if request.method == 'POST' and form.validate():
        new_user_obj = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data, method='scrypt'),
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(new_user_obj)
        db.session.commit()

        # login_user(new_user, remember=True)
        flash('Account created!', category='success')
        return redirect(url_for('home_page_bp.home_page'))

    return render_template('register.html', form=form, user=current_logged_in_user)


@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)

    if request.method == 'POST' and form.validate():
        # user = User.get(username=form.username.data).first()
        user = current_logged_in_user

        if user is None:
            flash('Email password combination does not exist, try again.', category='error')
            return redirect(url_for('auth_bp.login'))
        
        if not check_password_hash(user.password, form.old_password.data):
            flash('Email password combination does not exist, try again.', category='error')
            return redirect(url_for('auth_bp.change_password'))
        
        new_password = generate_password_hash(form.new_password.data, method='scrypt')
        db.session.query(User).filter_by(id=user.id).update({"password": new_password})
        db.session.commit()

        # login_user(new_user, remember=True)
        flash('Password updated!, please log back in', category='success')
        logout_user()
        return redirect(url_for('auth_bp.login'))

    return render_template('change_password.html', form=form, user=current_logged_in_user)

