FROM ubuntu:bionic

ENV PYTHONUNBUFFERED 1

RUN apt-get --quiet update
RUN apt-get install --yes --force-yes python3
RUN apt-get install --yes --force-yes python3-pip
RUN apt-get install --yes --force-yes libpython3-dev

RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN pip3 install -r requirements.txt
#RUN chmod +x manage.py
#RUN python3 manage.py makemigrations
#RUN python3 manage.py runserver 0.0.0.0:8000
