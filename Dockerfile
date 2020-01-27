FROM python:3

ADD app.py /

RUN pip install pyinotify

CMD [ "python3", "./app.py" ]
