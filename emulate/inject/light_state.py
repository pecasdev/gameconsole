from engine import now
from random import randrange


class LightState:
    def __init__(self) -> None:
        self.state = "idle"

        self.reaction_stamp_start = None
        self.reaction_stamp_end = None
        self.deadline_go_green = None
        self.reaction_duration = None

    def go_green(self):
        self.state = "green"
        self.reaction_stamp_start = now()

    def go_red(self):
        self.deadline_go_green = now() + randrange(1000, 2500)
        self.state = "red"

    def go_idle(self):
        if (
            self.reaction_stamp_end is not None
            and self.reaction_stamp_start is not None
        ):
            reaction_duration = self.reaction_stamp_end - self.reaction_stamp_start
            self.reaction_duration = int(reaction_duration)

            self.reaction_stamp_start = None
            self.reaction_stamp_end = None
        
        self.state = "idle"

    def handle_deadline(self):
        if (
            self.state == "red"
            and self.deadline_go_green is not None
            and now() > self.deadline_go_green
        ):
            self.go_green()
            self.deadline_go_green = None
    
    def handle_alpha_press(self):
        if self.state == "idle":
            return self.go_red()

        if self.state == "green":
            self.reaction_stamp_end = now()
            return self.go_idle()

        if self.state == "red":
            self.reaction_duration = -1
            return self.go_idle()
        
