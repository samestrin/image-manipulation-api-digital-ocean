FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/ 
RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "server:app", "-w", "2", "-b", "0.0.0.0:5000"]