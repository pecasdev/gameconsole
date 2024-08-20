if __name__ == "__main__":
    # idk if this is illegal but i can't get imports to work properly. i'm so tired.
    import os
    import sys

    gameconsole_dir = os.path.dirname(__file__)

    sys.path.insert(0, os.path.join(gameconsole_dir, "library"))
    sys.path.insert(0, os.path.join(gameconsole_dir, "tools"))

    if sys.argv[1] == "emulate":
        from inject import main
        from emulate import create_emulator

        create_emulator(main).runloop()

    if sys.argv[1] == "sprite_convert":
        from tools.sprite_convert import sprite_convert

        sprite_convert()
    
    if sys.argv[1] == "flash_hardware":
        import subprocess
        subprocess.run(".\\tools\\flash\\flash_to_pico.bat")

    if sys.argv[1] == "font_convert":
        from tools.font_convert import font_convert

        font_convert()
