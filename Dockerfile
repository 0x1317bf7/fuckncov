FROM python:3.9-alpine3.12

ENV TZ=Asia/Shanghai

COPY *.py /

RUN pip3 install --no-cache-dir -r requirements.py \
    && apk add --no-cache chromium

ENTRYPOINT [ "python3", "-u", "main.py"]
