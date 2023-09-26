from flask import render_template, session, redirect, url_for, Blueprint

app = Blueprint("chat", __name__)

@app.route('/chat')
def chat():
    print("chat")
    return render_template('chat.html')
