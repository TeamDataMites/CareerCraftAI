FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get -y install tesseract-ocr \
  && apt-get install -y python3 python3-distutils python3-pip \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

RUN apt update \
  && apt-get install ffmpeg libsm6 libxext6 -y

COPY . /app
WORKDIR /app

RUN pip3 install --upgrade pip

# Install Python dependencies
RUN pip3 install fastapi uvicorn python-multipart opencv-python pytesseract pillow flask

# Expose port 80
EXPOSE 8000

# Set the entrypoint for the container
CMD ["python3", "app.py"]
