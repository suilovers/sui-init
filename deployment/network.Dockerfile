# Use the official Rust image as the base image
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \ 
    curl \
    sudo \
    libpq-dev \
    libssl-dev \
    libclang-dev \
    build-essential \
    sed \
    cmake \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app
RUN curl -k -fsSL https://github.com/MystenLabs/sui/releases/download/mainnet-v1.24.1/sui-mainnet-v1.24.1-ubuntu-x86_64.tgz -o sui.tgz
RUN tar -xvzf sui.tgz
RUN sudo mv sui /usr/local/bin/sui
RUN sudo mv sui-test-validator /usr/local/bin/sui-test-validator
RUN sudo chmod +x /usr/local/bin/*
RUN rm -rf sui.tgz
ENV PATH="/usr/local/bin:${PATH}"

# ADD ./config/network.yaml /root/.sui/sui-config/network.yaml
ADD ./scripts/start-network.sh /app/start-network.sh
RUN chmod +x /app/start-network.sh
RUN sui genesis -f --with-faucet
# run forever
RUN sed -i 's/json-rpc-address: "0.0.0.0:9000"/json-rpc-address: "127.0.0.1:9000"/g' /root/.sui/sui_config/fullnode.yaml
CMD ["/bin/sh","/app/start-network.sh"]