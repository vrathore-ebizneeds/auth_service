FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn","auth_service.wsgi:application","--bind","0.0.0.0:8000"]
