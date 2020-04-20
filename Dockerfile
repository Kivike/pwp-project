FROM node:10

MAINTAINER Roope Rajala "coloris23@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /app

COPY ["package-lock.json", "package.json", "/app/"]
RUN npm install

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

RUN npm run build
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN python3 -m flask init-db
ENTRYPOINT [ "python3" ]
CMD ["app.py"]