# Sausage Store — Final Project (ITMO, Semester 2)

This is the final project for the second semester of the ITMO program. The goal was to build and deploy the "Sausage Store" — a microservice-based online shop — into a Kubernetes cluster using CI/CD, Helm charts, and database migrations.

## 🧩 Architecture

The system includes:

- `frontend` (Angular, TypeScript)
- `backend` (Java + Spring Boot, PostgreSQL + MongoDB)
- `backend-report` (Go, MongoDB)

The app allows users to add items to a cart, place orders, and generate activity reports.

## 🛠️ Project Structure

```plaintext
├── backend
│   ├── checkstyle.xml
│   ├── Dockerfile
│   ├── pom.xml
│   └── src
│       ├── main
│       └── test
├── backend-report
│   ├── app
│   │   ├── handlers
│   │   ├── models
│   │   ├── repositories
│   │   └── services
│   ├── config
│   │   └── config.go
│   ├── Dockerfile
│   ├── docs
│   │   └── docs.go
│   ├── go.mod
│   ├── go.sum
│   ├── main.go
│   ├── README.md
│   ├── routes
│   │   └── api.go
│   └── utility
│       ├── common.go
│       ├── errors.go
│       └── handler.go
├── frontend
│   ├── angular.json
│   ├── Dockerfile
│   ├── e2e
│   │   ├── protractor.conf.js
│   │   ├── src
│   │   └── tsconfig.e2e.json
│   ├── nginx.tmpl
│   ├── package-lock.json
│   ├── package.json
│   ├── proxy-conf.json
│   ├── src
│   │   ├── app
│   │   ├── browserslist
│   │   ├── environments
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── karma.conf.js
│   │   ├── main.ts
│   │   ├── polyfills.ts
│   │   ├── styles.css
│   │   ├── test.ts
│   │   ├── tsconfig.app.json
│   │   ├── tsconfig.spec.json
│   │   └── tslint.json
│   ├── tsconfig.json
│   └── tslint.json
├── LICENSE
├── README.md
└── sausage-store-chart     # Helm chart for the entire project
    ├── Chart.yaml          # Main chart file
    ├── charts
    │   ├── backend         # Java + Spring Boot application
    │   ├── backend-report  # Go + MongoDB application
    │   ├── frontend        # Angular + TypeScript application
    │   └── infra           # Infrastructure components
    └── values.yaml         # Configuration file for the Helm chart
```

## 🚀 What Was Done

All services were containerized and published to Docker Hub. A multi-stage Dockerfile was used for the frontend to build static files and serve them via NGINX. The backend and backend-report images were also built and tested.

Flyway migrations were configured for PostgreSQL. They include table creation, schema updates, data seeding (with fewer records), and indexing for reporting.

Helm charts were written for each service (`frontend`, `backend`, `backend-report`, `infra`) and combined in a parent chart `sausage-store`. The `values.yaml` file allows configuring image sources, resource limits, domain names, and database connections.

Kubernetes manifests include a PVC for PostgreSQL, LivenessProbe for backend (`/actuator/health`), HPA for `backend-report`, and VPA (recommendation mode) for the backend. Deployment strategies were set: RollingUpdate for the backend and Recreate for backend-report.

An optional `Job` was added to create a MongoDB database and user after deployment (using Helm hooks).

## ⚙️ CI/CD

GitHub Actions were used to automate deployment. Two jobs were created:

- `add_helm_chart_to_nexus`: builds and pushes the chart to a Nexus Helm repo
- `deploy_helm_chart_to_kubernetes`: installs the chart into the Yandex Cloud K8s cluster
