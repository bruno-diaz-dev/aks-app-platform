# Container Health Dashboard (Platform Demo)

This repository contains a **cloud-native containerized application** designed to demonstrate
**DevOps / Platform Engineering practices**, including containerization, CI/CD pipelines,
and Kubernetes-ready workloads.

The project focuses on **operability and observability**, not on application complexity.

---

## Application Overview

The application is a lightweight **FastAPI-based dashboard** that exposes:

- `/health` — standard health endpoint for Kubernetes probes
- `/` — HTML dashboard showing:
  - container health status
  - CPU usage
  - memory usage
  - container uptime

This mirrors how internal platform services expose health and runtime visibility
for SREs and DevOps teams.

---

## Containerization

The application is packaged as a Docker image using:

- Python 3.11 (slim image)
- FastAPI + Uvicorn
- psutil for runtime metrics
- Jinja2 for lightweight HTML rendering

The Dockerfile is optimized for:
- fast builds
- clean logs
- Kubernetes compatibility

---

## CI/CD Pipeline

This repository includes an **enterprise-style CI/CD pipeline** implemented with GitHub Actions.

### CI (Continuous Integration)

Runs automatically on:
- `push` to `main`
- `pull_request` to `main`

CI responsibilities:
- build Docker image
- run the container
- validate the `/health` endpoint
- fail fast if the application is unhealthy

### CD (Continuous Deployment)

Triggered **manually** via `workflow_dispatch`.

CD responsibilities:
- build release image
- tag image as:
  - `latest`
  - `sha-<commit>`
- push image to GitHub Container Registry (GHCR)

Manual triggering ensures:
- controlled releases
- explicit operator intent
- no accidental deployments

---

## Kubernetes Manifests

The `k8s/` directory contains Kubernetes manifests ready to be applied to any standard cluster:

- `namespace.yaml`
- `deployment.yaml`
- `service.yaml`

Key characteristics:
- readiness and liveness probes using `/health`
- CPU and memory requests/limits defined
- ClusterIP service for internal exposure

The manifests are **cloud-agnostic** and compatible with AKS, EKS, GKE, or local clusters.

---

## Local Development

Build the image locally:

```bash
docker build -t container-health:local ./app
```

Run the container:

```bash
docker run --rm -p 8000:8000 container-health:local
```

Access:

Dashboard: http://localhost:8000/

Health: http://localhost:8000/health

Notes & Roadmap

Kubernetes deployment is intentionally not auto-executed in CI/CD

Manifests are provided and validated, but deployment requires a target cluster

The pipeline is designed to support:

environment approvals

promotion strategies

future GitOps workflows

This repository focuses on platform design and pipeline correctness, not on cloud-specific provisioning.

