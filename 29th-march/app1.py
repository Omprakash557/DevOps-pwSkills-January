import requests
import math

response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
if response.status_code == 200:
    data = response.content
    print(data)



