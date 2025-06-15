import requests
from datetime import date

team_id = 147  # Toronto Blue Jays, for example
today = date.today().isoformat()
print(today)

url = (
    f"https://statsapi.mlb.com/api/v1/schedule"
    f"?teamId={team_id}&date={today}&sportId=1&hydrate=game(content)"
)

data = requests.get(url).json()

# Loop through the schedule to find the live game
gamePk = None
for date_info in data.get("dates", []):
    for game in date_info.get("games", []):
        if game["status"]["abstractGameState"] in ["Live", "In Progress"]:
            gamePk = game["gamePk"]
            break

print("Current gamePk:", gamePk)
