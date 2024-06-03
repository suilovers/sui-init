FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app
# install sudo
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    dos2unix \
    python3 \
    git \
    python3-venv \
    curl \
    python3-pip \
    expect \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/MystenLabs/sui/releases/download/mainnet-v1.24.1/sui-mainnet-v1.24.1-ubuntu-x86_64.tgz -o sui.tgz
RUN tar -xvzf sui.tgz
RUN sudo mv * /usr/local/bin
RUN sudo chmod +x /usr/local/bin/*
RUN rm -rf *
ENV PATH="/usr/local/bin:${PATH}"

RUN git clone https://github.com/MystenLabs/sui.git /app/sui-repo
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

RUN dos2unix /app/expect.sh
RUN dos2unix /app/init.sh
RUN chmod +x /app/expect.sh
RUN chmod +x /app/init.sh

CMD ["/bin/sh","/app/init.sh"]