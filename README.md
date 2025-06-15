# Cloud Wranglers Website

This repository contains the source for the **Cloud Wranglers** website. The site is built with [Hugo](https://gohugo.io/) and packaged for deployment via Docker and Helm.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Helm](https://helm.sh/) and access to a Kubernetes cluster (for deployment)
- [Hugo](https://gohugo.io/) (optional, for local development)

## Local Development

Run Hugo's development server to test changes locally:

```bash
hugo server -D
```

The site will be available at <http://localhost:1313>.

## Building and Running with Docker

Build the container image from the repository root:

```bash
docker build -t cloudwranglers/website .
```

Run the container:

```bash
docker run --rm -p 8080:8080 cloudwranglers/website
```

The site will be served on <http://localhost:8080>.

## Deploying with Helm

A Helm chart is provided in `helm/cloudwranglers`.
Install it to your cluster (namespace defaults to `cloudwranglers-site`):

```bash
helm install cloudwranglers ./helm/cloudwranglers \
  --namespace cloudwranglers-site --create-namespace
```

You can override settings using `--set` flags or a custom values file.
See `helm/EXTERNAL_ACCESS.md` for detailed options like ingress or load balancer configuration.


