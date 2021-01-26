from datetime import datetime
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SelectField, SelectMultipleField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, URL, ValidationError, Regexp, Optional
from wtforms.fields.html5 import DateField, TimeField
from . import models
import re


class ShowForm(FlaskForm):
    artist_id = IntegerField(
        'artist_id', validators=[DataRequired()]
    )
    venue_id = IntegerField(
        'venue_id', validators=[DataRequired()]
    )
    show_date = DateField(
        'show_date',
        validators=[DataRequired()],
        default=datetime.now(),
        format='%Y-%m-%d'
    )
    show_time = TimeField(
        'show_time',
        validators=[DataRequired()],
        default=datetime.now(),
        format='%H:%M'
    )


class BasicForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state_id = SelectField(
        'state_id', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()], coerce=int
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()]
    )
    website = StringField(
        'website', validators=[Optional(), URL()]
    )
    seeking = BooleanField(
        'seeking', render_kw={'checked': False}
    )
    seeking_description = TextAreaField(
        'seeking_description'
    )

    def validate_phone(self, phone):
        us_phone_num = '^([0-9]{3})[-][0-9]{3}[-][0-9]{4}$'
        match = re.search(us_phone_num, phone.data)
        if not match:
            raise ValidationError('Error, phone number must be in format xxx-xxx-xxxx')

        phone_prefixes = [x.prefix for x in models.Phone.query.filter_by(state=self.state_id.data).all()]
        if int(phone.data[:3]) not in phone_prefixes:
            raise ValidationError('Enter a valid prefix phone number')

    def validate_seeking_description(self, seeking_description):
        if self.seeking.data is True and seeking_description.data == '':
            raise ValidationError('Enter a short description of what you\'re looking for')


class VenueForm(BasicForm):
    address = StringField('address', validators=[DataRequired()])
    seeking_talent = BooleanField(
        'seeking_talent', render_kw={'checked': False}
    )

    def validate_seeking_description(self, seeking_description):
        if self.seeking_talent.data is True and seeking_description.data == '':
            raise ValidationError('Enter a short description of what you\'re looking for')


class ArtistForm(BasicForm):
    seeking_venue = BooleanField(
        'seeking_venue', render_kw={'checked': False}
    )

    def validate_seeking_description(self, seeking_description):
        if self.seeking_venue.data is True and seeking_description.data == '':
            raise ValidationError('Enter a short description of what you\'re looking for')