# from Routes import app
from flask import render_template, request, redirect, url_for, session, Blueprint

app = Blueprint("auth", __name__)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print('signup')
    # Signup route implementation
    return render_template('signup.html', template_folder='templates')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login route implementation
    pass
