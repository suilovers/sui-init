# ubuntu:22.04
FROM homebrew/brew:4.2.20

USER root

# install sudo
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    dos2unix \
    expect \
    && rm -rf /var/lib/apt/lists/*

USER linuxbrew

RUN brew --version
RUN brew install node
RUN brew install yarn

RUN curl -fsSL https://github.com/MystenLabs/sui/releases/download/mainnet-v1.23.1/sui-mainnet-v1.23.1-ubuntu-x86_64.tgz -o sui.tgz
RUN tar -xvzf sui.tgz
RUN sudo mv sui /usr/local/bin/sui
RUN sudo mv sui-test-validator /usr/local/bin/sui-test-validator
RUN sudo chmod +x /usr/local/bin/sui
RUN sudo chmod +x /usr/local/bin/sui-test-validator
RUN rm sui.tgz
ENV PATH="/usr/local/bin:${PATH}"

# Install Rust and Cargo
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
## Add Cargo to PATH
ENV PATH="/home/linuxbrew/.cargo/bin:${PATH}"
RUN cargo --version

WORKDIR /app

RUN python3 --version

ENV backend_path=/app/backend
ENV ui_path=/app/ui

# copy backend and ui folders
COPY backend /app/backend
COPY ui /app/ui

# Install backend dependencies
RUN python3 -m venv /app/venv
RUN . /app/venv/bin/activate
RUN /app/venv/bin/pip3 install -r ${backend_path}/requirements.txt

USER root
# Install ui dependencies
WORKDIR ${ui_path}
RUN yarn

EXPOSE  5000
EXPOSE 3000
# ADD init.sh
WORKDIR /app
COPY init.sh init.sh
COPY expect.sh expect.sh
RUN chmod +x init.sh
RUN dos2unix init.sh
RUN chmod +x expect.sh
RUN dos2unix expect.sh
# CMD ["/bin/sh","./init.sh"]
ENTRYPOINT ["/bin/sh","./init.sh"]
# CMD ["ls"]