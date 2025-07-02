import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def autopilot():
    API_KEY = os.getenv("climatiq_API")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "input": "Brystnipp.S. 1/2 - 3/8",
        "region": "DK",
        "unit_type": "weight"
    }

    response= requests.post(
        "https://api.climatiq.io/estimate",
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
            
        

def climatiq():
    API_KEY = os.getenv("climatiq_API")
    url = "https://api.climatiq.io/data/v1/estimate"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }


    payload = {
        "emission_factor": {
            "activity_id": "metals-type_stainless_steel_tube_pipe_fittings_beams_billets_rails_tubes",
            "data_version": "22.22"
        },
        "parameters": {
            "weight": 51,
            "weight_unit": "kg"
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("CO2e Estimate:", data["co2e"], data["co2e_unit"])
        print("Source:", data["emission_factor"]["source"])
    else:
        print("Request failed:", response.status_code, response.text)



if __name__=="__main__":
    autopilot()

