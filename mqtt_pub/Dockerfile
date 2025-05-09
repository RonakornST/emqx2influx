FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mqtt_pub_from_csv.py .
COPY cucumber_data.csv .

CMD ["python", "mqtt_pub_from_csv.py"]
