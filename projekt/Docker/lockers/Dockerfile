FROM python:3.7-alpine
WORKDIR /home_app

ENV FLASK_APP lockers_app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 5002
ENV FLASK_ENV development

COPY ./home_app /home_app
RUN apk add --no-cache gcc musl-dev linux-headers openssl-dev libffi-dev
RUN pip install -r requirements.txt

CMD ["flask", "run", "--cert", "adhoc"]