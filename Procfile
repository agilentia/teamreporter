web: gunicorn teamreporterapp.wsgi --log-file -
worker: celery -A teamreporterapp worker -l info
beat: celery -A teamreporterapp worker -B -l info
