# Architecture Decision Record 003: Model Serving Strategy

## Context
The "Think" phase of the loop requires running an LSTM model inference to predict future load.
The Operator needs to:
1. Fetch 60 minutes of data.
2. Preprocess the data.
3. Run `model.predict()`.
4. Use the output to decide the replica count.

## Options
1. **Embedded Model (Monolithic)**: The LSTM model is loaded directly within the Operator's memory/process.
   - *Pros*: Zero network latency for inference; simplest deployment (one Pod); no extra monitoring needed for a serving layer.
   - *Cons*: Operator Pod becomes heavy (needs PyTorch dependencies); scaling the operator (if needed) means duplicating the model; potential memory leaks in long-running Python process affecting the controller.
2. **Model as a Service (Microservice)**: A separate Pod (e.g., using TorchServe or FastAPI) exposes an endpoint (e.g., `/predict`).
   - *Pros*: Decoupled; Operator remains lightweight; Model service can ideally scale independently (though not needed for single-cluster control).
   - *Cons*: Network latency (minimal in cluster); complexity of managing two deployments; defining API contracts.

## Decision
We will use the **Embedded Model (Monolithic)** strategy for the MVP.

## Rationale
- **MVP Focus**: The primary goal is to demonstrate the *logic* and *capability* (Predictive Scaling). Simplicity is key.
- **Scale**: We are controlling a single target application (Google Online Boutique). The inference load (once every 1-5 minutes per metric) is negligible for a modern CPU, even with an LSTM.
- **Latency**: While network latency isn't a huge blocker, eliminating it simplifies the failure domain. If the Operator is up, the "Brain" is up.
- **Future Proofing**: If the model becomes too heavy or we need to control hundreds of apps, we can refactor the "Think" module to call an external API without changing the "Observe" or "Act" logic significantly.
