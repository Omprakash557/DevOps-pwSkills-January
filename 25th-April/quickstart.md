# Flask + Locust Load Testing Complete Guide

## Part 1: Virtual Environment Setup

### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install locust flask
```

### Windows
```bash
python3 -m venv venv
venv\Scripts\activate
pip install locust flask
```

---

## Part 2: Flask Application

Create `app.py`:

```python
from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

# Sample user data
USERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]

@app.route('/')
def home():
    """Home endpoint"""
    return "Welcome to Flask Load Testing Demo!"

@app.route('/api/users')
def get_all_users():
    """Get all users"""
    return jsonify(USERS)

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    """Get specific user by ID"""
    user = next((u for u in USERS if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/api/search')
def search():
    """Search endpoint"""
    return jsonify({"results": [USERS[0], USERS[1]]})

@app.route('/api/slow')
def slow_endpoint():
    """Intentionally slow endpoint for testing"""
    time.sleep(random.uniform(1, 3))
    return jsonify({"status": "slow response completed"})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Run Flask App

```bash
python app.py
```

You'll see:
```
 * Running on http://127.0.0.1:5000
```

### Test the endpoints in your browser:
- http://127.0.0.1:5000/
- http://127.0.0.1:5000/health
- http://127.0.0.1:5000/api/users
- http://127.0.0.1:5000/api/users/1
- http://127.0.0.1:5000/api/search
- http://127.0.0.1:5000/api/slow

---

## Part 3: Locust Test File

Create `locustfile.py` **in a new terminal** (keep Flask running):

```python
from locust import HttpUser, task, between
import random

class FlaskUser(HttpUser):
    """Simulates a user interacting with the Flask API"""
    
    # Wait 1-3 seconds between requests
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when user starts"""
        self.user_id = random.randint(1, 3)
    
    @task(5)
    def home(self):
        """Visit home - runs 5x more often"""
        self.client.get("/")
    
    @task(3)
    def get_all_users(self):
        """Get all users - runs 3x more often"""
        self.client.get("/api/users")
    
    @task(2)
    def get_specific_user(self):
        """Get specific user - runs 2x more often"""
        self.client.get(f"/api/users/{self.user_id}")
    
    @task(2)
    def search(self):
        """Search endpoint - runs 2x more often"""
        self.client.get("/api/search")
    
    @task(1)
    def slow_endpoint(self):
        """Slow endpoint - runs 1x less often"""
        self.client.get("/api/slow")
    
    @task(2)
    def health_check(self):
        """Health check - runs 2x more often"""
        self.client.get("/health")
```

---

## Part 4: Running Load Tests

### Option A: Web UI Mode (Recommended for Beginners)

```bash
locust -f locustfile.py --host=http://127.0.0.1:5000
```

Then open your browser: **http://localhost:8089**

**Steps:**
1. Enter number of users: **20**
2. Enter spawn rate: **5**
3. Click **Start swarming**

**What you'll see:**
- Real-time request count
- Average response time
- Failure rate
- Requests per second (RPS)

### Option B: Headless Mode (Automated Testing)

```bash
locust -f locustfile.py \
  --host=http://127.0.0.1:5000 \
  --users=20 \
  --spawn-rate=5 \
  --run-time=2m \
  --headless
```

**Parameters explained:**
- `--users=20` → 20 simulated users
- `--spawn-rate=5` → Add 5 users per second
- `--run-time=2m` → Run for 2 minutes
- `--headless` → No web UI, just output

---

## Part 5: Understanding Results

When you run the test, you'll see output like:

```
 Type     Name                     # reqs    # fails |    Avg     Min     Max   Med | req/s  failures/s
 GET      /                        1000        0     | 15.2      5      45    12  | 16.7   0.00
 GET      /api/search               200        0     | 18.3      8      52    15  | 3.3    0.00
 GET      /api/slow                 100        0     | 2234.5   1012   2998  2100 | 1.7    0.00
 GET      /api/users                300        0     | 12.5      4      38    10  | 5.0    0.00
 GET      /api/users/[id]           200        0     | 14.2      6      41    11  | 3.3    0.00
 GET      /health                   300        0     | 11.8      3      35    9   | 5.0    0.00
```

**Column meanings:**

| Column | Meaning |
|--------|---------|
| `Type` | HTTP method (GET, POST, etc.) |
| `Name` | Endpoint path |
| `# reqs` | Total requests made |
| `# fails` | Failed requests |
| `Avg` | Average response time (ms) |
| `Min` | Fastest response |
| `Max` | Slowest response |
| `Med` | Median response time |
| `req/s` | Requests per second |

---

## Part 6: Assignment Checklist

### ✅ Part 1: Flask Application (6 Endpoints)
- [ ] `/` → Home
- [ ] `/api/users` → Get all users
- [ ] `/api/users/<id>` → Get specific user
- [ ] `/api/search` → Search endpoint
- [ ] `/api/slow` → Slow endpoint (intentional delay)
- [ ] `/health` → Health check

### ✅ Part 2: Locust Test File
- [ ] Multiple tasks with different weights
- [ ] `@task(5)` for common actions
- [ ] `@task(1)` for rare actions
- [ ] Random wait times: `between(1, 3)`
- [ ] Dynamic user IDs: `random.randint(1, 3)`

### ✅ Part 3: Run Tests Two Ways
- [ ] **Web UI mode:** `locust -f locustfile.py --host=http://127.0.0.1:5000`
- [ ] **Headless mode:** With `--users`, `--spawn-rate`, `--run-time`, `--headless`

---

## Appendix: Core Concepts Explained

### 1. HttpUser - Virtual User

```python
class FlaskUser(HttpUser):
    wait_time = between(1, 3)
```

- Represents one simulated user
- If you set `--users=20`, Locust creates 20 instances
- Each user runs tasks independently
- Each user has its own `self.client` for making requests

### 2. Tasks - What Users Do

```python
@task
def get_users(self):
    self.client.get("/api/users")
```

- Tasks are what your simulated users do
- Pick from multiple tasks randomly
- Tasks should simulate real user behavior

### 3. Task Weight - Probability

```python
@task(5)
def home(self):
    self.client.get("/")

@task(1)
def slow_endpoint(self):
    self.client.get("/api/slow")
```

**How it works:**
- `home` has weight 5
- `slow_endpoint` has weight 1
- Ratio: 5:1
- `home` runs ~5 times for every 1 time `slow_endpoint` runs

**Example:** With these weights:
- 100 total actions
- ~83 will be `home` (5/6 of 100)
- ~17 will be `slow_endpoint` (1/6 of 100)

### 4. self.client - HTTP Client

```python
self.client.get("/path")      # GET request
self.client.post("/path")     # POST request
self.client.put("/path")      # PUT request
self.client.delete("/path")   # DELETE request
```

- Better than `requests` library for load testing
- Automatically collects statistics
- Better for distributed testing
- Built specifically for Locust

### 5. Spawn Rate - User Creation Speed

```bash
locust --users=100 --spawn-rate=10
```

- **`--users=100`** → Total target is 100 users
- **`--spawn-rate=10`** → Add 10 users per second
- **Time to reach 100 users** → 100 ÷ 10 = 10 seconds

**Why it matters:**
- Low spawn rate = gradual load increase (realistic)
- High spawn rate = sudden load spike (stress test)

### 6. Run Time - Test Duration

```bash
locust --run-time=2m    # 2 minutes
locust --run-time=30s   # 30 seconds
locust --run-time=1h    # 1 hour
```

### 7. Ramp-up Period - Gradual Load

With `--spawn-rate=5` and `--users=100`:
- **0-20 seconds:** Users gradually increase from 0 to 100
- **20-120 seconds:** Steady load at 100 users
- **120+ seconds:** Wind down, users stop

**Why gradual is important:**
- Catches issues at different load levels
- More realistic user behavior
- Better insight into system limits

---

## Complete Command Reference

### Web UI (Interactive)
```bash
locust -f locustfile.py --host=http://127.0.0.1:5000
```

### Headless (Automated)
```bash
locust -f locustfile.py \
  --host=http://127.0.0.1:5000 \
  --users=50 \
  --spawn-rate=10 \
  --run-time=5m \
  --headless
```

### Generate Report
```bash
locust -f locustfile.py \
  --host=http://127.0.0.1:5000 \
  --users=50 \
  --spawn-rate=10 \
  --run-time=5m \
  --headless \
  --html=report.html
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Make sure Flask is running in another terminal |
| Port already in use | Change Flask port: `app.run(port=5001)` |
| No web UI showing | Open http://localhost:8089 in browser |
| Tests not starting | Check `--host` URL is correct |
| All requests failing | Verify Flask endpoints exist |

---

## Next Steps

1. ✅ Run the basic setup
2. ✅ Test with 20 users
3. ✅ Increase to 100 users and watch metrics
4. ✅ Add more endpoints to Flask
5. ✅ Add more tasks to the test file
6. ✅ Generate and save reports
