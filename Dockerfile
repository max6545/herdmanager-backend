FROM python:3.10-slim

WORKDIR /usr/src/app
COPY . .


RUN ["pip3", "install", "pipenv"]
RUN ["pipenv", "install"]


ENV FLASK_APP app/app.py

CMD [ "pipenv", "run", "gunicorn", "-w", "4", "--worker-tmp-dir", "/dev/shm", "-b", "0.0.0.0:80", "app:app" ]

EXPOSE 80