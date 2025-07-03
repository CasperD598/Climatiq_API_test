import requests
import json
import os
from dotenv import load_dotenv

list = [
    ("bearing nuts",1.07),
    ("Earth moving machinery",455),
    ("exterior finishing materials",5),
    ("pipe anchors",1119.8),
    ("fabrics and leather materials",3.78),
    ("Hardware",86),
    ("insulation",5),
    ("interior finishing materials",133.5),
    ("plumbing fixtures",11.38)
]
result_list = []
no_result = []

#Get api key
load_dotenv()
API_KEY = os.getenv("climatiq_API")

#Oneshot function where Climatiq returns and co2e estimate of
#what it thinks the text means
def autopilot_oneshot(key, item):

    url = "https://preview.api.climatiq.io/autopilot/v1-preview3/estimate"

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    data = {
        "domain": "manufacturing",
        "text": item[0],
        "parameters": {
            "weight": float(item[1]),
            "weight_unit": "kg"
        },
        "year": 2025,
        "region": "DE",
        "region_fallback": True
    }

    response= requests.post(
        url,
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        results = response.json()
        #print(f"Name: {results["estimate"]["emission_factor"]["name"]}")
        #print(f"Activity ID: {results["estimate"]["emission_factor"]["activity_id"]}")
        #print(f"Co2e: {results["estimate"]["co2e"]}{results["estimate"]["co2e_unit"]}")
        return (results["estimate"]["emission_factor"]["name"],
                f"{results["estimate"]["co2e"]}{results["estimate"]["co2e_unit"]}",
                results["estimate"]["emission_factor"]["source_dataset"],
                item[0],
                item[1])
    else:
        print("Error:", response.status_code, response.text)

#Return activity_id for what Climatiq thinks the text means
def autopilot_suggest(key, item):
    url = "https://preview.api.climatiq.io/autopilot/v1-preview3/suggest"

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    data = {
        "suggest": {
            "domain": "manufacturing",
            "text": item[3],
            "unit_type": ["weight"]
        },
        "max_suggestions": 4
    }

    response = requests.post(url, headers=headers, json=data)
    
    suggestions = []

    if response.status_code == 200:
        results = response.json()
        for itemm in results.get("results", []):
            if itemm["emission_factor"]["access_type"] == "public":
                suggestions.append(itemm["suggestion_id"])
    else:
        print("Error:", response.status_code, response.text)

    suggest_est(key, suggestions, item[4])    




        
def suggest_est(key, suggest_array, weight):
    url = "https://preview.api.climatiq.io/autopilot/v1-preview3/suggest/estimate"

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    second_try = []
    for suggestion in suggest_array:
        data = {
            "suggestion_id": suggestion,
            "parameters": {
                "weight": float(weight),
                "weight_unit": "kg"
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            print(f"Name: {result["estimate"]["emission_factor"]["name"]}")
            print(f"Category: {result["estimate"]["emission_factor"]["category"]}")
            print(f"Activity id: {result["estimate"]["emission_factor"]["activity_id"]}")
            print(f"Co2e: {result["estimate"]["co2e"]}{result["estimate"]["co2e_unit"]}\n")
            second_try.append((result["estimate"]["emission_factor"]["name"],f"{result["estimate"]["co2e"]}{result["estimate"]["co2e_unit"]}"))
        else:
            print("Error:", response.status_code, response.text)

    return second_try

if __name__ == "__main__":
    #selector = input("Press 1 for one-shot or 2 for suggest: ")
    #if int(selector) == 1:
    #    autopilot_oneshot(API_KEY)
    #elif int(selector) == 2:
    #    autopilot_suggest(API_KEY)
    for item in list:
        result = autopilot_oneshot(API_KEY, item)
        if result[1] != "0.0kg":
            result_list.append(result)
        else:
            no_result.append(result)

    for item in result_list:
        print(item)
    print("")
    for item in no_result:
        print(item)
        #sec_result = autopilot_suggest(API_KEY, item)
    #print(sec_result)
