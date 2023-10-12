FROM python:3.10-slim

RUN pip install pipenv

ENV SRC_DIR /usr/local/src/herdmanager

WORKDIR ${SRC_DIR}

COPY Pipfile Pipfile.lock ${SRC_DIR}/

RUN pipenv install --system --clear

COPY ./ ${SRC_DIR}/

#WORKDIR ${SRC_DIR}
# CMD ["flask", "run", "-h", "0.0.0.0"]
ENV FLASK_APP app/app.py

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]
EXPOSE 5000