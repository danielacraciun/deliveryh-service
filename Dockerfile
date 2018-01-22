FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Adds our application code to the image
COPY . /code/
WORKDIR /code

EXPOSE 8000

# Migrates the database
CMD ./manage.py migrate
