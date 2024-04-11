FROM python:3.11

WORKDIR /business-fleet-manager

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /app app

COPY .env .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app.main:app"]