import rumps

import utils

class MenuBarSports(rumps.App):
    def __init__(self):
        super().__init__("MenuBarSports")

        self.team_id = 141
        self.game_id = utils.recent_game_id(self.team_id)
        self.icon = "team_logos/info.png"  # small icon file, e.g. 18x18 px
        #self.title = "↑5  TOR 1 | 0 NYY"  # text next to the icon

    @rumps.timer(10)
    def updating_info(self, _):
        self.game_id = utils.recent_game_id(self.team_id)
        self.title = str(self.game_id)

if __name__ == "__main__":
    MenuBarSports().run()