FROM python:3.10-slim

COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt

WORKDIR /app
COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]