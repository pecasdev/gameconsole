@echo off
@REM run me from the root of gameconsole

mpremote mkdir sd > nul

mpremote ^
mip install sdcard + ^
mip install ssd1306 + ^
cp -r library : + ^
cp hardware/copy_injection_from_sd.py : + ^
cp hardware/engine_driver.py : + ^
cp hardware/hardware_button_driver.py : + ^
cp hardware/hardware_frame_buffer_adaptor.py : + ^
cp hardware/inject_select_menu.py : + ^
cp hardware/main2.py :main2.py + ^
cp hardware/mount_sd.py : + ^
cp hardware/oled_screen_adaptor.py :