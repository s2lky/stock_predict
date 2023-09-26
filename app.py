from flask import Flask, render_template, request, redirect, url_for, session
# from flask_sqlalchemy import SQLAlchemy
from Routes import auth, chat, dashboard

app = Flask(__name__)
app.register_blueprint(auth.app)
app.register_blueprint(chat.app)
app.register_blueprint(dashboard.app)

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=8000)
