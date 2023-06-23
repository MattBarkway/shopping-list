# Use a base image with Rust and Cargo pre-installed
FROM rust:latest as builder

# Set the working directory in the container
WORKDIR /app

# Copy the Cargo.toml and Cargo.lock files
COPY Cargo.toml Cargo.lock ./

# Build a dummy project to cache dependencies
RUN mkdir src && \
    echo "fn main() {}" > src/main.rs && \
    cargo build --release

# Copy the entire source code
COPY . .

# Build the Actix Web application
RUN cargo build --release

# Use a minimal base image for the final container
FROM debian:buster-slim

# Set the working directory in the container
WORKDIR /app

# Copy the built binary from the builder stage
COPY --from=builder /app/target/release/your_app_name .

# Expose the port your Actix Web application listens on
EXPOSE 8080

# Specify the command to run when the container starts
CMD ["./your_app_name"]
