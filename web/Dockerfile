FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install opencv-python-headless
RUN apt-get update && apt-get install -y tesseract-ocr-all 

COPY . .
CMD ["python", "app.py"]