from flask import render_template, session, redirect, url_for, Blueprint

app = Blueprint("dashboard", __name__)

@app.route('/dashboard')
def dashboard():
    print("dashboard")
    return render_template('dashboard.html')
