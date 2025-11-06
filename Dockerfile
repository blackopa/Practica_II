FROM ubuntu:22.04

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install -y libsm6 libxext6 libxrender-dev

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./entrypoint.sh

RUN python3 ./get_model.py

CMD [ "sh", "entrypoint.sh" ]