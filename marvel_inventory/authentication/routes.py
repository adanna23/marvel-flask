from flask import Blueprint, render_template, request, flash, redirect, url_for
from marvel_inventory.forms import UserLoginForm
from marvel_inventory.models import User, db, check_password_hash

from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
     form = UserLoginForm()
     try:
          if request.method == 'POST' and  form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)
            
            user= User(email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have succesfully created a user account {email}', 'user-created')
            return redirect(url_for('site.home'))
     except:
            raise Exception('Invalid Form of data: Please check your form input')

     return render_template('signup.html', form = form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
     form = UserLoginForm()
     try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)
            
            logged_user = User.query.filter(User.email == email).first()
            print(logged_user)
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                print('Successful login')
                flash('You were successfully logged in: Via Email/Password', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                print('Incorrect password')
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
     except:
        raise Exception('Invalid Form Data: Please check your Form')
     return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))

