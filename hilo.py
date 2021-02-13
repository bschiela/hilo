""" What are the odds of winning high-low with different strategies.

1. Static median (8): Take the largest outlier and guess in the direction of the 8s.
2. Dynamic median: Track the median card remaining in the deck as they are revealed.
3. Visible median: Compute the median based on face-up cards on the table.
    3a. Top card only.
    3b. All cards in surviving stacks.

TODO:
- median computation is slow.  just increment/decrement by 0.5.
- write unit tests/asserts for correctness (consider performance of python function
  calls though)
- compute more stats (e.g. mean number of cards remaining, uncertainty in win %) and
  save to .csv
- a "draw" might be an optimal guess near the end-game (how often does this occur?)
"""

import numpy as np


def get_number(card):
    return card // 4


def get_suit(card):
    return card % 4


def simulate(num_games, track_median=False):
    num_wins = 0
    num_losses = 0

    for g in range(num_games):
        print(f'game {g} / {num_games}', end = '\r')
        deck = np.arange(52)
        median = np.median(deck)
        np.random.shuffle(deck)
        table, deck = deck[:9], deck[9:]

        while len(table) > 0 and len(deck) > 0:
            if track_median and len(deck) > 0:
                median = np.median(deck)

            outlier_loc = np.argmax(np.abs(table - median))
            outlier = table[outlier_loc]
            if outlier < median:
                guess = 'high'
            elif outlier > median:
                guess = 'low'
            else:
                guess = 'high' if np.random.randint(2) else 'low'

            draw, deck = deck[0], deck[1:]
            draw_num = get_number(draw)
            outlier_num = get_number(outlier)
            if (guess == 'high' and draw_num > outlier_num) or (guess == 'low' and draw_num < outlier_num):
                # success, swap card in table
                table[outlier_loc] = draw
            else:
                # fail, delete card from table
                table = np.delete(table, outlier_loc)

        if len(table) == 0:
            num_losses += 1
        else:
            num_wins += 1
            assert len(table) > 0
            assert len(deck) == 0

    assert num_losses + num_wins == num_games
    print(f'win %: {num_wins / num_games * 100}')


if __name__ == '__main__':
    trials = 100000
    for _ in range(3):
        print('===== static median =====')
        simulate(trials)
    for _ in range(3):
        print('===== dynamic median =====')
        simulate(trials, track_median=True)
