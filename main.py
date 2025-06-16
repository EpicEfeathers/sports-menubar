import rumps
import os

import api_utils

def return_info_image_path(bases:list, outs:int):
    return f"bases/bases{int(bases[0])}{int(bases[1])}{int(bases[2])}_outs{outs}.png"


class MenuBarSports(rumps.App):
    def __init__(self):
        super().__init__("MenuBarSports") # default message (should never show)

        self.team_id = 119

    @rumps.timer(10)
    def updating_info(self, _):
        self.game_id = api_utils.recent_game_id(self.team_id)
        print(self.game_id)

        # all data
        home_abbreviation, away_abbreviation, bases, outs, home_score, away_score, inning, is_top = api_utils.extract_game_info(self.game_id)

        im_path = return_info_image_path(bases, outs)
        self.update_title(im_path, home_abbreviation, away_abbreviation, home_score, away_score, inning, is_top)

    # properly create title
    def update_title(self, im_path, home_abbreviation, away_abbreviation, home_score, away_score, inning, is_top):
        # make sure path exists
        if os.path.exists(im_path):
            self.icon = im_path
        else:
            # if three outs
            self.icon = "bases/bases000_outs0.png"

            is_top = not is_top
            if is_top:
                inning += 1
        
        self.title = f"{'↑' if is_top else '↓'}{inning}  {away_abbreviation} {away_score} | {home_score} {home_abbreviation}"

if __name__ == "__main__":
    MenuBarSports().run()