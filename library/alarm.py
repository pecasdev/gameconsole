import engine

class Alarm:
    def __init__(self, func, timeout_ms) -> None:
        self.func = func
        self.timeout_ms = timeout_ms
        self.stopped = False
    
    def start(self):
        self.start_stamp = engine.now()
    
    def stop(self):
        self.stopped = True
    
    # return true if handled, false if not yet handled
    def handle(self):
        if self.stopped:
            return True
        
        if engine.now() > self.start_stamp + self.timeout_ms:
            self.func()
            return True
    
        return False