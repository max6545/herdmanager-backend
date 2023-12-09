FROM python:3.10-slim

ARG NC_HOST
ARG NC_USER
ARG NC_PW
ARG USE_PG_DB
ARG DB_PW
ARG DB_USER
ARG DB_HOST
ARG DB_NAME
ENV NEXTCLOUD_HOST $NC_HOST
ENV NEXTCLOUD_USER $NC_USER
ENV NEXTCLOUD_PASSWORD $NC_PW
ENV USE_PG_DB $USE_PG_DB
ENV DB_PW $DB_PW
ENV DB_USER $DB_USER
ENV DB_HOST $DB_HOST
ENV DB_NAME $DB_NAME

RUN pip install pipenv
RUN pip install --upgrade pip

ENV SRC_DIR /usr/local/src/herdmanager


WORKDIR ${SRC_DIR}

COPY Pipfile Pipfile.lock ${SRC_DIR}/
RUN pipenv install --system --clear
COPY ./ ${SRC_DIR}/

ENV FLASK_APP app/app.py

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]
EXPOSE 5000