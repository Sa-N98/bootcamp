from flask import Flask, render_template, request , redirect, url_for
from model import *
import os

current_dir = os.path.abspath(os.path.dirname(__file__)) 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, 'database.sqlite3')

db.init_app(app)
app.app_context().push()



@app.route('/', methods=['GET', 'POST'])   # / == http://127.0.0.1:5000
def home():
    if request.method == 'POST':
        user_name=request.form['username']
        user_email=request.form['email']
        user_password=request.form['password']
        user_type = request.form['usertype']
        if not user_type == 'end_user':
            return "Invalid User Type"
        
        if user.query.filter(user.email == user_email).first():
            return "User already exists"
        else:
            new_user = user(username=user_name, email=user_email, password=user_password, user_type=user_type)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])   # / == http://127.0.0.1:5000
def login():
    if request.method == 'POST':
        user_email=request.form['email']
        user_password=request.form['password']

        check_user = user.query.filter(user.email == user_email).first()

        if check_user != None:
           if check_user.password == user_password:
                return redirect(url_for('user_dashbord'))
           else:
                return "Invalid password"
        else:
            return "User does not exist"
    
    return render_template('user_login.html')

@app.route('/about')  
def about():
    return render_template('about.html')










@app.route('/user_dashbord')  
def user_dashbord():
    movie_data = movie.query.all()
    return render_template('user_dashbord.html', movieData = movie_data)

















if __name__ == '__main__':  
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
