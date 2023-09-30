FROM debian:sid
# RUN echo 'deb http://mirror.psu.ac.th/debian/ sid main contrib non-free' > /etc/apt/sources.list
RUN echo 'deb http://mirror.kku.ac.th/debian/ sid main contrib non-free non-free-firmware' >> /etc/apt/sources.list

# RUN apt update -oAcquire::AllowInsecureRepositories=true && apt install -y --allow-unauthenticated deb-multimedia-keyring && apt update && apt upgrade -y
RUN apt update && apt upgrade -y
RUN apt install -y python3 python3-dev python3-pip python3-venv npm build-essential checkinstall cmake pkg-config yasm git libjpeg-dev libgeos-dev

RUN python3 -m venv /venv
ENV PYTHON=/venv/bin/python3

RUN $PYTHON -m pip install poetry uwsgi

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN $PYTHON -m poetry config virtualenvs.create false && $PYTHON -m poetry install --no-interaction --only main

COPY dustpath/web/static/package.json dustpath/web/static/package-lock.json dustpath/web/static/
RUN npm install --prefix dustpath/web/static
RUN cd /app/dustpath/web/static/brython; \
    for i in $(ls -d */); \
    do \
    cd $i; \
    python3 -m brython --make_package ${i%%/}; \
    mv *.brython.js ..; \
    cd ..; \
    done

ENV DUSTPATH_SETTINGS=/app/dustpath-production.cfg

COPY . /app
