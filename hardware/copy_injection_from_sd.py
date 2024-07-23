import os


def rmdir(dir):
    for file in os.listdir(dir):
        if is_folder(f"{dir}/{file}"):
            rmdir(f"{dir}/{file}")
        else:
            os.remove(f"{dir}/{file}")
    os.rmdir(dir)


def is_folder(filename):
    if os.stat(filename)[0] & 0x4000:
        return True
    else:
        return False


COPY_RETRY_COUNT = 3


def copy_injection_from_sd(injection_name):
    injection_dir = f"/sd/{injection_name}"

    try:
        rmdir("/inject")
    except:
        pass

    os.mkdir("/inject")

    # idk why this function sometimes doesn't work, faulty pin connection?
    def copy_file(filename):
        from_dir = f"{injection_dir}{filename}"
        to_dir = f"/inject{filename}"
        
        for _ in range(COPY_RETRY_COUNT):
            # confirm file was read properly
            from_file = open(from_dir)
            content = from_file.read()
            if len(content) == 0:
                from_file.close()
                continue
            
            # copy file
            to_file = open(to_dir, "w")
            to_file.write(content)

            from_file.close()
            to_file.close()
            
            # confirm file was copied properly
            copy_was_successful = False
            try:
                to_file = open(to_dir)
                if len(to_file.read()) == len(content):
                    copy_was_successful = True
            
            except:
                pass
            
            finally:
                to_file.close()
            
            if copy_was_successful:
                return
        
        raise RuntimeError(f"Could not copy {from_dir} to {to_dir}")
            

    # should have slash at start, otherwise empty string
    def walk_and_copy(subdir):
        for filename in os.listdir(f"{injection_dir}{subdir}"):
            if is_folder(f"{injection_dir}{subdir}/{filename}"):
                os.mkdir(f"/inject{subdir}/{filename}")
                walk_and_copy(f"{subdir}/{filename}")

            else:
                copy_file(f"{subdir}/{filename}")

    print(f"COPYING INJECTION '{injection_name}' FROM SD")
    walk_and_copy("")
    print("DONE COPYING")
