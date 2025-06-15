import requests
import pprint
import json

data = requests.get("https://statsapi.mlb.com/api/v1/teams?sportId=1").json()

results = []
for team in data["teams"]:
    results.append({
        "id": team["id"],
        "name": team["name"],
        "abbreviation": team["abbreviation"],
        "logo": f"https://www.mlbstatic.com/team-logos/{team["id"]}.svg"
    })

with open("teams.json", "w") as f:
    json.dump(results, f, indent=4)