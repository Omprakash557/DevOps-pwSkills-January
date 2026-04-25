"""
SIMPLEST LOCUST EXAMPLE
Run with: locust -f simple_locustfile.py --host=https://jsonplaceholder.typicode.com
Then open: http://localhost:8089
"""

from locust import HttpUser, task, between

class SimpleUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def get_posts(self):
        self.client.get("/posts")
