from flask import current_app as app
import dateutil.parser
import babel


def format_date(value, format='medium'):
  if format == 'full':
      format="EEEE MMMM, d, y"
  elif format == 'medium':
      format="EE MM, dd"
  return babel.dates.format_datetime(value, format)


def format_time(value, format='medium'):
  if format == 'full':
      format="h:mma"
  elif format == 'medium':
      format="h:mma"
  return babel.dates.format_datetime(value, format)


app.jinja_env.filters['date'] = format_date
app.jinja_env.filters['time'] = format_time
