# Build stage
FROM golang:1.22-alpine AS builder

# Install git and build dependencies
RUN apk add --no-cache git gcc g++ musl-dev

# Install Hugo (version compatible with Go 1.22)
RUN go install -tags extended github.com/gohugoio/hugo@v0.123.6

# Set up the working directory
WORKDIR /src
COPY . .

# Build the site
RUN hugo --minify

# Serve stage
FROM nginx:alpine

# Copy the built site from the builder stage
COPY --from=builder /src/public /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"] 