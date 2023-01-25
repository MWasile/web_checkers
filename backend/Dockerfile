FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system

COPY . .
CMD python3 manage.py makemigrations && python3 manage.py migrate && python manage.py collectstatic --no-input --clear
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000