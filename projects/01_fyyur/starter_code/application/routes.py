from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for, jsonify, abort
import logging
from logging import Formatter, FileHandler
from sqlalchemy import desc, text

from . import models
from . import forms
from . import db


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    def venue_info(area):
        state = models.State.query.order_by(desc('state_code'))\
            .with_entities(models.State.state_code)\
            .filter_by(id=area.state)
        return {
            'city': area.city,
            'state': state.first()[0],
            'venues': [{
                'id': venue.id,
                'name': venue.name
            } for venue in models.Venue.query.filter_by(state=area.state, city=area.city).all()]
        }

    areas_data = models.Venue.query\
        .with_entities(models.Venue.state, models.Venue.city)\
        .group_by(models.Venue.state, models.Venue.city).all()

    venues_data = [venue_info(area) for area in areas_data]

    return render_template('pages/venues.html', areas=venues_data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_str = request.form['search_term']
    response_venues = models.Venue.query.filter(text('name ~* :reg')).params(reg=search_str).all()
    response = {
        'count': len(response_venues),
        'data': response_venues
    }

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue_data = models.Venue.query.filter_by(id=venue_id).first()

    return render_template('pages/show_venue.html', venue=venue_data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = forms.VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    body = request.get_json()
    genres = [models.Genre.query.filter_by(id=genre).all()[0] for genre in body['genres']]
    seeking_description = body['seeking_description']

    if not body['seeking_talent']:
        seeking_description = ''

    venue = models.Venue(
        name=body['name'],
        city=body['city'],
        state=body['state'],
        address=body['address'],
        phone=body['phone'],
        image_link=body['image_link'],
        facebook_link=body['facebook_link'],
        website=body['website'],
        seeking_talent=body['seeking_talent'],
        seeking_description=seeking_description,
        genres=genres
    )

    form = forms.VenueForm(csrf_enabled=False)
    is_valid = form.validate()
    response = jsonify({'message': 'Success'})
    response.headers['Content-Type'] = 'application/json'

    if is_valid:
        try:
            db.session.add(venue)
            db.session.commit()
            flash('Venue was created!')
        except():
            flash('An error occurred. Venue ' + body['name'] + ' could not be created.')
            db.session.rollback()
        finally:
            db.session.close()
    else:
        response = jsonify({'message': 'Errors', 'errors': form.errors})
    return response


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        venue = models.Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash('Venue was deleted!')
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({'message': 'Success'})


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = models.Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_str = request.form['search_term']
    response_artists = models.Artist.query.filter(text('name ~* :reg')).params(reg=search_str).all()
    response = {
        'count': len(response_artists),
        'data': response_artists
    }

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    data = models.Artist.query.filter_by(id=artist_id).first()
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = forms.ArtistForm(csrf_enabled=False)
    artist_to_edit = models.Artist.query.filter_by(id=artist_id).first()

    artist = {
        "id": artist_to_edit.id,
        "name": artist_to_edit.name
    }

    form.name.data = artist_to_edit.name
    form.city.data = artist_to_edit.city
    form.state.data = artist_to_edit.state
    form.genres.data = [x.id for x in artist_to_edit.genres]
    form.phone.data = artist_to_edit.phone
    form.facebook_link.data = artist_to_edit.facebook_link
    form.image_link.data = artist_to_edit.image_link
    form.website.data = artist_to_edit.website
    form.seeking_venue.data = artist_to_edit.seeking_venue
    form.seeking_description.data = artist_to_edit.seeking_description

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    body = request.get_json()

    genres_to_save = [models.Genre.query.filter_by(id=genre).all()[0] for genre in body['genres']]
    artist = models.Artist.query.get(artist_id)
    artist.name = body['name']
    artist.city = body['city']
    artist.phone = body['phone']
    artist.state = body['state']
    artist.image_link = body['image_link']
    artist.facebook_link = body['facebook_link']
    artist.genres = genres_to_save
    artist.website = body['website']
    artist.seeking_venue = body['seeking_venue']
    artist.seeking_description = body['seeking_description']

    form = forms.ArtistForm(csrf_enabled=False)
    is_valid = form.validate()
    response = jsonify({'message': 'Success'})
    response.headers['Content-Type'] = 'application/json'

    if is_valid:
        try:
            db.session.commit()
            flash(f'Venue {artist.name} was successfully updated!')
        except IndexError:
            flash('An error occurred. Venue ' + body['name'] + ' could not be updated .')
            db.session.rollback()
        finally:
            db.session.close()
    else:
        response = jsonify({'message': 'Errors', 'errors': form.errors})
    return response


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = forms.VenueForm(csrf_enabled=False)
    venue_to_edit = models.Venue.query.filter_by(id=venue_id).first()

    venue = {
        "id": venue_to_edit.id,
        "name": venue_to_edit.name
    }

    form.name.data = venue_to_edit.name
    form.city.data = venue_to_edit.city
    form.state.data = venue_to_edit.state
    form.genres.data = [x.id for x in venue_to_edit.genres]
    form.address.data = venue_to_edit.address
    form.phone.data = venue_to_edit.phone
    form.facebook_link.data = venue_to_edit.facebook_link
    form.image_link.data = venue_to_edit.image_link
    form.website.data = venue_to_edit.website
    form.seeking_talent.data = venue_to_edit.seeking_talent
    form.seeking_description.data = venue_to_edit.seeking_description

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    body = request.get_json()

    genres_to_save = [models.Genre.query.filter_by(id=genre).all()[0] for genre in body['genres']]
    venue = models.Venue.query.get(venue_id)
    venue.name = body['name']
    venue.city = body['city']
    venue.phone = body['phone']
    venue.state = body['state']
    venue.address = body['address']
    venue.image_link = body['image_link']
    venue.facebook_link = body['facebook_link']
    venue.genres = genres_to_save
    venue.website = body['website']
    venue.seeking_talent = body['seeking_talent']
    venue.seeking_description = body['seeking_description']

    form = forms.VenueForm(csrf_enabled=False)
    is_valid = form.validate()
    response = jsonify({'message': 'Success'})
    response.headers['Content-Type'] = 'application/json'

    if is_valid:
        try:
            db.session.commit()
            flash(f'Venue {venue.name} was successfully updated!')
        except IndexError:
            flash('An error occurred. Venue ' + body['name'] + ' could not be updated .')
            db.session.rollback()
        finally:
            db.session.close()
    else:
        response = jsonify({'message': 'Errors', 'errors': form.errors})
    return response


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = forms.ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    body = request.get_json()
    genres = [models.Genre.query.filter_by(id=genre).all()[0] for genre in body['genres']]
    seeking_description = body['seeking_description']

    if not body['seeking_venue']:
        seeking_description = ''

    artist = models.Artist(
        name=body['name'],
        city=body['city'],
        state=body['state'],
        phone=body['phone'],
        image_link=body['image_link'],
        facebook_link=body['facebook_link'],
        website=body['website'],
        seeking_venue=body['seeking_venue'],
        seeking_description=seeking_description,
        genres=genres
    )

    form = forms.ArtistForm(csrf_enabled=False)
    is_valid = form.validate()
    response = jsonify({'message': 'Success'})
    response.headers['Content-Type'] = 'application/json'

    if is_valid:
        try:
            db.session.add(artist)
            db.session.commit()
            flash(f'Artist {artist.name} was created!')
        except():
            flash('An error occurred. Venue ' + body['name'] + ' could not be created.')
            db.session.rollback()
        finally:
            db.session.close()
    else:
        response = jsonify({'message': 'Errors', 'errors': form.errors})
    return response


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    error = False
    try:
        venue = models.Artist.query.get(artist_id)
        db.session.delete(venue)
        db.session.commit()
        flash('Artist was deleted!')
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({'message': 'Success'})


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = forms.ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')
