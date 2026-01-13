# Container Health Dashboard — Platform Engineering Demo

This repository demonstrates **production-oriented Platform / DevOps engineering practices**
using a simple, cloud-native workload as the vehicle.

The goal is **not application complexity**, but to showcase **how a platform is designed,
governed, released, and operated** with enterprise-grade rigor.

---

## What This Repository Demonstrates

- CI/CD correctness and enforcement
- Promotion without rebuilds (build once, promote many)
- Governance via required checks and code ownership
- Kubernetes-ready workloads with clear separation of concerns
- Auditability and rollback via Git history
- Platform thinking over tool-specific implementations

This is a **platform demo**, not a tutorial.

---

## Application Overview

The application is a lightweight **FastAPI-based container health dashboard** exposing:

- `GET /health`  
  Standard health endpoint suitable for Kubernetes liveness/readiness probes

- `GET /`  
  HTML dashboard showing:
  - container health status
  - CPU usage
  - memory usage
  - container uptime

This mirrors how internal platform or SRE-owned services expose runtime data
to support operations and troubleshooting.

---

## Containerization Strategy

The application is packaged as a Docker image using:

- Python 3.11 (slim)
- FastAPI + Uvicorn
- psutil for runtime metrics
- Jinja2 for lightweight HTML rendering

Design goals:

- deterministic builds
- fast startup
- no environment-specific configuration
- suitable for Kubernetes workloads

---

## CI / CD Design Overview

This repository intentionally uses **multiple CI systems** to demonstrate
**tool-agnostic pipeline design**.

- **GitHub Actions**
  - primary CI
  - build and runtime validation
  - release automation

- **Azure DevOps**
  - complementary pipeline
  - enterprise-style security scanning
  - controlled execution on a self-hosted agent

Using more than one CI system is **intentional**, reflecting real-world
security and execution boundary decisions.

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

Container image vulnerability scanning is implemented in **Azure DevOps**
using **Trivy**.

Security behavior:

- scans images before release
- blocks on **HIGH** and **CRITICAL** vulnerabilities
- supports documented and time-bound CVE exceptions when mitigated by architecture

GitHub Actions prioritizes speed and feedback, while Azure DevOps demonstrates
**enterprise security gating**.

---

## Release & Promotion Model

This project follows a strict **build once, promote many** strategy.

- the container image is built **once**
- the same image is promoted across environments
- no environment-specific rebuilds occur

Releases are triggered **manually** to ensure:

- explicit operator intent
- controlled promotions
- no accidental deployments

Image tagging strategy:

- `latest`
- `sha-<commit>`

---

## Platform & Environment Design

Kubernetes configuration is structured using **Kustomize**
to separate platform concerns from application concerns.

### Platform bootstrap

```text
platform/namespaces/
```

- one namespace per environment (`dev`, `stage`, `prod`)
- created once
- not versioned with application releases

---

### Application base

```text
platform/apps/container-health/base/
```

- environment-agnostic manifests
- no namespaces
- no image tags
- reusable across all environments

---

### Environment overlays

```text
platform/apps/container-health/dev
platform/apps/container-health/stage
platform/apps/container-health/prod
```

Each overlay defines:

- target namespace
- promoted image tag

Promotion is performed by updating a Git-tracked `image-tag.txt` file.  
Rollback is achieved via `git revert`.

No rebuilds are required to promote or roll back a release.

---

## Platform Flow

```mermaid
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

Build the image:

```bash
docker build -t container-health:local ./app
```

Run locally:

```bash
docker run --rm -p 8000:8000 container-health:local
```

Access:

- Dashboard: http://localhost:8000/
- Health: http://localhost:8000/health

---

## Governance & Decisions

Significant platform decisions are documented as **Platform Decision Records (PDRs)**:

- `docs/pdr/001-ci-and-governance-enforcement.md`

Some pull requests are intentionally **not merged** to demonstrate:

- required CI checks
- code owner enforcement
- prevention of self-approval

This mirrors real production governance.

---

## Intent

- Kubernetes deployment is intentionally **not auto-executed** in CI/CD
- Manifests are validated but require a target cluster
- The design supports:
  - environment approvals
  - controlled promotions
  - future GitOps workflows

This repository prioritizes **platform design, promotion strategy,
and CI/CD enforcement** over cloud-specific infrastructure provisioning.
