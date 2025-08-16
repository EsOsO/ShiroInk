FROM public.ecr.aws/docker/library/python:3.9-alpine
LABEL cc.mansase.name="ShiroInk"
LABEL cc.mansase.author="Massimo Bonvicini"
LABEL org.opencontainers.image.description="ShiroInk"
LABEL org.opencontainers.image.documentation="https://github.com/esoso/shiroink"
LABEL org.opencontainers.image.source="https://github.com/esoso/shiroink"
LABEL org.opencontainers.image.authors="esoso"
LABEL org.opencontainers.image.url="https://github.com/esoso/shiroink"
LABEL org.opencontainers.image.documentation="https://github.com/esoso/shiroink"
LABEL org.opencontainers.image.vendor="esoso"
LABEL org.opencontainers.image.licenses="ISC"
LABEL org.opencontainers.image.title="ShiroInk"

RUN addgroup -S shinoink && adduser -S shino -G shinoink -h /home/shino -s /bin/bash

WORKDIR /home/shino

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
USER shino

COPY ./src ./

ENTRYPOINT ["python", "main.py"]
