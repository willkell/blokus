import concurrent.futures
import re
import subprocess
import time

startTime = time.time()


def average(lst):
    return sum(lst) / len(lst)


def runGame():
    return subprocess.run(
        ["python", "main.py"], capture_output=True, text=True
    ).stdout.split("\n")


numGames = 0
scores = {1: [], 2: [], 3: [], 4: []}
wins = {1: 0, 2: 0, 3: 0, 4: 0}
times = []
res = []
with concurrent.futures.ProcessPoolExecutor() as executor:
    results = [executor.submit(runGame) for _ in range(2000)]

    for f in concurrent.futures.as_completed(results):
        numGames += 1
        print(f"Game {numGames} done")
        res.append(f.result())


for game in res:

    for row in game:
        if re.search("^Player [0-9]: [0-9]+$", row):
            scores[int(row[7])].append(int(row[10:]))
        elif re.search("^---", row):
            gameTime = float(row[4:-12])
            times.append(gameTime)
        elif re.search("^Player [0-9] wins", row):
            wins[int(row[7])] += 1
print("Number of games:", numGames)
print("Average Scores:")
for i in range(1, 5):
    print("Player {} Average Score: {}".format(i, average(scores[i])))
    print("Player {} Wins: {}".format(i, wins[i]))
print("Average Time: {}".format(average(times)))
print("Total Time: {}".format(time.time() - startTime))
