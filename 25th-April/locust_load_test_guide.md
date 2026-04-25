# Locust Load Testing Guide

## What is Locust?

Locust is an open-source load testing tool written in Python that allows you to write load tests in pure Python code. It's user-friendly, scalable, and provides a web-based UI for monitoring tests in real-time.

## Installation

```bash
# Install Locust
pip install locust

# Verify installation
locust --version
```

---

## Basic Load Test Example

### 1. Simple HTTP Request Load Test

Create a file named `locustfile.py`:

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    @task
    def index(self):
        self.client.get("/")
    
    @task(3)
    def about(self):
        # This task runs 3x more often than index()
        self.client.get("/about")
```

### 2. Run the Test

```bash
# Start Locust with web UI
locust -f locustfile.py

# Open browser to http://localhost:8089
```

The web UI allows you to:
- Set number of users to simulate
- Set spawn rate (users per second)
- Start/stop tests
- Monitor live metrics (RPS, response times, failures)
- View performance graphs

---

## Advanced Example: API Load Testing

Create `api_loadtest.py`:

```python
from locust import HttpUser, task, between, constant
import json
import random

class APIUser(HttpUser):
    wait_time = constant(1)  # Fixed 1 second between requests
    
    def on_start(self):
        """Called when a user starts"""
        self.user_id = random.randint(1, 1000)
        self.headers = {"Content-Type": "application/json"}
    
    @task(1)
    def get_user(self):
        """GET request to fetch user data"""
        response = self.client.get(
            f"/api/users/{self.user_id}",
            name="/api/users/[id]"  # Groups requests by pattern
        )
        if response.status_code == 200:
            self.user_data = response.json()
    
    @task(2)
    def create_post(self):
        """POST request to create a post"""
        payload = {
            "title": f"Test Post {random.randint(1, 100)}",
            "content": "This is a test post",
            "user_id": self.user_id
        }
        self.client.post(
            "/api/posts",
            json=payload,
            name="/api/posts"
        )
    
    @task(1)
    def update_profile(self):
        """PUT request to update user profile"""
        payload = {
            "name": f"User {self.user_id}",
            "email": f"user{self.user_id}@test.com"
        }
        self.client.put(
            f"/api/users/{self.user_id}",
            json=payload,
            name="/api/users/[id]"
        )
    
    @task(1)
    def delete_post(self):
        """DELETE request"""
        post_id = random.randint(1, 100)
        self.client.delete(
            f"/api/posts/{post_id}",
            name="/api/posts/[id]"
        )
```

---

## Running Tests Programmatically

Create `run_loadtest.py`:

```python
from locust import HttpUser, task, between, events
from locust.env import Environment
from locust.contrib.fasthttp import FastHttpUser
import gevent

class TestUser(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def load_index(self):
        self.client.get("/")

def main():
    # Create environment
    env = Environment(user_classes=[TestUser])
    
    # Create a locust runner
    runner = env.create_local_runner()
    
    # Start the test (spawning users)
    runner.spawn_users(user_count=10, spawn_rate=5, wait=True)
    
    # Let it run for 60 seconds
    gevent.sleep(60)
    
    # Stop the test
    runner.stop()
    
    # Print statistics
    print("\n" + "="*60)
    print("LOAD TEST RESULTS")
    print("="*60)
    for key, stats in env.stats.entries.items():
        print(f"\n{key[0]} {key[1]}")
        print(f"  Requests: {stats.num_requests}")
        print(f"  Failures: {stats.num_failures}")
        print(f"  Avg Response Time: {stats.avg_response_time:.2f}ms")
        print(f"  Min Response Time: {stats.min_response_time:.2f}ms")
        print(f"  Max Response Time: {stats.max_response_time:.2f}ms")
        print(f"  RPS: {stats.total_rps:.2f}")

if __name__ == "__main__":
    main()
```

Run it:
```bash
python run_loadtest.py
```

---

## Command Line Options

```bash
# Start with specific host
locust -f locustfile.py --host=http://example.com

# Run without web UI (headless)
locust -f locustfile.py \
  --host=http://example.com \
  --users=100 \
  --spawn-rate=10 \
  --run-time=5m \
  --headless

# Generate HTML report
locust -f locustfile.py \
  --html=report.html \
  --headless \
  --users=50 \
  --spawn-rate=5 \
  --run-time=10m

# Connect to master-slave setup
locust -f locustfile.py --master  # Master
locust -f locustfile.py --worker --master-host=127.0.0.1  # Worker
```

---

## Performance Optimization Tips

### 1. Use FastHttpUser for High Load

```python
from locust.contrib.fasthttp import FastHttpUser

class FastUser(FastHttpUser):
    wait_time = between(1, 2)
    
    @task
    def index(self):
        self.client.get("/")
```

### 2. Custom Logging with Events

```python
from locust import events

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("Load test starting...")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Load test finished!")

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, context, exception, **kwargs):
    if exception:
        print(f"Request failed: {name} - {exception}")
```

### 3. Response Validation

```python
@task
def validate_response(self):
    with self.client.get("/api/data", catch_response=True) as response:
        if response.status_code == 200:
            response.success()
        else:
            response.failure(f"Got status code {response.status_code}")
        
        if response.json()["status"] == "ok":
            response.success()
        else:
            response.failure("Status not OK")
```

---

## Interpreting Results

Key metrics to monitor:

- **RPS (Requests Per Second)**: Throughput of your API
- **Response Time**: How long requests take (avg, min, max, p95, p99)
- **Failure Rate**: % of requests that failed
- **95th Percentile**: Performance for 95% of requests

Example output:
```
 Type      Name                                          # reqs    # fails |    Avg     Min     Max   Med | req/s  failures/s
 GET       /api/users/[id]                               1000        5    | 45.2     12    342   34  | 16.7   0.08
 POST      /api/posts                                     500        2    | 78.3     25    401   65  | 8.3    0.03
 PUT       /api/users/[id]                               500        1    | 52.1     18    289   45  | 8.3    0.02
 DELETE    /api/posts/[id]                               500        0    | 38.5     10    156   32  | 8.3    0.00
```

---

## Real-World Example: E-commerce Site

```python
from locust import HttpUser, task, between
import random

class ShopperUser(HttpUser):
    wait_time = between(2, 5)
    
    def on_start(self):
        self.product_ids = list(range(1, 101))
    
    @task(3)
    def browse_products(self):
        product_id = random.choice(self.product_ids)
        self.client.get(f"/products/{product_id}")
    
    @task(1)
    def search_products(self):
        query = random.choice(["laptop", "phone", "tablet", "watch"])
        self.client.get(f"/search?q={query}")
    
    @task(2)
    def add_to_cart(self):
        product_id = random.choice(self.product_ids)
        self.client.post(f"/cart/add", json={"product_id": product_id})
    
    @task(1)
    def checkout(self):
        self.client.post("/checkout", json={
            "payment_method": "credit_card",
            "shipping_address": "123 Main St"
        })
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Check host URL and ensure target service is running |
| Too many open files | Increase system limits: `ulimit -n 10000` |
| Web UI not accessible | Check firewall and port 8089 |
| High CPU usage | Reduce user count or use FastHttpUser |
| Memory errors | Use workers/distributed testing for large loads |

---

## References

- [Locust Documentation](https://docs.locust.io/)
- [GitHub Repository](https://github.com/locustio/locust)
