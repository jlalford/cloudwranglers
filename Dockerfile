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

# Install python for contact form handler
RUN apk add --no-cache python3

# Copy the built site from the builder stage
COPY --from=builder /src/public /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy contact form server
COPY app /app

# Set proper permissions
RUN chmod -R 755 /usr/share/nginx/html

# Expose port 8080
EXPOSE 8080

# Start the contact form handler and Nginx
CMD ["sh", "-c", "python3 /app/contact_server.py & nginx -g 'daemon off;'"]
