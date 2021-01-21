from . import db

venue_genres = db.Table('venue_genres',
                        db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
                        db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True)
                        )

artist_genres = db.Table('artist_genres',
                         db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
                         db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True)
                         )


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    genres = db.relationship('Genre', secondary=venue_genres, backref=db.backref('venues', lazy=True))


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)


class State(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    state_code = db.Column(db.String(2), unique=True, nullable=False)


class Phone(db.Model):
    __tablename__ = 'phones'

    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.Integer, unique=True, nullable=False)
    state = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    genres = db.relationship('Genre', secondary=artist_genres, backref=db.backref('artists', lazy=True))


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    show_date = db.Column(db.Date)
    show_time = db.Column(db.Time)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist = db.relationship('Artist', backref=db.backref('artists', lazy=True))
    venue = db.relationship('Venue', backref=db.backref('venues', lazy=True))

