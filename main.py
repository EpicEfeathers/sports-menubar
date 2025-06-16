import rumps
import os
import json

import api_utils
import utils

def return_info_image_path(bases:list, outs:int):
    return f"bases/bases{int(bases[0])}{int(bases[1])}{int(bases[2])}_outs{outs}.png"


class MenuBarSports(rumps.App):
    def __init__(self):
        super().__init__("MenuBarSports") # default message (should never show)

        self.settings = utils.load_settings()
        self.team_id = self.settings.get('selected_team', 108)

        with open("teams.json") as f:
            teams = json.load(f)

        teams.sort(key=lambda team: team['team_name']) # sort by team name, not by location

        self.team_lookup = {team['name']: team['id'] for team in teams}

        self.options_menu = rumps.MenuItem("Selected Team")

        self.options_list = [team['name'] for team in teams]
        for i, title in enumerate(self.options_list):
            item = rumps.MenuItem(title, callback=self.select_option)

            # select first item
            if self.team_lookup.get(title) == self.team_id:
                item.state = True
            self.options_menu.add(item)

        self.menu = [self.options_menu]

    def select_option(self, sender):
        for title, item in self.options_menu.items():
            item.state = False
        sender.state = True

        selected_team = sender.title
        self.team_id = self.team_lookup.get(selected_team, 141)

        # update user settings
        self.settings['selected_team'] = self.team_id
        utils.save_settings(self.settings)

        # update the menu bar
        self.update_team_info()


    @rumps.timer(10)
    def updating_info(self, _):
        self.update_team_info()

    def update_team_info(self):
        self.game_id = api_utils.recent_game_id(self.team_id)

        # all data
        info = api_utils.extract_game_info(self.game_id)

        if info:
            # if bases (and outs) info has been returned
            if 'bases' in info:
                im_path = return_info_image_path(info['bases'], info['outs'])
            else:
                im_path = None

            self.update_title(info, im_path)
        else:
            print("Error in fetching data")

    # properly create title
    def update_title(self, info, im_path):
        # if game is live
        if info['game_state'] == "Live":
            # make sure path exists
            if os.path.exists(im_path):
                self.icon = im_path
            else:
                # if three outs
                self.icon = "bases/bases000_outs0.png"

                info['is_top'] = not info['is_top']
                if info['is_top']:
                    info['inning'] += 1
            
            self.title = f"{'↑' if info['is_top'] else '↓'}{info['inning']}  {info['away_abbr']} {info['away_score']} | {info['home_score']} {info['home_abbr']}"
        else:
            if info['game_state'] == "Final":
                game_info = info['game_state']
            else:
                game_info = f"{info['time']}{info['ampm']}"
            self.title = f"{game_info} • {info['away_abbr']} {info['away_score']} | {info['home_score']} {info['home_abbr']}"

if __name__ == "__main__":
    MenuBarSports().run()