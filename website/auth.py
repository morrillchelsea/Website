'''
Created on Jul 4, 2022

@author: chelseanieves

Purpose: Manages routes related to user account creation and authentication
'''
import string
from flask import Blueprint, request, render_template, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from flask_login.utils import login_required
from website import db, logger
from .models import User

auth = Blueprint('auth', __name__)
SPECIAL_CHAR = string.punctuation
COMMON_PASS = "website/CommonPassword.txt"

@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Verifies user account credentials and logs user in.
    Returns an error if no account is found'''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            # hash password and compare to stored password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect('/')
            else:
                flash('Incorrect password, try again.', category='error')
                # log failed authentication attempt
                logger.error('Authentication failure: Incorrect password')
        else:
            flash("No account with this email exists.", category = 'error')
            # log failed authentication attempt
            logger.error('Authentication failure: Account not found')

    return render_template("login.html", title = "Log In", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    '''Ends user's session and redirects user to the home page'''
    logout_user()
    flash('Log out successful!', category='success')
    return redirect('/')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    '''Method to call Log In web page of "My Pets" '''
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        # query database by email to determine if  user is not already registered
        user = User.query.filter_by(email=email).first()
        if user:
            flash("There is already an account associated with this email address.",
                  category="error")
        elif email == "" or first_name == "" or password1 == "" or password2 == "":
            flash("Error: Field cannot be left blank.", category = "error")
        # password complexity should be enforced to include at least 12 characters in length,
        # and include at least 1 uppercase character, 1 lowercase character, 1 number and
        # 1 special character.
        elif validate_pass(password1, password2) is True:
            new_user = User(email=email, first_name = first_name, password =
                            generate_password_hash(password1, method= "sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created successfully.", category = "success")
            return redirect('/')
    # render template and pass page title to display
    return render_template("sign_up.html", title = "Sign Up", user=current_user)

@auth.route('/change-pass', methods=['GET', 'POST'])
@login_required
def change_pass():
    '''Method to call chage-pass page from My Profile. Enables user to change their current
    password if supplied appropriate credentials'''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get("current_pass")
        new_pass1 = request.form.get("new_pass1")
        new_pass2 = request.form.get("new_pass2")
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Please verify the e-mail you have entered is the correct e-mail associated with\
            the account.", category = "error")
        elif check_password_hash(user.password, password) is False:
            flash("Authentication error: Password does not match current password.\
            Please try again.", category = 'error')
        elif email == "" or password == "" or new_pass1 == "" or new_pass2 == "":
            flash("Error: Field cannot be left blank.", category = "error")
        elif validate_pass(new_pass1, new_pass2) is True:
            user.password = generate_password_hash(new_pass1, method= "sha256")
            db.session.commit()
            flash("Password updated successfully.", category = "success")
    return render_template("change_pass.html", title = "Change Password", user=current_user)
def validate_pass(password1, password2):
    '''Validates user's desired password is not found in list of common passphrases.
    Validates user's desired password against requirements (12 char in length, 1 upper, 1 lower,
    1 special char)
    Returns true if user's password meets requirements.'''
    try:
        with open(f'{COMMON_PASS}') as f:
            contents = f.read()
            if password1 in contents:
                flash("Error: Found in list of common passwords. Please try again.",
                      category = "error")
            elif len(password1) < 12:
                flash("Invalid length: Password must be greater than 12 characters.",
                      category = "error")
            elif not any(char.isdigit() for char in password1):
                flash("Error: Password must contain at least one numerical character.",
                      category = "error")
            elif not any(char.islower() for char in password1):
                flash("Error: Password must contain at least one lowercase character.",
                      category = "error")
            elif not any(char.isupper() for char in password1):
                flash("Error: Password must contain at least one uppercase character.",
                      category = "error")
            elif not any(char in SPECIAL_CHAR for char in password1):
                flash("Error: Password must contain at least one special character.",
                      category = "error")
            elif password1 != password2:
                flash("Error: Passwords do not match.", category = "error")
            else:
                return True
    except IOError:
        print("Could not find file CommonPassword.txt")
        flash("Error: Something went wrong. Unable to complete action.", category = "error")
        return False
    