FROM python:3.7
MAINTAINER Maarten Fabré "maartenfabre@gmail.com"
WORKDIR /my_movies/
ADD /app app/
ADD /src src
ADD requirements.txt .
ADD README.rst .
ADD HISTORY.rst .
ADD setup.py .

RUN pip install -r requirements.txt
RUN python setup.py install
WORKDIR /my_movies/app/
CMD ["python", "app.py"]