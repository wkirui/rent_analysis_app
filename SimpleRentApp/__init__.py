from flask import Flask,redirect

from .dash_app import create_dash_app

app = Flask(__name__)

# enter dash app
create_dash_app(app)

@app.route('/')
def start_application():
    return redirect('/dash')

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')