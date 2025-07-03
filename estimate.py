import requests
import json
import os
from dotenv import load_dotenv
 
item = input("Please enter ID: ")
weight = input("and weight(in kg): ")

API_KEY = os.getenv("climatiq_API")
url = "https://api.climatiq.io/data/v1/estimate"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    }

data = {
    "emission_factor":{
        "activity_id": item,
        "data_version": "23.23"
    },
    "parameters":{
        "weight": int(weight),
        "weight_unit": "kg"
    }
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    results = response.json()
    print(f"Name: {results['emission_factor']['name']}")
    print(f"Activity ID: {results['emission_factor']['activity_id']}")
    print(f"Co2e: {results['co2e']}{results['co2e_unit']}")
else:
    print("Error:", response.status_code, response.text)