FROM python:3.9.7

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG APP_USER=appuser

RUN groupadd -r ${APP_USER} -g 1000 && useradd --no-log-init --create-home -u 1000 -r -g ${APP_USER} ${APP_USER}

ARG APP_DIR=/home/${APP_USER}/project/
RUN echo $APP_DIR && mkdir ${APP_DIR} && chown ${APP_USER}:${APP_USER} ${APP_DIR}

COPY ./requirements.txt ${APP_DIR}


RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    postgresql-client \
    python3-dev \
    musl-dev \
    netcat \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r ${APP_DIR}requirements.txt


COPY service ${APP_DIR}
COPY ./local.entrypoint.sh ${APP_DIR}
RUN chmod a+x ${APP_DIR}local.entrypoint.sh && \
    mkdir -p ${APP_DIR}backend-static && \
    mkdir -p ${APP_DIR}media && \
    chown ${APP_USER}:${APP_USER} ${APP_DIR}backend-static && \
    chown ${APP_USER}:${APP_USER} ${APP_DIR}media

#USER ${APP_USER}:${APP_USER}
WORKDIR ${APP_DIR}
EXPOSE 8000

CMD ["sh", "./local.entrypoint.sh"]