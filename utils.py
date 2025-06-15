import requests
import pprint
from datetime import date

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
    link = f"https://statsapi.mlb.com/api/v1.1/game/{game_id}/feed/live"
    content = requests.get(link).json()

    current_play = content['liveData']['plays']['currentPlay']
    outs = current_play["count"]["outs"]

    #pprint.pprint(current_play)
    '''runners = current_play.get('runners', [])
    bases = [False, False, False]

    #pprint.pprint(runners)
    for runner in runners:
        pprint.pprint(runner)'''
    
    pprint.pprint(content["liveData"]["linescore"]['offense'])


#extract_game_info(777531)
print(recent_game_id(141))