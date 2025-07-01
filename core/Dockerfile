# -----------------------------------
# Python base (used for everything)
# -----------------------------------
FROM --platform=${TARGETPLATFORM} python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user
ARG UID=1001
ARG GID=1001
RUN groupadd -g $GID django && \
    useradd -u $UID -g django -m django

RUN echo "Acquire::http::Pipeline-Depth 0;" > /etc/apt/apt.conf.d/99custom && \
    echo "Acquire::http::No-Cache true;" >> /etc/apt/apt.conf.d/99custom && \
    echo "Acquire::BrokenProxy    true;" >> /etc/apt/apt.conf.d/99custom

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential --fix-missing && \
    rm -rf /var/lib/apt/lists/*

# -----------------------------------
# Build python dependencies
# -----------------------------------
FROM base AS builder

# Install Python deps (supports pyproject or requirements.txt)
WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r core/requirements.txt

# -----------------------------------
# Runtime Image
# -----------------------------------
FROM builder AS runner

WORKDIR /app

COPY --from=builder /app/core/entrypoint.sh .
RUN chmod +x entrypoint.sh

RUN apt-get update && apt-get install -y dumb-init && rm -rf /var/lib/apt/lists/*
USER django

COPY --from=builder /app/core .

ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONPATH=/app

# Port and static file handling
EXPOSE 8000

ENTRYPOINT ["dumb-init", "--", "bash", "./entrypoint.sh"]