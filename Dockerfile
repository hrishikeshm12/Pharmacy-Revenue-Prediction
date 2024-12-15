# Dockerfile for Flask app
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
