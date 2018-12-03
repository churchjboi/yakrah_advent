__author__ = "yakrah"

from argparse import ArgumentParser

import logging
import operator
import sys

OPERATOR_LOOKUP = { '+': operator.add, '-': operator.sub }


def parse_args():
    argument_parser = ArgumentParser()

    argument_parser.add_argument('--input-file', default='puzzle_input.txt')

    return argument_parser.parse_args()


# Part 1
def calibrate(input_file, original_value=0):
    ret_val = original_value
    with open(input_file, 'r') as input_open:
        for calibration in input_open:
            operator_str = calibration[0]
            op = OPERATOR_LOOKUP.get(operator_str, None)
            if not op:
                logging.warning('{} was not a known operator'.format(operator_str))
                continue
            ret_val = op(ret_val, int(calibration[1:]))
            yield ret_val


# Part 2
def calibrate_like_you_mean_it(input_file, original_value=0):
    # You can do this way smarter...
    calib_set = set()
    starting_value = original_value
    last_val = None
    while True:
        for calib in calibrate(input_file, starting_value):
            if calib in calib_set:
                return calib
            else:
                calib_set.add(calib)
                last_val = calib
        starting_value = last_val


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s", stream=sys.stdout)
    args = parse_args()
    calibrations = [calib for calib in calibrate(args.input_file)]
    logging.info('calibrate with {}'.format(calibrations[-1]))
    logging.info('first duplicate {}'.format(calibrate_like_you_mean_it(args.input_file)))
