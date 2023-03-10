FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
ENV chromedriverVersion 108.0.5359.71
USER root
WORKDIR /app
ADD . /app
ADD https://chromedriver.storage.googleapis.com/${chromedriverVersion}/chromedriver_linux64.zip /tmp/
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata tesseract-ocr chromium unzip

RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata \
    && unzip /tmp/chromedriver_linux64.zip chromedriver -d /app/

CMD ["python"]