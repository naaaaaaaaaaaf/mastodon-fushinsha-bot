FROM python:3.8.5

RUN apt update
RUN apt install -y mecab libmecab-dev mecab-ipadic-utf8 swig
RUN ln -s /var/lib/mecab/dic /usr/lib/mecab/dic
RUN mkdir /var/app
WORKDIR /var/app
COPY src/Pipfile ./
#COPY src/Pipfile.lock ./
RUN pip install pipenv
#RUN pipenv install --system