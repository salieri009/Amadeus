# Architecture Decision Record 002: Project Structure

## Context
Amadeus consists of several distinct components:
- **AI/ML Core**: Code for training, evaluating, and saving the LSTM model.
- **Operator**: The runtime logic that interacts with Kubernetes and Prometheus.
- **Manifests**: YAML files for deploying Amadeus and the target application (Google Online Boutique).
- **Simulation/Load Testing**: Locust scripts for generating traffic.

We need a directory structure that organizes these effectively while keeping them accessible.

## Decision
We will use a **Monorepo** structure with the following layout:

```
Amadeus/
├── ADRs/                   # Architectural Decision Records
├── model/                  # AI Core (Training, Evaluation, Data Processing)
│   ├── data/               # Dataset storage (gitignored mostly)
│   ├── notebooks/          # Jupyter notebooks for experimentation
│   ├── src/                # Reusable model code (network definition, training loop)
│   └── weights/            # Trained model artifacts (.pth)
├── operator/               # The Amadeus Controller
│   ├── main.py             # Entry point
│   ├── logic/              # Business logic (scaling, healing)
│   └── k8s/                # K8s client wrappers
├── manifests/              # Kubernetes objects
│   ├── amadeus/            # Deployment for Amadeus itself
│   └── target-app/         # Online Boutique & Monitoring Setup
├── simulation/             # Locust scripts & Chaos Engineering
│   └── locustfile.py
├── tests/                  # Unit and Integration tests
└── README.md
```

## Rationale
- **Simplicity**: A single repository is easier to manage for a team of 1 (Jungwook).
- **Integration**: The Operator needs to import the Model definition to run inference. A monorepo makes sharing code (e.g., model architecture class) straightforward.
- **Deployment**: All manifests and code are in one place, simplifying CI/CD or manual deployment.
