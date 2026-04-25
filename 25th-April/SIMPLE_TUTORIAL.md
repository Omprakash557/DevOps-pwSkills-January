# Locust Load Testing - Simple Tutorial

## What is Load Testing?

Load testing simulates multiple users accessing a website/API at the same time to see how it performs under pressure.

**Example:** Instead of 1 person visiting your site, simulate 100 people visiting at once. Does it still work? How fast is it?

---

## Step 1: Install Locust

```bash
pip install locust
```

That's it! Locust is now ready to use.

---

## Step 2: Create a Test File

Create a file called `locustfile.py`:

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def visit_homepage(self):
        self.client.get("/")
```

**What this does:**
- `HttpUser` = simulates a real user
- `wait_time = between(1, 3)` = wait 1-3 seconds between requests
- `@task` = a thing the user does
- `self.client.get("/")` = visit the homepage

---

## Step 3: Run the Test

```bash
locust -f locustfile.py --host=http://example.com
```

Then open your browser to: **http://localhost:8089**

You'll see a form. Fill it in:
- **Number of users:** 10
- **Spawn rate:** 2

Click **Start swarming**

---

## Step 4: Watch the Results

You'll see:
- **RPS** = requests per second (how many visits)
- **Response time** = how long it takes
- **Failures** = if anything breaks

---

## Example: Test an API

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def get_users(self):
        self.client.get("/users")
    
    @task(3)
    def get_posts(self):
        self.client.get("/posts")
```

**What's different:**
- `@task(3)` = this runs 3 times for every 1 time `get_users` runs
- Tasks with higher numbers = more popular requests

---

## Example: Test POST Requests

```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def create_post(self):
        self.client.post("/posts", json={
            "title": "Test",
            "body": "Test content"
        })
```

---

## Common Wait Times

```python
from locust import constant, between

# Random between 1-3 seconds
wait_time = between(1, 3)

# Always exactly 2 seconds
wait_time = constant(2)
```

---

## Common HTTP Methods

```python
# GET - fetch data
self.client.get("/api/users")

# POST - create data
self.client.post("/api/users", json={"name": "John"})

# PUT - update data
self.client.put("/api/users/1", json={"name": "Jane"})

# DELETE - remove data
self.client.delete("/api/users/1")
```

---

## Real Example: Test a Fake API

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class TestUser(HttpUser):
    wait_time = between(1, 2)
    
    @task(2)
    def get_posts(self):
        self.client.get("/posts")
    
    @task(1)
    def get_comments(self):
        self.client.get("/comments")
```

Run it:

```bash
locust -f locustfile.py --host=https://jsonplaceholder.typicode.com
```

This tests a real public API!

---

## Run Without the Web UI

```bash
locust -f locustfile.py \
  --host=http://example.com \
  --users=50 \
  --spawn-rate=5 \
  --run-time=2m \
  --headless
```

**Explanation:**
- `--users=50` = 50 simulated users
- `--spawn-rate=5` = add 5 new users per second
- `--run-time=2m` = run for 2 minutes
- `--headless` = no web UI, just run it

---

## Understanding Results

When you see results like this:

```
Type    Name          # reqs   # fails   Avg      Min      Max
GET     /posts        500      0         45ms     10ms     150ms
GET     /comments     250      2         52ms     15ms     200ms
```

- `# reqs` = 500 requests were made
- `# fails` = 0 requests failed (all successful)
- `Avg` = average response time was 45ms
- `Min/Max` = fastest was 10ms, slowest was 150ms

---

## Quick Checklist

✅ Install: `pip install locust`
✅ Create: `locustfile.py`
✅ Add tasks with `@task`
✅ Set wait time with `wait_time = between(1, 3)`
✅ Run: `locust -f locustfile.py --host=http://example.com`
✅ Open: http://localhost:8089
✅ Set users and spawn rate
✅ Click "Start swarming"
✅ Watch results in real-time

---

## Next Steps

- Read the full guide for advanced features
- Try with your own website
- Test with different user counts
- Look at the HTML reports

**That's it! You now know how to load test.** 🎉
