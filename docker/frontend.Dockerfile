# Use a Node.js base image
FROM node:latest as builder

# Set the working directory in the container
WORKDIR /app

# Copy package.json and yarn.lock files
COPY shopping-list/package.json shopping-list/yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy the entire source code
COPY . .

# Build the Svelte app
RUN yarn build

# Use a lightweight base image for the final container
FROM nginx:alpine

# Copy the built files to the NGINX document root
COPY --from=builder /app/public /usr/share/nginx/html

# Expose the default HTTP port
EXPOSE 80

# Start NGINX server
CMD ["nginx", "-g", "daemon off;"]
