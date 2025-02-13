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
                return redirect(url_for('user_dashbord', USERNAME = check_user.username , ID=check_user.id))
           else:
                return "Invalid password"
        else:
            return "User does not exist"
    
    return render_template('user_login.html')

@app.route('/about')  
def about():
    return render_template('about.html')


@app.route('/user_dashbord/<USERNAME>/<ID>')  
def user_dashbord(USERNAME, ID):
    movie_data = movie.query.all()
    return render_template('user_dashbord.html', movieData = movie_data, userName = USERNAME, userID = ID)




@app.route('/movie_details/<USERID>/<MOVIE_ID>')
def movie_details(MOVIE_ID, USERID):
    movie_data = movie.query.filter(movie.id == MOVIE_ID).first()
    return render_template('movie_details.html', movieData = movie_data, userID = USERID)



@app.route('/userbooking/<USER_ID>', methods=['GET', 'POST'])
def userbooking(USER_ID):
    if request.method == 'POST':
        Booking = request.form['booking']
        MOVIE_id ,THEATER_id  = Booking.split(',')
       
        new_booking = booking(user_id=USER_ID, movie_id=int(MOVIE_id), theater_id=int(THEATER_id) )
        db.session.add(new_booking)
        db.session.commit()

        return "Movie Booked"
    

    booking_data = booking.query.filter(booking.user_id == USER_ID).all()
    user_booking = {}
    for movie_booking in booking_data:
        movie_data = movie.query.filter(movie.id == movie_booking.movie_id).first()
        theater_data = theaters.query.filter(theaters.id == movie_booking.theater_id).first() 
        user_booking[movie_booking.id] = [ movie_data.title,theater_data.name] 


    return render_template('mybooking.html', userID = USER_ID , bookingData = user_booking)


@app.route('/userbooking_delete/<BOOKING_ID>', methods=['GET', 'POST'])
def userbooking_delete(BOOKING_ID):
    booking.query.filter(booking.id == BOOKING_ID).delete()
    db.session.commit()
    return "Booking Deleted"












if __name__ == '__main__':  
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
