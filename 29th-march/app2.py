import requests

payload = {
    'title': 'My Post', 
    'body': 'body123', 
    'userId': 1
    }

# json -> key <> value pair
# title, body, userId -> key
# My Post, body123, 1 -> value

response = requests.post('https://jsonplaceholder.typicode.com/posts', 
 json=payload)


if response.status_code == 201:
    data = response.json()
    print(data)     

# post api -> send the data from client to server
# post data -> payload