FROM python:3.6.1-alpine

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD [ "app/autoapp.py" ]