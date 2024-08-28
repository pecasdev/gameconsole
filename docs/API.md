### Overview
If a function name has a leading underscore (eg. `_draw_character` as opposed to `draw_character`), you probably shouldn't be calling it unless you know what you're doing. 
### Screen
### Engine + Object
### Hardware State
### Sprite
talk about sprites lol
### Font
View usable characters in `library/font/__init__.py`.
View the Sprites associated with each character in `tools/font_convert/input/*`.

You will rarely interact with Fonts directly. Instead call `FontManager.set_current_font(name:str)` with parameter "small", "medium" or "large" to set the current font. Subsequent `Screen.draw_text(...)` calls will use the most recently set font.

If you want to make your own custom fonts, see [tools/font_convert](TOOLS#font-convert). Once you have a  `.font` file, import it by calling `FontManager.import_font(filename:str)`.

### Alarm
