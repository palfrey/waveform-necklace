FROM python:2
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install numpy
RUN apt-get update
RUN apt-get install -y --no-install-recommends libsndfile-dev libasound2-dev
RUN pip install scikits.audiolab
WORKDIR /code
ADD . /code
CMD gunicorn necklace:app --log-file=- --bind 0.0.0.0:5000 --reload