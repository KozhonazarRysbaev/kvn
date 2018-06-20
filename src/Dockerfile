FROM python:3.5-onbuild
ENV DJANGO_SETTINGS_MODULE=main.settings

COPY ./ /usr/src/kvnet
#RUN bash run.sh
#WORKDIR /usr/src/kvnet/
CMD python manage.py runserver 0.0.0.0:8000