FROM python:3.11
ENV PYTHONUNBUFFERED=1

WORKDIR /app/resourcedb
COPY requirements.txt /app/resourcedb/
RUN apt update -y && apt upgrade -y && apt install -y iputils-ping 
RUN pip install -r requirements.txt
RUN groupadd -r docker && useradd -r -m -g docker docker

COPY . /app/resourcedb
