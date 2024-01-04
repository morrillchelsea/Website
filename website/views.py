'''
Created on Jul 4, 2022

@author: chelseanieves

Purpose: Manages additional routes, unrelated to user authentication or account creation
'''
from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required
from flask_login.utils import current_user
# assign today's date and time to a variable date
date = f"Today is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
views = Blueprint('views', __name__)

@views.route('/')   # URL '/' to be handled by main() route handler
def main():
    '''Method to call home web page of "My Pets." Passes variable date to display current date/time
    to user. '''
    # render template home.html and pass date variable to display date/time to user
    return render_template("home.html", date = date, user=current_user)

@views.route('/poptart')
@login_required
def poptart():
    '''Method to call cat web page "Pop Tart" of "My Pets" '''
    # render template and pass page title to display
    return render_template("poptart.html", title = "Pop Tart", user=current_user)

@views.route('/beni')
@login_required
def benito():
    '''Method to call "Benito" web page of "My Pets" '''
    # render template and pass page title to display
    return render_template("beni.html", title = "Benito", user=current_user)

@views.route('/chorizo')
@login_required
def chorizo():
    '''Method to call Chorizo web page of "My Pets" '''
    # render template and pass page title to display
    return render_template("chorizo.html", title = "Chorizo", user=current_user)

@views.route('/profile')
@login_required
def profile():
    '''Method to call My Profile page of "My Pets" '''
    return render_template("profile.html", title = "Profile", user=current_user)
