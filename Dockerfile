FROM python:3-alpine

MAINTAINER Victor Rachieru

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "python", "app.py" ]