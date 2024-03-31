import threading
import itertools

# Place this outside the functions so all threads share the same copy
seen_sequences = set()

def possible_sums(n, seq):
    for r in range(1, len(seq)+1):
        for subset in itertools.combinations(seq, r):
            if sum(subset) == n:
                yield subset

def simulate_game(numbers, roll_history, start_roll, file_lock):
    global seen_sequences

    if start_roll is not None:
        roll_history.append(start_roll)
        for subset in possible_sums(start_roll, numbers):
            numbers = [n for n in numbers if n not in subset]
            break
    else:
        start_roll = roll_history[0]

    # Game is won
    if not numbers:
        sequence = tuple(roll_history)
        # Only write and count sequence if it hasn't been visited before
        if sequence not in seen_sequences:
            with file_lock:
                with open(f"all{start_roll}games.txt", "a") as file:
                    file.write(f"{sequence} T\n")
            seen_sequences.add(sequence)
            return 1
        return 0

    total_count = 0
    for dice1 in range(1, 7):
        for dice2 in range(1, 7):
            total_roll = dice1 + dice2
            subsets = list(possible_sums(total_roll, numbers))

            if subsets:
                for subset in subsets:
                    total_count += simulate_game([n for n in numbers if n not in subset], roll_history + [total_roll], None, file_lock)
            else: # Game is lost
                sequence = tuple(roll_history + [total_roll])
                if sequence not in seen_sequences:
                    with file_lock:
                        with open(f"all{start_roll}games.txt", "a") as file:
                            file.write(f"{sequence} F\n")
                    seen_sequences.add(sequence)
                break

    return total_count


def simulate_game_thread(start_roll, file_lock):
    numbers = [n + 1 for n in range(9)]
    roll_history = []
    total_games = simulate_game(numbers, roll_history, start_roll, file_lock)
    print(f"Total number of possible games starting with roll {start_roll}: {total_games}")

def main():
    file_lock = threading.Lock()
    threads = []

    for start_roll in range(2, 13): 
        with open(f"all{start_roll}games.txt", "w") as file:
            file.write("Rolls GameWon\n")
        thread = threading.Thread(target=simulate_game_thread, args=(start_roll, file_lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()