from engine import Engine


# his name is reaction ralph
class Ralph:
    def __init__(self, sprites):
        [sprite.load() for sprite in sprites.values()]
        self.sprites = sprites

        self.current_sprite_name = "sleep"

        self.state_to_sprite_name = {
            "idle": "thumb_up",
            "go": "go",
            "wait": "wait",
        }

    def _current_sprite_offset(self):
        if self.current_sprite_name == "sleep":
            return [10, 26]
        elif self.current_sprite_name == "wait":
            return [10, 8]
        elif self.current_sprite_name == "go":
            return [5, 24]
        elif self.current_sprite_name == "thumb_up":
            return [10, 28]
        else:
            return [0, 0]

    def _current_sprite(self):
        return self.sprites[self.current_sprite_name]

    def set_current_sprite_name_from_state(self, state):
        self.current_sprite_name = self.state_to_sprite_name[state]

    def draw_sprite(self):
        [sprite_x, sprite_y] = self._current_sprite_offset()
        self._current_sprite().blit(sprite_x, sprite_y)

        if self.current_sprite_name == "sleep":
            Engine.screen.draw_text(5, 5, "press A to play")

        if self.current_sprite_name == "thumb_up":
            Engine.screen.draw_text(5, 5, "press A to\nplay again")

        if self.current_sprite_name == "wait":
            Engine.screen.draw_text(5, 5, "WAIT")

        if self.current_sprite_name == "go":
            Engine.screen.draw_text(5, 5, "PRESS A!!!")
