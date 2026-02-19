# Architecture Decision Record 004: Data Storage for Training

## Context
To train the LSTM model, we need a historical dataset of metrics (CPU, Memory, Request Count).
Prometheus holds this data, but:
1. Retention might be short (default 15 days).
2. Querying large ranges for training (e.g., 10k data points) repeatedly is inefficient and can stress the monitoring system.
3. ML workflows typically require static files (CSV/Parquet) for reproducibility and versioning.

## Decision
We will use **CSV/Parquet files** for the training dataset.

## Rationale
- **Phase 1 (Data Collection)**: We will write a script (`collector.py`) that queries Prometheus for specific time ranges and saves the results to `model/data/train.csv`.
- **Reproducibility**: Having a static file ensures that every training run uses the exact same data, which is crucial for debugging model performance.
- **Simplicity**: CSVs are universally supported by `pandas` and `PyTorch` datasets.
- **Online Learning**: For the "Self-Healing/Fine-tuning" phase later, the Operator can maintain a small buffer of recent data in memory or append to a local log file, but the bulk pre-training will rely on exported files.
