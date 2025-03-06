from contextlib import suppress

import psutil

teams = ["soupwars", "my_player_client", "player.player"]

for process in psutil.process_iter():
    with suppress(psutil.ZombieProcess, psutil.NoSuchProcess, psutil.AccessDenied):
        line = " ".join(process.cmdline()).lower()
        if "python" not in line and "uv run" not in line:
            continue
        if (
            "chronobio." in line
            or ("sample_" in line and "_player" in line)
            or ("player_client" in line)
            or any(team in line for team in teams)
        ) and ("chronobio.killall" not in line):
            print(line)
            process.kill()
