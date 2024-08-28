import sys
import os
import shutil
import time

# disable this if you don't want to copy over the injection in the "inject" folder
INCLUDE_INJECTION_FROM_INJECT_FOLDER = False

# disable this if you don't want to remove unknown injections
REMOVE_UNUSED_INJECTIONS = True

# set this to None if the drive changes frequently
DEFAULT_SD_DRIVE = "D"


def _specify_drive():
    if DEFAULT_SD_DRIVE is None:
        return input("What drive is the SD card mounted on? ")
    else:
        return DEFAULT_SD_DRIVE


def _assert_drive_is_valid(drive):
    for required_file in ["PES_DRIVE", "GAMELIST"]:
        path = f"{drive}:/{required_file}"

        if not os.path.isfile(path):
            print(f"Could not find {path}, aborting")
            sys.exit()


def _determine_injections_to_flash():
    injections_to_flash = []

    if INCLUDE_INJECTION_FROM_INJECT_FOLDER:
        injections_to_flash.append("dist/inject")

    for injection in os.listdir("dist/published_injections"):
        injections_to_flash.append(injection)

    return injections_to_flash


def _determine_current_injections(drive):
    with open(f"{drive}:/GAMELIST") as f:
        current_injections = f.read().splitlines()
        current_injection_names = [item.split(" ")[0] for item in current_injections]
    return current_injection_names


def _generate_diff_output(current_injections, injections_to_flash):
    update_injections = []
    new_injections = []
    remove_injections = []

    for injection in injections_to_flash:
        if injection in current_injections:
            update_injections.append(injection)
        else:
            new_injections.append(injection)

    for injection in current_injections:
        if injection not in injections_to_flash:
            remove_injections.append(injection)

    def format_lines(lines):
        if len(lines) == 0:
            return "N/A"
        else:
            return "\n".join(lines)

    output = format_lines(
        [
            "== NEW INJECTIONS ==",
            format_lines(new_injections),
            "== UPDATE INJECTIONS ==",
            format_lines(update_injections),
            "== REMOVE INJECTIONS ==",
            format_lines(remove_injections),
        ]
    )

    return output


def _confirm_user_intent():
    confirm = input("Confirm flash? ('Y' to continue) ")
    if confirm.lower() == "y":
        return
    else:
        print("'Y' not received, aborting")
        sys.exit()


# idk why shutil copies over empty folders, very annoying
def _walk_delete_empty_folders(dir):
    dirs = [x[0] for x in os.walk(dir, topdown=False)]
    for dir in dirs:
        try:
            os.rmdir(dir)  # will fail if directory is not empty
        except Exception:
            pass


def _move_files_to_sd(filepath, drive):
    destination = f"{drive}:/{filepath}"

    # delete if exists
    if os.path.isdir(destination):
        shutil.rmtree(destination)

    # hardcoded :(
    if filepath != "dist/inject":
        filepath = f"dist/published_injections/{filepath}"

    files_copied = 0

    def copy_and_count(src, dst):
        nonlocal files_copied
        shutil.copy2(src, dst)
        files_copied += 1

    for attempt in range(1, 6):
        try:
            shutil.copytree(
                filepath,
                destination,
                ignore=shutil.ignore_patterns("*.pyc"),
                copy_function=copy_and_count,
            )
            _walk_delete_empty_folders(destination)

            if attempt > 1:
                print(f"success copying {filepath}, continuing")

            return files_copied
        except:
            print(f"Error copying {filepath}, attempt {attempt}, retrying")
            time.sleep(0.5)
            pass

    print(f"Error copying {filepath}, aborting")
    sys.exit()


def _update_gamelist(drive, injection_to_filecount):
    output = ""
    for injection, filecount in injection_to_filecount.items():
        output += f"{injection} {filecount}\n"

    with open(f"{drive}:/GAMELIST", "w") as f:
        f.write(output)


def flash_to_sd():
    print(os.getcwd())
    drive = _specify_drive()
    _assert_drive_is_valid(drive)

    injections_to_flash = _determine_injections_to_flash()
    current_injections = _determine_current_injections(drive)

    diff_output = _generate_diff_output(current_injections, injections_to_flash)
    print(diff_output)

    _confirm_user_intent()

    injection_to_filecount = {}
    for injection in injections_to_flash:
        files_copied = _move_files_to_sd(injection, drive)
        injection_to_filecount[injection] = files_copied

    _update_gamelist(drive, injection_to_filecount)
    print("FLASH COMPLETE")
