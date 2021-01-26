from flask import current_app as app
import dateutil.parser
import babel


def format_datetime(value, format='medium'):
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(value, format)

app.jinja_env.filters['datetime'] = format_datetime
