from engine import Engine
from font.font_manager import FontManager

def draw_sd_copy_progress_bar(files_copied: int, total_file_count: int):
    Engine.screen.clear()
    
    progress = int(100 * files_copied/total_file_count)
    
    FontManager.set_current_font("medium")
    Engine.screen.draw_text(5, 20, "COPYING FROM SD")
    Engine.screen.draw_text(5, 40, f"PROGRESS: {progress}%")
    FontManager.set_current_font("small")
    
    Engine.screen.flush()