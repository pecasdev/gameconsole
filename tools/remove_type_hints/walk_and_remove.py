import os
import shutil
from remove_type_hints import remove_type_hints_from_source_code
from .shutil_include_patterns import include_patterns

EXTENSIONS_TO_NOT_REMOVE_TYPE_HINTS_FROM = [".font", ".sprite"]


def copy_without_type_hints(src: str, dst: str):
    with open(src) as read_file:
        with open(dst, "w") as write_file:
            source_code = read_file.read()

            remove_type_hints = True
            for extension in EXTENSIONS_TO_NOT_REMOVE_TYPE_HINTS_FROM:
                if extension in src:
                    remove_type_hints = False
                    break

            if remove_type_hints:
                to_write = remove_type_hints_from_source_code(source_code)
            else:
                to_write = source_code

            write_file.write(to_write)


def walk_and_remove_type_hints(rootdir: str):
    shutil.rmtree(f"dist/{rootdir}", ignore_errors=True)

    shutil.copytree(
        rootdir,
        f"dist/{rootdir}",
        ignore=include_patterns("*.py", "*.font", "*.sprite"),
        copy_function=copy_without_type_hints,
    )
