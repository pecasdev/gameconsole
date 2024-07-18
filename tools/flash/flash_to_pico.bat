@REM run me from the root of gameconsole

mpremote ^
mip install sdcard + ^
mip install ssd1306 + ^
cp -r library : + ^
cp hardware/engine_driver.py : + ^
cp hardware/hardware_button_driver.py : + ^
cp hardware/oled_screen_adaptor.py : + ^
cp hardware/main.py :main2.py + ^
cp -r inject :