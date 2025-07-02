import requests
import json
import os
from dotenv import load_dotenv

item = input("Please enter product: ")
weight = input("and weight(in kg): ")

print(f"Item: {item}\nWeight: {weight}kg")

load_dotenv()

def autopilot_oneshot():
    API_KEY = os.getenv("climatiq_API")
    url = "https://preview.api.climatiq.io/autopilot/v1-preview3/estimate"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "domain": "general",
        "text": item,
        "parameters": {
            "weight": 100,
            "weight_unit": "kg"
        },
        "year": 2025,
        "region": "DK",
        "region_fallback": True
    }

    response= requests.post(
        url,
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        results = response.json()
        for item in results.get("matches", []):
            print(f"Activity ID: {item['activity_id']}")
            print(f"Name: {item['name']}")
            print(f"Unit Type: {item['unit_type']}")
            print(f"Emission Factor: {item['co2e_factor']['value']} {item['co2e_factor']['unit']}\n")
    else:
        print("Error:", response.status_code, response.text)

if __name__ =="main":
    #autopilot()
    pass