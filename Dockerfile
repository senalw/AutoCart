FROM python:3.11
LABEL author='SenalW'

WORKDIR /AutoCart

RUN apt-get update  \
    && apt-get dist-upgrade -y \
    && apt-get install make -y \
    && apt-get install wget -y

COPY Makefile .
COPY requirements.txt .
COPY requirements-style.txt .
COPY requirements-test.txt .
COPY settings.py .

RUN make setup
RUN make install

COPY src ./src/
COPY resources ./resources/