FROM python:3.11
WORKDIR /jrios

COPY . /jrios/
RUN pip install -r requirements.txt
EXPOSE 80
CMD [ "waitress-serve", "--port=80", "--call", "api:create_app" ]
