import requests
import json
import os

# 你的API的URL
BASE_URL = os.getenv("BASE_URL", "http://localhost:8998")
url = BASE_URL + "/tools/database"

# 准备的SQL查询
queries = {
    "queries": [
        '''SELECT * FROM railway
WHERE origin = 'Beijing'
  AND destination = 'Shanghai'
  AND DATE(departure_time) = '2023-07-08'
ORDER BY departure_time;'''
    ]
}
# queries = {"queries":["SELECT * FROM railway\nWHERE origin = 'Shanghai'\n  AND destination = 'Hangzhou'\n  AND DATE(departure_time) = '2023-07-04';"]
# }

# 发送POST请求
response = requests.post(url, json=queries)

# 打印返回的结果
# print(json.dumps(response.json(), indent=4))


def query_database(query):
    try:
        response = requests.post(
            url,
            json={'queries': query}
        ).json()
        return json.dumps(response, indent=4)
    except Exception as e:
        print(f'run error{e}')


query = [
    "SELECT * FROM railway\nWHERE origin = 'Shanghai'\n  AND destination = 'Beijing'\n  AND DATE(departure_time) = '2023-07-01';",
    "SELECT * FROM railway\nWHERE origin = 'Beijing'\n  AND destination = 'Hangzhou'\n  AND DATE(departure_time) = '2023-07-04';",
    "SELECT * FROM railway\nWHERE origin = 'Hangzhou'\n  AND destination = 'Shanghai'\n  AND DATE(departure_time) = '2023-07-07';"]
print(query_database(query))

print(query_database(["INSERT INTO railway (origin, destination, departure_time, arrival_time, price) VALUES ('Shanghai', 'Beijing', '2023-07-01 08:00:00', '2023-07-01 12:00:00', 500);"]))
