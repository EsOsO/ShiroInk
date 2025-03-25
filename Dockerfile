FROM public.ecr.aws/docker/library/python:3.9-alpine
LABEL cc.mansase.name="ShiroInk"
LABEL cc.mansase.author="Massimo Bonvicini"
LABEL org.opencontainers.image.authors="esoso"
LABEL org.opencontainers.image.description="ShiroInk"
LABEL org.opencontainers.image.documentation="https://github.com/esoso/shiroink"
LABEL org.opencontainers.image.licenses="ISC"
LABEL org.opencontainers.image.source="https://github.com/esoso/shiroink"
LABEL org.opencontainers.image.title="ShiroInk"
LABEL org.opencontainers.image.url="https://github.com/esoso/shiroink"
LABEL org.opencontainers.image.vendor="esoso"

RUN addgroup -S shiroink && adduser -S shiro -G shiroink -h /home/shiro -s /bin/bash

WORKDIR /home/shiro

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
USER shiro

COPY ./src ./

ENTRYPOINT ["python", "main.py"]
