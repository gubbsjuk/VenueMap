FROM python:3.8.2

# Vekkje ka d gjor, men d printa ihvertfall!
ENV PYTHONUNBUFFERED 1

COPY manage.py manage.py
COPY requirements.txt requirements.txt
COPY vm_app vm_app
COPY venuemap venuemap


# Temporary media.
COPY media media

# Temporary database with contents.
COPY db.sqlite3 db.sqlite3

# Install requirements
RUN pip install -r requirements.txt

# EXPOSE PORT 8000 FOR WEBAPP
EXPOSE 8000

# START SERVER
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]