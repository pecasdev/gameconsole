from inject import main
from emulate import create_emulator
from font import Font

if __name__ == "__main__":
    Font.import_font("library/font/default_fonts/small.font")
    create_emulator(main).runloop()