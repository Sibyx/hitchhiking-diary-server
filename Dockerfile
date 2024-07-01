FROM python:3.12-slim as builder

# System setup
RUN apt update -y && apt install -y libffi-dev build-essential libsasl2-dev libpq-dev

# Application destination
WORKDIR /usr/src/app

# Copy source
COPY . .

RUN pip install -r requirements.txt --no-cache-dir && \
    pip freeze -l > packages.txt && \
    pip wheel -w wheels -r packages.txt && \
    find ./wheels -type f -name "*.whl"  -printf "%f\n" > wheels/requirements.txt

FROM python:3.12-slim

# System setup
RUN apt update -y && apt install -y supervisor curl postgresql-client argon2 tzdata

# Copy application and dependencies
COPY --from=builder /usr/src/app /usr/src/app

# Install dependencies
WORKDIR /usr/src/app/wheels
RUN pip install -r requirements.txt

# Prepare app
WORKDIR /usr/src/app

RUN rm -rf wheels
RUN date -I > BUILD.txt
RUN mkdir /var/log/uvicorn

# Configuration
COPY conf/supervisor.conf /etc/supervisord.conf
RUN chmod +x conf/entrypoint.sh

# Timezone setup
RUN ln -sf /usr/share/zoneinfo/Europe/Bratislava /etc/localtime

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8000/api/v1/status || exit 1

# Execution
RUN chmod +x conf/entrypoint.sh
CMD ["conf/entrypoint.sh"]
