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

        # all data
        info = api_utils.extract_game_info(self.game_id)

        im_path = return_info_image_path(info['bases'], info['outs'])
        self.update_title(info, im_path)

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
            self.title = f"{info['game_state']} • {info['away_abbr']} {info['away_score']} | {info['home_score']} {info['home_abbr']}"

if __name__ == "__main__":
    MenuBarSports().run()