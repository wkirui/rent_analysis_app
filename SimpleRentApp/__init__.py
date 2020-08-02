from flask import Flask

from .dash_app import create_dash_app

app = Flask(__name__)

# enter dash app
create_dash_app(app)

@app.route('/')
def start_application():
    return("Hello world!")