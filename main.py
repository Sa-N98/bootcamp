from flask import Flask, render_template
from model import *
import os

current_dir = os.path.abspath(os.path.dirname(__file__)) 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, 'database.sqlite3')

db.init_app(app)
app.app_context().push()



@app.route('/')   # / == http://127.0.0.1:5000
def home():
    return render_template('demo.html')

@app.route('/about')  
def about():
    return render_template('about.html')

if __name__ == '__main__':  
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
