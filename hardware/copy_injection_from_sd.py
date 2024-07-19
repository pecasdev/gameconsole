import os


def rmdir(dir):
    for i in os.listdir(dir):
        os.remove("{}/{}".format(dir, i))
    os.rmdir(dir)


def copy_injection_from_sd(injection_name):
    injection_dir = f"/sd/{injection_name}"

    try:
        rmdir("/inject")
    except:
        pass

    os.mkdir("/inject")

    for filename in os.listdir(injection_dir):
        from_file = open(f"{injection_dir}/{filename}")
        to_file = open(f"/inject/{filename}", "w")

        to_file.write(from_file.read())

        from_file.close()
        to_file.close()
