def create_debug_print_handler():
    prev_line = ""

    def handle(line):
        nonlocal prev_line
        if line != prev_line:
            print(line)
            prev_line = line

    return handle

def zfill(number: int, length: int):
    string = str(number)
    zeroes_to_add = max(0, (length - len(string)))
    return "0" * zeroes_to_add + string