FROM python:3.10.7

COPY ./meeting_website /srv/www/meeting_website
WORKDIR /srv/www/meeting_website
ENV SECRET_KEY = 'django-insecure-$2bwkovur#eq^(u!5e@tftmbx#0dpf+%@#dpvm1y@g6l=($m52'
ENV EMAIL = 'service.megano@gmail.com'
ENV EMAIL_HOST_USER = "service.megano@gmail.com"
ENV EMAIL_HOST_PASSWORD = "riuqnqydepsshhmj"
RUN pip3 install -r req.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]