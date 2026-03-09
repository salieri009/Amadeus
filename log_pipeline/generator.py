import json
import random
import os

def generate_logs(num_logs: int = 100, output_dir: str = "input_logs"):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "server_logs.jsonl")
    
    ips = [f"192.168.1.{i}" for i in range(1, 20)]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "curl/7.68.0",
        "python-requests/2.25.1"
    ]
    
    with open(file_path, "w", encoding="utf-8") as f:
        for _ in range(num_logs):
            is_error = random.random() < 0.1  # 10% chance for an error status
            is_slow = random.random() < 0.1   # 10% chance for high latency
            
            log = {
                "ip": random.choice(ips),
                "status": random.choice([500, 502, 503, 504]) if is_error else random.choice([200, 201, 301, 302, 400, 401, 403, 404]),
                "user_agent": random.choice(user_agents),
                "response_time_ms": random.randint(5000, 10000) if is_slow else random.randint(10, 1000)
            }
            f.write(json.dumps(log) + "\n")
            
    print(f"Generated {num_logs} logs at {file_path}")

if __name__ == "__main__":
    generate_logs()
