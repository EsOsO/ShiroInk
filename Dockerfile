# temp stage
ARG PYTHON_IMAGE_VERSION=3.13.7-slim

FROM python:${PYTHON_IMAGE_VERSION} AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:${PYTHON_IMAGE_VERSION}

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

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache-dir /wheels/*

RUN addgroup --gid 1000 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1000 --system --group app

USER app

COPY ./src ./

ENTRYPOINT ["python", "main.py"]
CMD [ "--help" ]
