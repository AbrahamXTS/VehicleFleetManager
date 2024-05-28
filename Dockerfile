FROM python:3.11

WORKDIR /business-fleet-manager

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /app app

# COPY .env .

COPY ./log_conf.yaml .

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app", "--log-config=log_conf.yaml"]