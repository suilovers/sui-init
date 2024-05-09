# ubuntu:22.04
FROM ubuntu:20.04

USER root

# install sudo
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    dos2unix \
    expect \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Rust and Cargo
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
## Add Cargo to PATH
RUN ls -la /root
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cargo --version

# location /app
RUN git clone https://github.com/MystenLabs/sui.git
WORKDIR /app/sui
RUN RUST_LOG="off,sui_node=info" cargo run --bin sui-test-validator

# RUN python3 --version

# ENV backend_path=/app/backend
# ENV ui_path=/app/ui

# # copy backend and ui folders
# COPY backend /app/backend
# COPY ui /app/ui

# # Install backend dependencies
# RUN python3 -m venv /app/venv
# RUN . /app/venv/bin/activate
# RUN /app/venv/bin/pip3 install -r ${backend_path}/requirements.txt

# USER root
# # Install ui dependencies
# WORKDIR ${ui_path}
# RUN yarn

EXPOSE  5000
EXPOSE 3000
# ADD init.sh
WORKDIR /app
COPY *.sh ./
RUN chmod +x *.sh
RUN dos2unix *.sh
# CMD ["/bin/sh","./init.sh"]
ENTRYPOINT ["/bin/sh","./init.sh"]
# CMD ["ls"]