from engine import Engine


def draw_loadscreen(title: str):
    Engine.screen.clear()
    Engine.screen.draw_text(5, 10, f"NOW LOADING {title}")
    Engine.screen.draw_text(5, 20, f"THIS CAN TAKE\nUP TO 10 SECONDS")
    Engine.screen.flush()
