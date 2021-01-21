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


class CreateForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[(x.id, x.state_code) for x in models.State.query.order_by('state_code').all()]
    )
    phone = StringField(
        'phone', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        coerce=int,
        choices=[(x.id, x.name) for x in models.Genre.query.order_by('name').all()]
    )
    facebook_link = StringField(
        # TODO implement enum restriction
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

        phone_prefixes = [x.prefix for x in models.Phone.query.filter_by(state=self.state.data).all()]
        if int(phone.data[:3]) not in phone_prefixes:
            raise ValidationError('Enter a valid prefix phone number')

    def validate_seeking_description(self, seeking_description):
        if self.seeking and seeking_description.data == '':
            raise ValidationError('Enter a short description of what you\'re looking for')


class VenueForm(CreateForm):
    address = StringField('address', validators=[DataRequired()])
