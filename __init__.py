def remove_types_from_source_code():
    from tools.remove_type_hints.walk_and_remove import walk_and_remove_type_hints
    import os

    walk_and_remove_type_hints("library")
    walk_and_remove_type_hints("hardware")

    walk_and_remove_type_hints("inject")
    for injection in os.listdir("published_injections"):
        walk_and_remove_type_hints(f"published_injections/{injection}")


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

    if sys.argv[1] == "flash_to_pico":
        import subprocess

        remove_types_from_source_code()
        subprocess.run(".\\tools\\flash_to_pico\\flash_to_pico.bat")

    if sys.argv[1] == "flash_to_sd":
        from tools.flash_to_sd import flash_to_sd

        remove_types_from_source_code()
        flash_to_sd()

    if sys.argv[1] == "font_convert":
        from tools.font_convert import font_convert

        font_convert()

    if sys.argv[1] == "remove_type_hints":
        remove_types_from_source_code()
