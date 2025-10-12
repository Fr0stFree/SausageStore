# Sausage Store — Final Project (ITMO, Semester 3)

This is the final project for the third semester of the ITMO program. The goal was to build and deploy the "Sausage Store" — a microservice-based online shop — into a Kubernetes cluster using CI/CD, Helm charts, and database migrations.

## Useful Links
- [GitHub Project Repository](https://github.com/Fr0stFree/SausageStore)
- [GitLab Project Repository](https://cloud-services-engineer.gitlab.yandexcloud.net/muzyka.frostfree/itmo-iac-hw)
- [ArgoCD Application](https://argocd.infra.students-projects.ru/applications/argocd/sausage-store-frostfree)
- [Nexus Helm Repository](https://nexus.cloud-services-engineer.education-services.ru/#browse/browse:frostfree-sausage-store)
- [Project URL](https://front-frostfree.2sem.students-projects.ru/)
- [Vault URL](http://62.84.126.185:8200/)

## 🧩 Architecture

The system includes:

- `frontend` (Angular, TypeScript)
- `backend` (Java + Spring Boot, PostgreSQL + MongoDB)
- `backend-report` (Go, MongoDB)

The app allows users to add items to a cart, place orders, and generate activity reports.

## 🛠️ Project Structure

```plaintext
.
├── LICENSE
├── README.md
├── ansible
│   ├── ansible.cfg                     # Ansible configuration file
│   ├── inventory
│   │   ├── dynamic_inventory.py        # Dynamic inventory written in Python  
│   │   ├── src
│   │   └── templates
│   ├── roles
│   │   ├── docker                      # Role for installing and configuring Docker
│   │   └── vault                       # Role for installing and configuring HashiCorp Vault
│   └── vault-playbook.yaml             # Ansible playbook for deploying Vault
├── backend                             # Java + Spring Boot application
├── backend-report                      # Go + MongoDB application
├── frontend                            # Angular + TypeScript application
├── infra                               # Infrastructure as Code (Terraform)
│   ├── custom_policies
│   │   └── ensure_yandex_instance_has_labels.yml
│   ├── output.tf
│   ├── provider.tf
│   ├── templates
│   │   └── cloud-init.yaml.tmpl        # Cloud-init template for VM setup
│   ├── terraform.tfvars
│   ├── test
│   │   ├── go.mod
│   │   ├── go.sum
│   │   └── vm_availability_test.go     # Basic test for VM availability
│   ├── variables.tf
│   ├── vm-dev.tf
│   ├── vm-prod.tf
│   └── vpc.tf
└── sausage-store-chart                 # Helm chart for the entire project
    ├── Chart.yaml                      # Main chart file
    ├── charts
    │   ├── backend                     # Java + Spring Boot application
    │   ├── backend-report              # Go + MongoDB application
    │   ├── frontend                    # Angular + TypeScript application
    │   └── infra                       # Infrastructure components
    └── values.yaml                     # Configuration file for the Helm chart
```

## 🚀 What Was Done

All services were containerized and published to Docker Hub. A multi-stage Dockerfile was used for the frontend to build static files and serve them via NGINX. The backend and backend-report images were also built and tested.

Flyway migrations were configured for PostgreSQL. They include table creation, schema updates, data seeding (with fewer records), and indexing for reporting.

Helm charts were written for each service (`frontend`, `backend`, `backend-report`, `infra`) and combined in a parent chart `sausage-store`. The `values.yaml` file allows configuring image sources, resource limits, domain names, and database connections.

Kubernetes manifests include a PVC for PostgreSQL, LivenessProbe for backend (`/actuator/health`), HPA for `backend-report`, and VPA (recommendation mode) for the backend. Deployment strategies were set: RollingUpdate for the backend and Recreate for backend-report.

An optional `Job` was added to create a MongoDB database and user after deployment (using Helm hooks).

## ⚙️ CI/CD

The project uses a GitLab-based CI/CD pipeline that automates the full lifecycle of infrastructure and application delivery. The pipeline supports three operational modes — Terraform, Ansible, and Kubernetes (Helm) — selected via the OPERATION variable. In Terraform mode, it scans, plans, applies, and tests cloud infrastructure changes using Terraform and Terratest. In Ansible mode, it connects to provisioned instances via SSH and configures services through automated playbooks. In Kubernetes mode, the pipeline builds and pushes Docker images for all services and packages a Helm chart for deployment. Sensitive data such as SSH keys, Vault tokens, and Docker credentials are securely injected as GitLab CI variables. Manual approval is required for critical stages like applying Terraform changes or packaging Helm charts, ensuring control and safety. Overall, the pipeline provides a unified, secure, and reproducible process for deploying infrastructure and applications across different environments.
