FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app
# install sudo
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    dos2unix \
    python3 \
    python3-venv \
    python3-pip \
    expect \
    && rm -rf /var/lib/apt/lists/*

COPY ./backend/requirements.txt /app

# Install backend dependencies
RUN python3 -m venv /app/venv
RUN . /app/venv/bin/activate
RUN /app/venv/bin/pip3 install -r /app/requirements.txt

COPY ./backend /app
EXPOSE 5000
ADD ./scripts/expect.sh /app/expect.sh
ADD ./scripts/init.sh /app/init.sh
ENV FLASK_APP=app.py

CMD ["/bin/sh","/app/init.sh"]