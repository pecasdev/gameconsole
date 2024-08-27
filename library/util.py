# returns a "print function" that doesn't print the same line twice in a row
# useful when printing something repeated like the player's position
def create_debug_print_handler():
    prev_line = ""

    def handle(line):
        nonlocal prev_line
        if line != prev_line:
            print(line)
            prev_line = line

    return handle

# works the same way Python's `"".zfill` works
def zfill(number: int, length: int) -> str:
    string = str(number)
    zeroes_to_add = max(0, (length - len(string)))
    return "0" * zeroes_to_add + string