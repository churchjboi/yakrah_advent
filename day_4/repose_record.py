__author__ = "yakrah"

from argparse import ArgumentParser
from collections import namedtuple, defaultdict
from datetime import datetime, timedelta


class GuardActions:
    STARTS_SHIFT = 1
    WAKES_UP = 2
    FALLS_ASLEEP = 3

class GuardStates:
    AWAKE = 0
    ASLEEP = 0


GuardEvent = namedtuple('GuardEvent', ['guard_id', 'action'])


def parse_args():
    argument_parser = ArgumentParser()

    argument_parser.add_argument('--input-file', default='puzzle_input.txt')

    return argument_parser.parse_args()


def parse_event_from_record(record_str):
    if 'Guard' in record_str:
        guard_id = record_str.split(' ')[2].strip('#').strip()
        action = GuardActions.STARTS_SHIFT
    else:
        guard_id = None
        action = GuardActions.WAKES_UP if record_str.strip() == 'wakes up' else GuardActions.FALLS_ASLEEP

    return GuardEvent(guard_id, action)


def add_minutes_to_map(guard_sleep_map, guard_id, fell_asleep, woke_up):
    working_time = fell_asleep
    while working_time < woke_up:
        if guard_id in guard_sleep_map:
            guard_sleep_map[int(guard_id)][working_time.minute] += 1
        else:
            guard_sleep_map[int(guard_id)] = defaultdict(lambda: 0)
        working_time = working_time + timedelta(minutes=1)


def repose_record(guard_record_file):
    guard_events = {}

    guard_sleep_map = {}

    with open(guard_record_file, 'r') as guard_records:
        for guard_record in guard_records:
            event_time_str = guard_record[guard_record.find('[')+1:guard_record.find(']')].strip()
            action_str = guard_record[guard_record.find(']')+1:]
            event_time = datetime.strptime(event_time_str, '%Y-%m-%d %H:%M')
            guard_events[event_time] = parse_event_from_record(action_str)

    event_times_sorted = sorted(guard_events.keys())
    guard_on = guard_events[event_times_sorted[0]].guard_id
    fell_asleep = None
    for event_time in event_times_sorted:

        action = guard_events[event_time]

        if action.action == GuardActions.STARTS_SHIFT:
            guard_on = action.guard_id
        elif action.action == GuardActions.FALLS_ASLEEP:
            fell_asleep = event_time
        elif action.action == GuardActions.WAKES_UP:
            add_minutes_to_map(guard_sleep_map, int(guard_on), fell_asleep, event_time)
        else:
            raise Exception("This shouldn't have happened man.... do better")

    max_minutes = 0
    max_guard = None

    for guard, sleep_map in guard_sleep_map.items():
        guard_minutes = 0
        for minute, count in sleep_map.items():
            guard_minutes += count
        if guard_minutes > max_minutes:
            max_minutes = guard_minutes
            max_guard = guard

    # Solve part 1
    inversed_guard_map = {counts: minute for minute, counts, in guard_sleep_map[max_guard].items()}
    best = max(inversed_guard_map.keys())
    print('This guard slept the most: #{}'.format(max_guard))
    print('He slept the most during minute: {}'.format(inversed_guard_map[best]))
    print('P1 solution: {}'.format(int(max_guard) * int(inversed_guard_map[best])))

    # Solve part 2 (use all same maps)

    top_guard = None
    top_sleep_count = 0

    for guard, sleep_map in guard_sleep_map.items():
        if max(sleep_map.values()) > top_sleep_count:
            top_sleep_count = max(sleep_map.values())
            top_guard = guard

    top_guard_sleep_map_inversed = {counts: minutes for minutes, counts in guard_sleep_map[top_guard].items()}

    print('This guard slept the most for any one minute: #{}'.format(top_guard))
    print('He slept for the above minute this many times: {}'.format(top_guard_sleep_map_inversed[top_sleep_count]))
    print('P2 solution: {}'.format(top_guard * top_guard_sleep_map_inversed[top_sleep_count]))


if __name__ == "__main__":
    args = parse_args()
    repose_record(args.input_file)
