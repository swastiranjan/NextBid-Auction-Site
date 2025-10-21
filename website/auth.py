from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        print(user)

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please re-enter!', category='error')
        else:
            flash('No account exists with entered email!', category='error')
        
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #this makes sure logout page can't be accessed unless a user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        state = request.form.get('state')
        address = request.form.get('address')

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already in use!", category='error')        
        elif len(email) < 4:
            flash('Invalid email!', category='error')
        elif len(firstName) == 0:
            flash('Please enter first name!', category='error')
        elif len(lastName) == 0:
            flash('Please enter last name!', category='error')
        elif len(password1) < 8:
            flash('Password must be atleast 8 characters!', category='error')
        elif password1 != password2:
            flash('Entered passwords do not match!', category='error')
        elif len(address) == 0:
            flash('Please enter address!', category='error')
        else:
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='scrypt'), last_name=lastName, address=address, state=state)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Successfully created account!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)