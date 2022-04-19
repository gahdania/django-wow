FROM python:3.8-alpine3.10

ARG PROJECT_ENV='production'
ADD src/django_wow /app
ADD ${PROJECT_ENV}.env /app/.env
WORKDIR /app
ADD requirements/*.txt /app/requirements/
RUN set -ex \
    && apk add --no-cache --virtual .build-deps postgresql-dev build-base libffi-dev sshfs \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements/${PROJECT_ENV}.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps


ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ENV PROJECT_ENV $PROJECT_ENV

EXPOSE 80

CMD /app/docker-entrypoint.sh


