FROM python:3.10

RUN mkdir app
RUN mkdir app/logs

WORKDIR /app

COPY server /app

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]