FROM python:3.10

RUN mkdir app

WORKDIR /app

COPY client /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install openjdk-11-jdk -y
RUN pip3 install -r requirements.txt

CMD ["python", "pyspark_stream.py"]