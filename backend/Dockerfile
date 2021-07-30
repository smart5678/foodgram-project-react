FROM python:3.8.5

WORKDIR /code

COPY requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip3 install -r ./requirements.txt
COPY . .
# RUN python manage.py makemigrations
# RUN python manage.py migrate
# RUN python manage.py collectstatic

# CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
# CMD python /code/manage.py runserver 0:8000
