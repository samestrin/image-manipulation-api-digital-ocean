FROM python:3.12-slim
WORKDIR /app
COPY /src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
EXPOSE 5000
CMD ["gunicorn", "src.app:app", "-w", "2", "-b", "0.0.0.0:5000"]