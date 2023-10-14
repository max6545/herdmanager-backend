FROM python:3.10-slim

ARG NC_HOST
ARG NC_USER
ARG NC_PW
ENV NEXTCLOUD_HOST $NC_HOST
ENV NEXTCLOUD_USER $NC_USER
ENV NEXTCLOUD_PASSWORD $NC_PW
ENV IN_DOCKER_ENV Yes

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