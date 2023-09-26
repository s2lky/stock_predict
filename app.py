from flask import Flask
from Routes import auth, chat, dashboard, home

app = Flask(__name__)
app.register_blueprint(auth.app)
app.register_blueprint(chat.app)
app.register_blueprint(dashboard.app)
app.register_blueprint(home.app)

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=8000)
