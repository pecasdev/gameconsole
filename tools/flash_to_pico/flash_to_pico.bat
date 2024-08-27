@echo off
@REM run me from the root of gameconsole

@REM create empty sd folder for mounting
mpremote mkdir sd > nul

@REM install packages
mpremote ^
mip install sdcard + ^
mip install ssd1306

@REM any code that's meant for the pico should be in dist
cd dist

@REM flash api library
mpremote cp -r library :

@REM flash hardware library
cd hardware
mpremote cp -r hardware_library :

@REM flash main2.py (TODO - rename to main.py later)
mpremote cp main2.py :main2.py