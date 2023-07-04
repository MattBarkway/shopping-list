# Use a Node.js base image
FROM node:19.8.1-alpine as builder

# Set the working directory in the container
WORKDIR /app

# Copy package.json and yarn.lock files
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install --immutable

# Copy the entire source code
COPY . .

# Build the Svelte app
RUN yarn build

# Use a lightweight base image for the final container
FROM nginx:alpine

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the prerendered HTML file from the build stage to the Nginx directory
COPY --from=builder /app/build /usr/share/nginx/html

# Expose the default HTTP port
EXPOSE 80

# Start NGINX server
CMD ["nginx", "-g", "daemon off;"]
