# Architecture Decision Record 001: Architecture Pattern

## Context
The Amadeus project aims to provide predictive scaling and self-healing capabilities for Kubernetes applications.
The system needs to:
1. Observed metrics from Prometheus (CPU, Memory, Request Count).
2. Predict future load using an LSTM model (10-minute lookahead).
3. Act on these predictions by scaling Pods via the Kubernetes API.
4. Detect specific log patterns (OOMKilled, CrashLoopBackOff) for self-healing.

## Options
1. **CronJob**: A scheduled job that runs every X minutes to check metrics and scale.
   - *Pros*: Simple to implement.
   - *Cons*: Not real-time; initialization overhead for each run; difficult to maintain state (e.g., previous predictions).
2. **Custom Controller / Operator**: A long-running process that watches for events or runs a control loop.
   - *Pros*: Real-time (or near real-time) reaction; maintains state (memory of recent metrics); idiomatic to Kubernetes.
   - *Cons*: More complex to implement than a script.
3. **External Service (Webhook)**: A service outside the cluster (or inside) that receives webhooks from Alertmanager.
   - *Pros*: Event-driven.
   - *Cons*: Hard to implement complex logic like "load prediction" which requires continuous data analysis, not just threshold alerts.

## Decision
We will implement the **Custom Controller / Operator Pattern**.
Specifically, we will build a Python-based Operator.

## Rationale
- The "Loop" structure (Observe -> Think -> Act) described in the PRD perfectly matches the Kubernetes Controller pattern.
- We need to maintain a window of recent historical data (e.g., last 60 minutes) for the LSTM model. A persistent process (Operator) can cache this or query it efficiently, whereas a CronJob would need to fetch/load it every time.
- Python is the chosen language, and libraries like `kopf` (Kubernetes Operator Framework) or the official `kubernetes` client make writing operators in Python accessible.
