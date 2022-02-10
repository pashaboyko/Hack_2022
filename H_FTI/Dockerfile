FROM python:3.7
MAINTAINER Boiko Pavlo 'pboyko172839465@gmail.com'

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /usr/src/app
COPY ./app/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt 
COPY ./app .

ENTRYPOINT  [ "python","-m", "main"]