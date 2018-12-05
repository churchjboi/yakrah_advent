from argparse import ArgumentParser
from functools import reduce


class InventoryHasher(object):
    def __init__(self, inv_file):
        self._inv_file = inv_file

    def _get_line_vals(self, line, keys=frozenset([2, 3])):
        og_len = len(line)
        chars = list(set(line))
        key_matches = {k: 0 for k in keys}
        for char in chars:
            reduction = og_len - len(line.replace(char, ''))

            if reduction in key_matches:
                key_matches[reduction] = 1
        return [key_matches[k] for k in keys]

    def get_hash(self, keys=frozenset([2, 3])):
        hash_solution = [0] * len(keys)
        with open(self._inv_file) as inv_file:
            for inv_item in inv_file:
                line_solution = self._get_line_vals(inv_item, keys=keys)
                hash_solution = [sum(x) for x in zip(hash_solution, line_solution)]
        return reduce(lambda x, y: x*y, hash_solution)


    def get_id_hashes(self, str_id):
        hashes = []
        for i in range(0, len(str_id)):
            sub_id_prefix = str_id[0:i]
            sub_id_suffix = str_id[i+1:]
            id_hash = '&'.join([sub_id_prefix, sub_id_suffix])
            hashes.append(id_hash)
        return hashes


    def get_overlap_ids(self):
        id_map = {}
        with open(self._inv_file) as inv_file:
            for inv_item in inv_file:
                for id_hash in self.get_id_hashes(inv_item):
                    if id_hash in id_map:
                        return id_hash.replace('&','')
                    else:
                        id_map[id_hash] = inv_item
        return None



def parse_args():
    argument_parser = ArgumentParser()

    argument_parser.add_argument('--input-file', default='puzzle_input.txt')

    return argument_parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    inv_hasher = InventoryHasher(args.input_file)
    print(inv_hasher.get_hash())
    print(inv_hasher.get_overlap_ids())
