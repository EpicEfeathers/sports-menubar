import requests
import pprint
from datetime import date
import json

def recent_game_id(team_id:int):
    today = date.today().isoformat()
    current_link = f"https://statsapi.mlb.com/api/v1/schedule?teamId={team_id}&date={today}&sportId=1"
    current_link = "https://statsapi.mlb.com/api/v1/schedule?teamId=118&date=2025-06-05&sportId=1"
    content = requests.get(current_link).json()

    # if there is a game today
    if content['totalGames'] > 0:
        game_id = content['dates'][-1]['games'][-1]['gamePk'] # get most recent game, if applicable (say doubleheader)
        return game_id
    
    # else, look at past schedule
    link = f"https://statsapi.mlb.com/api/v1/teams/{team_id}?hydrate=previousSchedule&fields=teams,previousGameSchedule,dates,games,gamePk"
    content = requests.get(link).json()
    try:
        dates = content.get('teams', [])[0].get('previousGameSchedule', {}).get('dates', [])
        if dates:
            game = dates[-1].get('games', [])
            if game: # if there are any games
                game_id = game[0].get('gamePk', [])
    except Exception as e:
        game_id = None
        print(f"Error when fetching recent game: {e}")

    return game_id

def extract_game_info(game_id:int):
    '''link = f"https://statsapi.mlb.com/api/v1.1/game/{game_id}/feed/live"
    content = requests.get(link).json()'''

    with open("example_data.json") as f:
        content = json.load(f)

    live_data = content['liveData']

    current_play = live_data['plays']['currentPlay']
    outs = current_play["count"]["outs"]

    offense = live_data['linescore']['offense']
    bases = [ # check to see if they are in offense (base runners)
        'first' in offense,
        'second' in offense,
        'third' in offense
    ]

    home_score = live_data['linescore']['teams']['home']['runs']

    away_score = live_data['linescore']['teams']['away']['runs']

    return bases, outs, home_score, away_score
    
    


print(extract_game_info(777531))