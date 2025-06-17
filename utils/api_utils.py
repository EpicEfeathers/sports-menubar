import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError

from datetime import date, datetime
import json

def make_api_call(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Timeout:
        print("The request timed out.")
    except ConnectionError:
        print("Could not connect to API.")
    except HTTPError as e:
        print(f"HTTPError occurred: {e}")
    except Exception as e:
        print(f"Exception occurred: {e}")

    return None

def recent_game_id(team_id:int):
    # if there is a game today
    today = date.today().isoformat()
    current_game_url = f"https://statsapi.mlb.com/api/v1/schedule?teamId={team_id}&date={today}&sportId=1"
    content = make_api_call(current_game_url)

    if content.get('totalGames', 0) > 0:
        try:
            game_id = content['dates'][-1]['games'][-1]['gamePk'] # get most recent game, if applicable (say doubleheader)
            return game_id
        except Exception as e:
            print(f"Exception occurred when fetching recent game: {e}")
    
    # else, look at past schedule
    previous_schedule_url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}?hydrate=previousSchedule&fields=teams,previousGameSchedule,dates,games,gamePk"
    content = make_api_call(previous_schedule_url)
    try:
        dates = content.get('teams', [])[0].get('previousGameSchedule', {}).get('dates', [])
        if dates:
            game = dates[-1].get('games', [])
            if game: # if there are any games
                game_id = game[0].get('gamePk')
    except Exception as e:
        game_id = None
        print(f"Error when fetching recent game: {e}")

    return game_id

def extract_game_info(game_id:int):
    game_feed_url = f"https://statsapi.mlb.com/api/v1.1/game/{game_id}/feed/live"
    content = make_api_call(game_feed_url)

    '''with open("example_data/in_between_innings_(bottom_to_top).json") as f:
        content = json.load(f)'''

    try:
        game_data = content['gameData']
        game_state = game_data['status']['abstractGameState']
        detailed_state = game_data['status']['detailedState']

        home_abbr = game_data['teams']['home']['abbreviation']
        away_abbr = game_data['teams']['away']['abbreviation']

        datetime = game_data['datetime']['dateTime'] # datetime in ISO 8601 format
        time = convert_datetime(datetime) # convert to human readable time

        # if previewing today's game
        if game_state == "Preview":
            return {
                "game_state": game_state,
                "detailed_state": detailed_state,
                "time": time,
                "home_abbr": home_abbr,
                "away_abbr": away_abbr,
                "home_score": 0,
                "away_score": 0
            }

        # else, game is live or final (or postponed or smth)
        live_data = content['liveData']

        current_play = live_data['plays']['currentPlay']
        outs = current_play["count"]["outs"]

        linescore = live_data['linescore']

        offense = linescore['offense']
        bases = [ # check to see if they are in offense (base runners)
            'first' in offense,
            'second' in offense,
            'third' in offense
        ]

        home_score = linescore['teams']['home']['runs']

        away_score = linescore['teams']['away']['runs']

        inning = linescore['currentInning']
        is_top = linescore['isTopInning']

        return {
            "game_state": game_state,
            "detailed_state": detailed_state,
            "time": time,
            "home_abbr": home_abbr,
            "away_abbr": away_abbr,
            "bases": bases,
            "outs": outs,
            "home_score": home_score,
            "away_score": away_score,
            "inning": inning,
            "is_top": is_top
        }

        #return game_state, home_abbr, away_abbr, bases, outs, home_score, away_score, inning, is_top

    except Exception as e:
        print(f"Exception occurred while fetching data: {e}")
        return None
    

def convert_datetime(date_time):
    # take ISO 8601 date
    utc_dt = datetime.fromisoformat(date_time)

    # convert it to local timezone
    local_dt = utc_dt.astimezone()

    return local_dt.strftime("%I:%M%p")