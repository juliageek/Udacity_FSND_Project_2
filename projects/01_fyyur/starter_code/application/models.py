from . import db

venue_genres = db.Table('venue_genres',
                        db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
                        db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
                        )

artist_genres = db.Table('artist_genres',
                         db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
                         db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
                         )


class Venue(db.Model):
    __tablename__ = 'Venue'

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
    seeking_description = db.Column(db.String(120), db.CheckConstraint('seeking_talent=True'))
    genres = db.relationship('Genre', secondary=venue_genres, backref=db.backref('venues', lazy=True))


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)


class State(db.Model):
    __tablename__ = 'State'

    id = db.Column(db.Integer, primary_key=True)
    state_code = db.Column(db.String(2), unique=True, nullable=False)


class Phone(db.Model):
    __tablename__ = 'Phone'

    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.Integer, unique=True, nullable=False)
    state = db.Column(db.Integer, db.ForeignKey('State.id'), nullable=False)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120), db.CheckConstraint('seeking_talent=True'))
    genres = db.relationship('Genre', secondary=artist_genres, backref=db.backref('artists', lazy=True))

