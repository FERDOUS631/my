web: gunicorn kpi_notice.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn kpi_notice.wsgi