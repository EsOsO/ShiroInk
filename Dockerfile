# temp stage
# Pin base image to specific digest for security and reproducibility
ARG PYTHON_IMAGE_VERSION=3.13.7-slim
ARG PYTHON_IMAGE_DIGEST=sha256:5f55cdf0c5d9dc1a415637a5ccc4a9e18663ad203673173b8cda8f8dcacef689

FROM python:${PYTHON_IMAGE_VERSION}@${PYTHON_IMAGE_DIGEST} AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:${PYTHON_IMAGE_VERSION}@${PYTHON_IMAGE_DIGEST}

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

# Preserve directory structure to maintain proper Python imports
COPY --chown=app:app ./src ./src

# Set PYTHONPATH to allow imports from src directory
ENV PYTHONPATH=/app/src

# Use direct python execution since PYTHONPATH is set
ENTRYPOINT ["python", "/app/src/main.py"]
CMD ["--help"]
