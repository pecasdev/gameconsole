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

    def __current_sprite(self):
        return self.sprites[self.current_sprite_name]

    def set_current_sprite_name_from_state(self, state):
        self.current_sprite_name = self.state_to_sprite_name[state]

    def draw_sprite(self):
        self.__current_sprite().blit(0, 0)

        if self.current_sprite_name == "sleep":
            Engine.screen.draw_text(5, 5, "press A to play")

        if self.current_sprite_name == "thumb_up":
            Engine.screen.draw_text(5, 5, "press A to\nplay again")

        if self.current_sprite_name == "wait":
            Engine.screen.draw_text(5, 5, "WAIT")

        if self.current_sprite_name == "go":
            Engine.screen.draw_text(5, 5, "PRESS A!!!")
