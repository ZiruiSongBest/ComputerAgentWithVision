import os

import requests
import json

# 基础URL
BASE_URL = os.getenv("BASE_URL", "http://localhost:8998")

# 测试邮件发送API
def test_send_email():
    print("Testing: Send Email API")

    data = {
        "from_email": "hang20145@gmail.com",
        "to_email": "yaohang.li@student.uts.edu.au",
        "subject": "Test Subject",
        "content": "This is a test email."
    }

    response = requests.post(f"{BASE_URL}/gmail/send", json=data)
    if response.status_code == 200:
        print(f"Success: {response.json()}")
    else:
        print(f"Failure: {response.json()}")

# 测试获取最近邮件列表API
def test_list_recent_emails():
    print("Testing: List Recent Emails API")

    response = requests.get(f"{BASE_URL}/gmail/list")
    if response.status_code == 200:
        print(f"Success: {response.json()}")
    else:
        print(f"Failure: {response.json()}")

if __name__ == "__main__":
    test_send_email()
    test_list_recent_emails()