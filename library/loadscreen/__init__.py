from engine import Engine


def draw_loadscreen(title: str):
    Engine.screen.clear()
    Engine.screen.draw_text(10, 10, f"NOW LOADING {title}")
    Engine.screen.draw_text(10, 20, f"THIS MIGHT TAKE 10 SECONDS")
    Engine.screen.flush()
