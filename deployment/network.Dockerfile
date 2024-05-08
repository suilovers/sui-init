# Use the official Rust image as the base image
FROM rust:latest

RUN apt-get update && apt-get install -y \ 
    libclang-dev

# Set the working directory inside the container
WORKDIR /app
RUN git clone https://github.com/MystenLabs/sui.git
WORKDIR /app/sui
RUN RUST_LOG="off,sui_node=info" cargo run --bin sui-test-validator

# run forever
CMD ["tail", "-f", "/dev/null"]