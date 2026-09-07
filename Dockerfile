FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY dashboard ./dashboard

ARG APP_VERSION=1.0.0
ENV APP_ENV=production
ENV APP_VERSION=$APP_VERSION
ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
