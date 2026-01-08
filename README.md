# Container Health Dashboard — Platform Engineering Demo

This repository contains a **cloud-native, containerized application** designed to demonstrate
**Platform / DevOps engineering practices**, with emphasis on:

- operability
- promotion strategies
- CI/CD correctness
- Kubernetes-ready workloads

The focus of this project is **platform design and lifecycle management**, not application complexity.

---

## Application Overview

The application is a lightweight **FastAPI-based dashboard** that exposes:

- `/health` — standard health endpoint for Kubernetes probes
- `/` — HTML dashboard displaying:
  - container health status
  - CPU usage
  - memory usage
  - container uptime

This mirrors how internal platform or SRE-owned services expose runtime visibility
to support operations and troubleshooting.

---

## Containerization

The application is packaged as a Docker image using:

- Python 3.11 (slim base image)
- FastAPI + Uvicorn
- psutil for runtime metrics
- Jinja2 for lightweight HTML rendering

The Docker image is designed to be:

- fast to build
- deterministic
- suitable for Kubernetes workloads
- free of environment-specific configuration

---

## CI / CD Design Overview

This repository intentionally demonstrates **tool-agnostic CI/CD design** using
multiple CI platforms.

- **GitHub Actions** — primary CI and release automation
- **Azure DevOps** — complementary pipeline showcasing enterprise security scanning
  on a self-hosted agent

Different platforms are used **by design** to demonstrate architectural decisions
around security boundaries, execution environments, and control.

---

## Continuous Integration (CI)

CI runs automatically on:

- `push` to `main`
- `pull_request` targeting `main`

CI responsibilities:

- build the Docker image
- run the container
- validate the `/health` endpoint
- fail fast if the application is unhealthy

CI focuses strictly on **build correctness and runtime validation**.

---

## Security & Image Scanning

Container image vulnerability scanning is implemented in the **Azure DevOps pipeline**
using **Trivy**.

Security responsibilities include:

- image scanning before release
- blocking on **HIGH** and **CRITICAL** vulnerabilities
- allowing documented and temporary CVE exceptions when mitigated by architecture

GitHub Actions focuses on automation and speed, while Azure DevOps demonstrates
**enterprise-style security gating** on a controlled execution environment.

---

## Release & Promotion Model

This project follows a **build once, promote many** strategy.

- The container image is built **once**
- The same image is promoted across environments
- No environment-specific rebuilds occur

Release actions are triggered **manually** to ensure:

- explicit operator intent
- controlled releases
- no accidental deployments

Images are tagged as:

- `latest`
- `sha-<commit>`

---

## Platform & Environment Design

Kubernetes configuration is structured to clearly separate responsibilities using **Kustomize**.

### Platform bootstrap

```text
platform/namespaces/
```

- One namespace per environment (`dev`, `stage`, `prod`)
- Created once
- Not versioned with application releases

### Application base

```text
platform/apps/container-health/base/
```

- Environment-agnostic manifests
- No namespaces
- No image tags
- Reusable across all environments

### Environment overlays

```text
platform/apps/container-health/dev
platform/apps/container-health/stage
platform/apps/container-health/prod
```

Each environment overlay defines:

- target namespace
- promoted image tag

Promotion is performed by updating a Git-tracked `image-tag.txt` file.  
Rollback is achieved via `git revert`.

No rebuilds are required to promote or roll back a release.

---

## Platform Flow Diagram

```text
                   ┌─────────────────────┐
                   │     Developer        │
                   │   (git commit)       │
                   └─────────┬───────────┘
                             │
                             ▼
                  ┌───────────────────────┐
                  │   CI – GitHub Actions  │
                  │───────────────────────│
                  │ • Build Docker image  │
                  │ • Run container       │
                  │ • Validate /health    │
                  └─────────┬─────────────┘
                            │
                            ▼
              ┌──────────────────────────────┐
              │  Container Registry (GHCR)   │
              │──────────────────────────────│
              │ ghcr.io/.../container-health │
              │ tags:                         │
              │  • sha-<commit>              │
              │  • latest                    │
              └─────────┬────────────────────┘
                        │
                        │  (no rebuilds)
                        │
        ┌───────────────┼────────────────────────┐
        │               │                        │
        ▼               ▼                        ▼
┌──────────────┐  ┌──────────────┐     ┌──────────────┐
│  DEV Overlay │  │ STAGE Overlay │     │  PROD Overlay│
│──────────────│  │──────────────│     │──────────────│
│ image-tag.txt│  │ image-tag.txt│     │ image-tag.txt│
│ namespace:   │  │ namespace:   │     │ namespace:   │
│  -dev        │  │  -stage      │     │  -prod       │
└──────┬───────┘  └──────┬───────┘     └──────┬───────┘
       │                 │                      │
       ▼                 ▼                      ▼
┌──────────────┐  ┌──────────────┐     ┌──────────────┐
│  AKS / K8s   │  │  AKS / K8s   │     │  AKS / K8s   │
│ container-   │  │ container-   │     │ container-   │
│ health-dev   │  │ health-stage │     │ health-prod  │
└──────────────┘  └──────────────┘     └──────────────┘
```

---

## Local Development

```bash
docker build -t container-health:local ./app
```

```bash
docker run --rm -p 8000:8000 container-health:local
```

Access:

- Dashboard: http://localhost:8000/
- Health: http://localhost:8000/health

---

## Notes & Intent

- Kubernetes deployment is intentionally **not auto-executed** in CI/CD
- Manifests are validated but require a target cluster
- The design supports:
  - environment approvals
  - promotion strategies
  - future GitOps workflows

This repository intentionally focuses on **platform design, promotion strategy,
and CI/CD correctness**, rather than cloud-specific infrastructure provisioning.
# test
# test
