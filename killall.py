import subprocess

result = subprocess.run(["ps", "aux"], capture_output=True)

teams = ["soupwars", "my_player_client", "player.player"]

stdout = result.stdout.decode("utf-8")
for line in stdout.splitlines():
    if "python" not in line.lower():
        continue
    if (
        "chronobio." in line
        or ("sample_" in line and "_player" in line)
        or any(team in line for team in teams)
    ):
        print(line)
        pid = line.split()[1]
        subprocess.run(["kill", "-9", pid])
