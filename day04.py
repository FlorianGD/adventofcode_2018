"""Solutions for day 4 of AoC 2018"""

import operator
import re
from collections import defaultdict, Counter

import numpy as np
from dateutil import parser

# Part 1

with open('day04_input.txt') as f:
    shifts = f.readlines()

# First, I need to sort the dates and times
shifts.sort(key=lambda x: parser.parse(x[1:17]))


def timeshifts(shifts):
    """
    From a list of timeshifts, return a dictionnary with an entry per guard.
    Each entry is a dict with an entry per day that stores the times recorded,
    so the first one is the minute the guard falls asleep, the next, the moment
    he wakes up and so on.
    """
    guard_dict = defaultdict(lambda: defaultdict(list))
    for line in shifts:
        # The first line contains the id, and we carry it forward
        if '#' in line:
            guard_id = int(re.search(r'#(\d+) ', line).group(1))
            # This is the only info we want when there is an id
            continue
        date = parser.parse(line[1:17])
        day = date.date()
        minute = date.minute
        guard_dict[guard_id][day].append(minute)
    return guard_dict


def total_time_asleep(guard_dict):
    """
    Computes the total time the guard were asleep
    """
    guard_total = defaultdict(int)
    for id, day_dict in guard_dict.items():
        for day, minutes in day_dict.items():
            wakes_ups = np.array(minutes[1::2])
            falls_asleeps = np.array(minutes[::2])
            guard_total[id] += np.sum(wakes_ups - falls_asleeps)
    return guard_total


def max_total(total_dict):
    """
    Returns the id of the guard with the max total time asleep
    """
    return max(total_dict.items(), key=operator.itemgetter(1))[0]


def max_minute(guard_dict, id_max):
    """
    Returns the minutes where the guard id_max is asleep the more often
    """
    minutes_counter = Counter()
    for day, minutes in guard_dict[id_max].items():
        # I list all the minutes were the guard is asleep and concatenate
        # all spans for each day
        all_minutes = np.concatenate(
            [np.arange(a, b) for a, b in zip(minutes[::2], minutes[1::2])]
        )
        minutes_counter.update(all_minutes)
    return max_total(minutes_counter)


def part_one(shifts):
    """
    Returns the id of the guard that is asleep the most times the minutes he is
    asleep the most
    """
    guard_dict = timeshifts(shifts)
    total_dict = total_time_asleep(guard_dict)
    max_id = max_total(total_dict)
    max_min = max_minute(guard_dict, max_id)
    return max_id * max_min


test_shifts = '''[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up'''.splitlines()

assert part_one(test_shifts) == 240

print(f'Solution for part 1: {part_one(shifts)}')
