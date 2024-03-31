def total_games(start_roll):
    games = {
        11: 1312,
        12: 3656,
        10: 5461,
        2: 7196,
        4: 13242,
        6: 17665,
        8: 19758,
        3: 19840,
        7: 23258,
        5: 23877,
        9: 25899
    }
    return games.get(start_roll, 0)

def search_games(rolls):
    roll_pattern = '(' + ', '.join(str(roll) for roll in rolls) + ','
    wins = 0
    losses = 0
    with open(f"all{rolls[0]}games.txt", "r") as file:
        for line in file:
            if line.startswith(roll_pattern):
                outcome = line.strip().split(' ')[-1]
                if outcome == 'T':
                    wins += 1
                else:
                    losses += 1
    return wins, losses

def live_odds():
    rolls = []
    while True:
        roll = input("Enter a roll (or 'q' to quit): ")
        if roll.lower() == 'q':
            break
        rolls.append(int(roll))
        if len(rolls) == 1:
            total = total_games(rolls[0])
            print(f"Total number of possible games starting with roll {rolls[0]}: {total}")
            continue
        wins, losses = search_games(rolls)
        total = wins + losses
        if total == 0:
            print("No games found.")
            continue
        win_rate = wins / total * 100
        print(f"Win rate for {rolls}: {win_rate:.2f}%")

if __name__ == "__main__":
    live_odds()