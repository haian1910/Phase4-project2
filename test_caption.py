import base64
import requests
import sys

image_path = "tiger.jpg" if len(sys.argv) <= 1 else sys.argv[1]

with open(image_path, "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

resp = requests.post("https://0i3t2ia4lqpem5-8000.proxy.runpod.net/caption", json={"image": image_b64})
print(resp.json())
