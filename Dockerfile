# Build stage
FROM alpine:3.19 AS builder

# Install build dependencies
RUN apk add --no-cache \
    git \
    go \
    gcc \
    g++ \
    make \
    python3 \
    nodejs \
    npm

# Install Hugo
RUN go install -tags extended github.com/gohugoio/hugo@v0.123.6

# Set up the working directory
WORKDIR /src
COPY . .

# Build the site using the full path to Hugo
RUN /root/go/bin/hugo --minify

# Serve stage
FROM nginx:1.25-alpine

# Copy the built site from the builder stage
COPY --from=builder /src/public /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set proper permissions
RUN chmod -R 755 /usr/share/nginx/html

# Expose port 8080
EXPOSE 8080

# Start Nginx
CMD ["nginx", "-g", "daemon off;"] 