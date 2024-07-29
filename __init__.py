if __name__ == "__main__":
    # idk if this is illegal but i can't get imports to work properly, i'm so tired
    import os
    import sys

    gameconsole_dir = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(gameconsole_dir, "library"))

    from inject import main
    from emulate import create_emulator

    create_emulator(main).runloop()
