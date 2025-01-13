FROM python:3.8.12
# 作業ディレクトリ指定
WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python","manage.py","runserver","0.0.0.0:8000"]

