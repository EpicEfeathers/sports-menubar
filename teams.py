# logos https://www.mlbstatic.com/team-logos/{team_id}.svg
import requests
import os
import cairosvg

class TeamManager:
    _teams = None

    @classmethod
    def get_teams(cls):
        if cls._teams is None:
            data = requests.get("https://statsapi.mlb.com/api/v1/teams?sportId=1").json()

            cls._teams = [
                {
                    "id": team["id"],
                    "name": team["name"],
                    "abbreviation": team["abbreviation"],
                    "logo_url": f"https://www.mlbstatic.com/team-logos/{team["id"]}.svg"
                }
                for team in data["teams"]
            ]
        return cls._teams
    
    @classmethod
    def get_logos(cls):
        if cls._teams is None:
            cls.get_teams()
        
        for team in cls._teams:
            logo_url = team["logo_url"]
            logo_path = os.path.join("team_logos", f"{team['id']}.png")

            if not os.path.exists(logo_path):
                try:
                    resp = requests.get(logo_url)
                    resp.raise_for_status() # check if valid

                    file = cairosvg.svg2png(bytestring=resp.content)

                    with open (logo_path, "wb") as f: # wb = write to binary, as svg file
                        f.write(file)
                except Exception as e:
                    print(f"Failed to download logo for team id {team['id']}: {e}")


TeamManager.get_teams()
TeamManager.get_logos()