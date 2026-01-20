FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg wget nodejs npm && apt-get clean
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN wget -O font.ttf 'https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf'
CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:8080", "server:app", "--timeout", "120"]
