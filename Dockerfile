FROM python:3

ADD *.py /

RUN pip install pyinotify

CMD [ "python3", "./app.py" ]
