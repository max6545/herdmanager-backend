FROM python:3.10-slim

ARG NC_HOST
#ARG nextcloud_user
#ARG nextcloud_password
ENV NEXTCLOUD_HOST $NC_HOST
RUN ls && echo $NEXTCLOUD_HOST
#ENV NEXTCLOUD_USER nextcloud_user
#ENV NEXTCLOUD_PASSWORD nextcloud_password


#RUN pip install pipenv
#ENV SRC_DIR /usr/local/src/herdmanager


#WORKDIR ${SRC_DIR}

#COPY Pipfile Pipfile.lock ${SRC_DIR}/

#RUN pipenv install --system --clear

#COPY ./ ${SRC_DIR}/

#ENV FLASK_APP app/app.py

#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]
#EXPOSE 5000