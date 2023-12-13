FROM python:3.12

ENV APP_HOME /app

WORKDIR APP_HOME

COPY . .

EXPOSE 3000

ENTRYPOINT ["python3", "src/main.py"]