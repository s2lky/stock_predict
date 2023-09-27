# from Routes import app
from flask import render_template, request, redirect, url_for, session, Blueprint

app = Blueprint("auth", __name__)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print('signup')
    # Signup route implementation
    return render_template('signup.html')

@app.route('/login/<email>')
def login(email):
    print(email)
    # Login route implementation
    return render_template('login.html')

@app.route('/mailSender', methods=['POST'])
def auth():
    email = request.form.get('email')
    # DB에 있는 이메일인지 조회
    exist = False
    
    # DB에 없다면 /signup으로 리다이렉트

    # DB에 있다면 /<userid>로 정보담아서 리다이렉트

    return redirect(url_for('auth.login', email=email))