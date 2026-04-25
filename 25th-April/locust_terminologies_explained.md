# Locust Terminologies Explained
## Complete Guide to Understanding Load Testing Concepts

---

## Table of Contents
1. [Core Components](#core-components)
2. [User & Behavior Related](#user--behavior-related)
3. [Timing & Execution](#timing--execution)
4. [Performance Metrics](#performance-metrics)
5. [Test Execution Terms](#test-execution-terms)
6. [HTTP Request Related](#http-request-related)
7. [Test Results & Reporting](#test-results--reporting)

---

## Core Components

### 1. **HttpUser**
**Definition:** A base class that simulates a real user making HTTP requests to your application.

**In the Assignment:**
```python
class FlaskAppUser(HttpUser):
    """Simulates a user interacting with the Flask API"""
```

**Explanation:** 
- Each HttpUser instance represents one simulated user
- If you specify 50 users, Locust creates 50 instances of `FlaskAppUser`
- Each user runs independently and makes requests to your Flask app
- Multiple users = multiple concurrent requests (simulating real-world traffic)

**Visual Example:**
```
Locust with 3 users:
┌─ User 1 ──► GET /users
├─ User 2 ──► GET /search?q=alice
└─ User 3 ──► GET /users/1
(All happening simultaneously)
```

---

### 2. **Task**
**Definition:** A method decorated with `@task` that represents an action a user can perform.

**In the Assignment:**
```python
@task(3)
def get_home(self):
    """Task 1: Fetch home page (weight: 3)"""
    self.client.get("/")
```

**Explanation:**
- A task is a unit of work/action in your load test
- Represents a real user behavior (e.g., clicking a button, making an API call)
- Each task contains one or more HTTP requests
- Tasks are selected randomly and executed by simulated users

**Types of Tasks:**

| Task Type | Example | Real-world Scenario |
|-----------|---------|-------------------|
| Simple Task | GET request | User viewing a page |
| Complex Task | Multiple requests | User logging in (auth + load data) |
| Conditional Task | IF statement inside | User follows different paths |

---

### 3. **Task Weight** (Priority/Probability)
**Definition:** A number that determines how likely a task is to be chosen for execution.

**In the Assignment:**
```python
@task(3)      # Weight 3 - Higher chance of being selected
def get_home(self):
    self.client.get("/")

@task(1)      # Weight 1 - Lower chance of being selected
def test_slow_endpoint(self):
    self.client.get("/slow-endpoint")
```

**How Weight Works:**
- Higher weight = More likely to be executed
- Weight is relative (ratio-based)
- Default weight = 1 if not specified

**Weight Calculation Example:**
```
Task 1: @task(3) ──► 3 out of 15 parts ──► 20% probability
Task 2: @task(4) ──► 4 out of 15 parts ──► 26.7% probability
Task 3: @task(2) ──► 2 out of 15 parts ──► 13.3% probability
Task 4: @task(3) ──► 3 out of 15 parts ──► 20% probability
Task 5: @task(1) ──► 1 out of 15 parts ──► 6.7% probability
Task 6: @task(2) ──► 2 out of 15 parts ──► 13.3% probability
        Total: 15 parts
```

**Real-world Use Case:**
- 80% of users view the homepage → `@task(80)`
- 15% search for products → `@task(15)`
- 5% checkout → `@task(5)`

---

### 4. **self.client**
**Definition:** An HTTP client that makes requests to the target application.

**In the Assignment:**
```python
self.client.get("/")                    # GET request
self.client.post("/login", json={...})  # POST request
self.client.put("/users/1", json={...}) # PUT request
```

**Explanation:**
- `self.client` is built into HttpUser
- It's similar to `requests` library but tracks all requests automatically
- Every request made through `self.client` is recorded for metrics
- Supports all HTTP methods: GET, POST, PUT, DELETE, PATCH, etc.

**Why Use self.client instead of requests?**
- Automatically tracks response times
- Records success/failure
- Includes request in reports
- Integrates with Locust's monitoring

---

## User & Behavior Related

### 5. **wait_time**
**Definition:** The time a user waits between completing one task and starting the next.

**In the Assignment:**
```python
wait_time = between(1, 5)
```

**Explanation:**
- This simulates real user behavior (users don't make requests continuously)
- `between(1, 5)` means wait randomly between 1-5 seconds
- Each user waits independently

**Different wait_time Options:**

```python
# Option 1: Random wait between 1-5 seconds
wait_time = between(1, 5)

# Option 2: Constant wait of 2 seconds
wait_time = constant(2)

# Option 3: Custom function
def wait_time(self):
    return random.expovariate(1/5)  # Exponential distribution
```

**Visualization:**
```
User timeline without wait_time:
GET / ──► GET /users ──► GET /search   (instant, unrealistic)

User timeline with wait_time = between(1, 5):
GET / ──[2 sec pause]──► GET /users ──[4 sec pause]──► GET /search
```

**Why It Matters:**
- Realistic behavior = Better stress testing
- Without wait_time, you're not testing real-world conditions
- Server load depends on both request rate AND user behavior

---

### 6. **User Groups/Profiles**
**Definition:** Different types of users with different behaviors.

**Example (Not in assignment but important):**
```python
class AdminUser(HttpUser):
    weight = 1  # 10% of traffic
    wait_time = between(1, 3)
    
    @task
    def view_reports(self):
        self.client.get("/admin/reports")

class RegularUser(HttpUser):
    weight = 9  # 90% of traffic
    wait_time = between(3, 5)
    
    @task
    def browse_products(self):
        self.client.get("/products")
```

---

## Timing & Execution

### 7. **Spawn Rate**
**Definition:** The number of users created per second during the test startup phase.

**In Assignment Example:**
```
Web UI:
- Number of users: 50
- Spawn rate: 5
```

**Explanation:**
- Spawn rate = 5 means 5 new users are created every second
- To reach 50 users: 50 ÷ 5 = 10 seconds
- Prevents overwhelming the target system with instant 50 concurrent requests

**Timeline Example:**
```
Second 0:  5 users active
Second 1:  10 users active
Second 2:  15 users active
Second 3:  20 users active
...
Second 10: 50 users active (target reached)
```

**When to Adjust Spawn Rate:**
- **High spawn rate (e.g., 10):** Quick ramp-up, stress test immediately
- **Low spawn rate (e.g., 1):** Gradual ramp-up, observe how system handles growth
- **Real-world scenario:** Use low spawn rate to simulate realistic traffic growth

---

### 8. **Run Time**
**Definition:** How long the load test runs.

**In Assignment Example:**
```bash
locust -f locustfile.py \
  --run-time 2m \  # Run for 2 minutes
  --headless
```

**Explanation:**
- Specified in seconds (s), minutes (m), or hours (h)
- Examples: `60s`, `2m`, `1h`
- Without `--run-time`, test runs indefinitely (until you stop it)

**Common Scenarios:**
- **Smoke test:** 1-2 minutes (quick validation)
- **Load test:** 10-30 minutes (typical load)
- **Soak test:** 1-8 hours (long-running stability)
- **Spike test:** 2-5 minutes (sudden load increase)

---

### 9. **Ramp-up Period**
**Definition:** The time it takes to reach the target number of users.

**Calculation:**
```
Ramp-up time = Number of users ÷ Spawn rate

Example:
- Users: 100
- Spawn rate: 10 users/second
- Ramp-up: 100 ÷ 10 = 10 seconds
```

**Why It's Important:**
- Helps identify if issues are from gradual load increase or system limits
- In real systems, traffic grows gradually (not all at once)

---

## Performance Metrics

### 10. **Response Time (Latency)**
**Definition:** Time taken for the server to respond to a request (in milliseconds).

**In Assignment Results:**
```
Endpoint    | Median | 95%ile | 99%ile | Average
------------|--------|--------|--------|--------
/           | 20ms   | 45ms   | 80ms   | 25ms
/slow-end   | 2100ms | 2900ms | 3000ms | 2000ms
```

**Different Types:**

| Metric | Meaning | Example |
|--------|---------|---------|
| **Median** | 50% of requests faster, 50% slower | "typical response" |
| **95%ile** | 95% of requests faster | "good response" |
| **99%ile** | 99% of requests faster | "worst acceptable" |
| **Average** | Mean of all responses | "overall trend" |
| **Min** | Fastest response | "best case" |
| **Max** | Slowest response | "worst case" |

**Interpretation:**
```
If Median = 20ms, 95%ile = 45ms:
- Most users experience 20ms response
- 5% of users wait 45ms or more
- Acceptable if target is <100ms
```

---

### 11. **Requests Per Second (RPS/Throughput)**
**Definition:** Number of HTTP requests completed per second.

**In Assignment Example:**
```
If 10 users make 1 request every 5 seconds:
RPS = 10 users ÷ 5 seconds = 2 requests/second

If 100 users make 1 request every 2 seconds:
RPS = 100 ÷ 2 = 50 requests/second
```

**Importance:**
- Shows system's handling capacity
- Higher RPS = Better performance at scale
- Real-world goal: "Must handle 1000 RPS"

---

### 12. **Failure Rate**
**Definition:** Percentage of requests that failed (non-2xx status code or exception).

**In Assignment:**
```
# fails = 5 (out of 150 requests)
Failure rate = (5 ÷ 150) × 100 = 3.3%
```

**What Counts as Failure:**
- HTTP status code ≥ 400 (404, 500, 503, etc.)
- Connection errors (timeout, refused)
- Exception during request

**Acceptable Rates:**
- Production: < 0.1% (99.9% success)
- Testing: < 1% (tolerable for load tests)
- Stress testing: > 5% (system under extreme load)

---

### 13. **Percentile Response Times**

**Understanding Percentiles:**
```
Test with 100 requests sorted by response time:

95th percentile:
  Request 1-95:   ✓ Faster (95% of requests)
  Request 96-100: ✗ Slower (5% of requests, outliers)

99th percentile:
  Request 1-99:   ✓ Faster (99% of requests)
  Request 100:    ✗ Slower (1% of requests, worst cases)
```

**Why Percentiles Matter:**
- **Median (50%):** Representative of "typical" user
- **95%ile:** Most users' experience
- **99%ile:** Captures poor experiences

**Real Example:**
```
API endpoint response times:
10ms, 15ms, 18ms, 20ms, 22ms, ..., 100ms, 150ms, 1000ms

50th percentile (median): 20ms
95th percentile: 85ms (90 requests ≤85ms, 5 requests >85ms)
99th percentile: 120ms (99 requests ≤120ms, 1 request >120ms)
```

---

## Test Execution Terms

### 14. **Headless Mode**
**Definition:** Running Locust from command line without the web UI.

**In Assignment:**
```bash
locust -f locustfile.py \
  --host=http://127.0.0.1:5000 \
  --users 20 \
  --spawn-rate 5 \
  --run-time 2m \
  --headless
```

**Comparison:**

| Mode | How to Start | Display | Use Case |
|------|--------------|---------|----------|
| **Web UI** | `locust` (default) | Dashboard at localhost:8089 | Interactive testing, monitoring |
| **Headless** | `locust --headless` | Console output only | Automated CI/CD, scripting |

---

### 15. **Web UI Dashboard**
**Definition:** Interactive browser interface for running and monitoring tests.

**How to Start:**
```bash
locust -f locustfile.py --host=http://127.0.0.1:5000
# Then open http://localhost:8089
```

**Components:**
```
┌─────────────────────────────────────┐
│  Locust Web UI (localhost:8089)     │
├─────────────────────────────────────┤
│                                     │
│ Number of users: [50]               │
│ Spawn rate: [5]                     │
│ [Start Swarming] [Stop] [Reset]     │
│                                     │
├─────────────────────────────────────┤
│ Statistics Table:                   │
│ Type | Name | # Reqs | # Fails | ... │
├─────────────────────────────────────┤
│ Charts (Real-time graphs):          │
│ - Response time over time           │
│ - RPS over time                     │
│ - Users over time                   │
└─────────────────────────────────────┘
```

---

## HTTP Request Related

### 16. **HTTP Methods (GET, POST, PUT, DELETE)**
**Definition:** Different types of HTTP requests representing different operations.

**In Assignment:**
```python
@task
def get_home(self):
    self.client.get("/")              # Retrieve data (read-only)

@task
def search_users(self):
    self.client.get(f"/search?q={query}")  # GET with query params
```

**Common HTTP Methods:**

| Method | Purpose | Example | Idempotent |
|--------|---------|---------|-----------|
| **GET** | Retrieve data (read-only) | Fetch user list | ✓ Yes |
| **POST** | Create new resource | Create new user | ✗ No |
| **PUT** | Update existing resource | Update user profile | ✓ Yes |
| **DELETE** | Remove resource | Delete user account | ✓ Yes |
| **PATCH** | Partial update | Update one field | ✗ No |

**In Locust:**
```python
self.client.get("/users")
self.client.post("/users", json={"name": "John"})
self.client.put("/users/1", json={"name": "Jane"})
self.client.delete("/users/1")
```

---

### 17. **Query Parameters**
**Definition:** Key-value pairs appended to URL for filtering/searching.

**In Assignment:**
```python
@task
def search_users(self):
    search_term = random.choice(["alice", "bob", "charlie"])
    self.client.get(f"/search?q={search_term}")
    # Actual URL: /search?q=alice
```

**Format:** `?key=value&key2=value2`

**Common Examples:**
```
/search?q=alice          (search query)
/users?page=2&limit=10   (pagination)
/products?sort=price     (sorting)
/items?category=books    (filtering)
```

---

### 18. **Response Status Codes**
**Definition:** Server's response to indicate request success/failure.

**Key Codes:**

| Code | Meaning | Example |
|------|---------|---------|
| **200** | OK (success) | Request succeeded |
| **201** | Created | New resource created |
| **304** | Not Modified | Cached response valid |
| **400** | Bad Request | Invalid parameters |
| **401** | Unauthorized | Authentication required |
| **403** | Forbidden | Access denied |
| **404** | Not Found | Resource doesn't exist |
| **500** | Server Error | Internal error |
| **503** | Service Unavailable | Server overloaded |

**In Assignment:**
```python
# Flask returns status codes
return jsonify(user), 200           # Success
return jsonify({"error": "..."}), 404  # Not found
```

---

### 19. **Timeout**
**Definition:** Maximum time to wait for a response before failing the request.

**In Assignment:**
```python
@task
def test_slow_endpoint(self):
    self.client.get("/slow-endpoint", timeout=10)
    # Wait max 10 seconds for response
```

**Why Use Timeout:**
- Prevents requests from hanging indefinitely
- Realistic (real users don't wait forever)
- Server overload protection

**Default Timeout:** Usually 30 seconds

---

## Test Results & Reporting

### 20. **Statistics Table**
**Definition:** Summary of all requests made during the test.

**In Assignment Example:**
```
Type | Name           | # requests | # failures | Median | 95%ile
-----|----------------|-----------|-----------|--------|-------
GET  | /              | 150       | 0         | 20     | 45
GET  | /users         | 180       | 0         | 22     | 50
GET  | /users/<id>    | 120       | 0         | 18     | 40
GET  | /search        | 140       | 0         | 21     | 48
GET  | /slow-endpoint | 40        | 0         | 2100   | 2900
GET  | /status        | 110       | 0         | 19     | 38
```

**How to Read:**
- **Type:** HTTP method used
- **Name:** Endpoint path
- **# requests:** Total requests made to this endpoint
- **# failures:** Number of failed requests
- **Median:** 50th percentile response time
- **95%ile:** 95th percentile response time

---

### 21. **Locustfile**
**Definition:** Python file containing test definitions (user behaviors, tasks).

**In Assignment:**
```python
# locustfile.py
from locust import HttpUser, task, between

class FlaskAppUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def get_home(self):
        self.client.get("/")
```

**Naming Convention:**
- File must be named `locustfile.py` OR
- Explicitly specify with `-f filename.py`

**What It Contains:**
1. User classes (HttpUser subclasses)
2. Task definitions (@task methods)
3. Wait time specifications
4. Optional: setup/teardown methods

---

### 22. **Test Scenarios**

**Different Load Test Types:**

| Type | Purpose | Duration | Ramp-up | Example |
|------|---------|----------|---------|---------|
| **Smoke Test** | Quick validation | 1-2 min | Instant | 5 users × 1 spawn rate |
| **Load Test** | Normal capacity | 10-30 min | Gradual | 100 users × 10 spawn rate |
| **Stress Test** | Breaking point | 5-30 min | Rapid | Start 100, go to 500 users |
| **Soak Test** | Long-term stability | 1-24 hours | Slow | 50 users × 2 spawn rate |
| **Spike Test** | Sudden traffic burst | 2-5 min | Instant jump | 10 to 1000 users instantly |

---

## Quick Reference Table

| Term | What It Is | Example |
|------|-----------|---------|
| **HttpUser** | Simulated user class | `class FlaskAppUser(HttpUser)` |
| **@task** | User action | `@task def get_home(self)` |
| **Weight** | Task probability | `@task(3)` (20% chance) |
| **self.client** | HTTP request maker | `self.client.get("/")` |
| **wait_time** | Pause between tasks | `wait_time = between(1, 5)` |
| **Spawn rate** | Users/second | 5 users per second |
| **Run time** | Test duration | 2 minutes |
| **Response time** | Server latency | 25ms median |
| **RPS** | Requests/second | 50 RPS throughput |
| **Failure rate** | % failed requests | 2% of requests failed |
| **Headless** | No UI mode | `--headless` flag |
| **Status code** | Response result | 200 (success), 404 (not found) |

---

## Practice Quiz

**Test your understanding:**

1. **If a task has `@task(5)` and another has `@task(10)`, what's the probability each is selected?**
   - Answer: 5/(5+10)=33%, 10/(5+10)=67%

2. **With 100 users and spawn rate of 5, how long to ramp up?**
   - Answer: 100÷5 = 20 seconds

3. **What does 95%ile response time of 100ms mean?**
   - Answer: 95% of requests respond in ≤100ms, 5% take >100ms

4. **Which is more realistic: 0 wait_time or wait_time = between(1, 5)?**
   - Answer: between(1, 5) - simulates real user behavior

5. **In a test, 950 requests succeeded and 50 failed. What's failure rate?**
   - Answer: (50÷1000)×100 = 5%

---

## Real-world Interpretation Example

**Scenario:** Your Flask app under 50 concurrent users for 5 minutes:

```
Statistics:
┌─────────────────────────────────────────────────────┐
│ Endpoint       | Reqs | Failures | Median | 95%ile  │
├─────────────────────────────────────────────────────┤
│ GET /users     | 500  | 0        | 45ms   | 120ms   │
│ GET /search    | 300  | 5        | 150ms  | 450ms   │
│ GET /slow      | 50   | 0        | 2000ms | 2800ms  │
│ POST /create   | 100  | 2        | 80ms   | 200ms   │
└─────────────────────────────────────────────────────┘

Analysis:
✓ /users: Healthy (45ms median, no failures)
⚠ /search: Issues (150ms slow, 1.7% failure rate)
⚠ /slow: Expected (simulates slow operation)
⚠ /create: Some failures (2% failure rate)

Conclusion: 
- /search endpoint needs optimization
- /create needs error handling
- System can handle 50 users (at current performance)
```

---

## Summary

Understanding these terminologies helps you:
1. **Design better load tests** - Right metrics, right duration
2. **Interpret results correctly** - Know what each metric means
3. **Communicate findings** - Use industry standard terms
4. **Optimize performance** - Identify actual bottlenecks
5. **Scale confidently** - Make data-driven decisions

Each term represents a concept that helps you understand how your application performs under load!
