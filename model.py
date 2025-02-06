from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class user(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    user_type = db.Column(db.String)


class movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    current_theaters = db.relationship('theaters', secondary="movie_theater") 
    title = db.Column(db.String)
    poster_url = db.Column(db.String)
    genre = db.Column(db.String)
    rating = db.Column(db.Float)
    

class movie_theater(db.Model):
    __tablename__ = 'movie_theater'
    m_id=db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    t_id=db.Column(db.Integer, db.ForeignKey('theaters.id'), primary_key=True)

class theaters(db.Model):
    __tablename__ = 'theaters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
