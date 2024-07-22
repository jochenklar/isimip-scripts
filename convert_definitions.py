import argparse
import json
from pathlib import Path

import yaml

ORDER = [
    'specifier',
    'specifier_file',
    'title',
    'subtitles',
    'dataset',
    'long_name',
    'long_names',
    'standard_name',
    'group',
    'description',
    'description_note',
    'time_period',
    'reanalysis',
    'bias_adjustment_target',
    'priority',
    'status',
    'mandatory',
    'extension',
    'unit',
    'units',
    'frequency',
    'resolution',
    'doi',
    'path',
    'url',
    'variables',
    'comment',
    'pre-industrial',
    'historical',
    'future',
    'simulation_rounds',
    'products',
    'category',
    'subcategory',
    'sectors',
]

FOLDED = [
    'comment',
    'description'
]

# from: https://stackoverflow.com/a/7445560

class folded_str(str):
    pass


def folded_str_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='>')


yaml.add_representer(folded_str, folded_str_representer)


def iterrate(row):
    for key in ORDER:
        if key in row:
            yield key, row[key]

    for key in sorted(row):
        if key not in ['specifier', *ORDER]:
            yield key, row[key]


def fold(key, value):
    return folded_str(value) if key in FOLDED else value


parser = argparse.ArgumentParser()
parser.add_argument('input_file')

args = parser.parse_args()

input_path = Path(args.input_file)
output_path = input_path.with_suffix('.yaml')

definitions = []
for row in json.load(input_path.open()):
    definition = {}

    for key, value in iterrate(row):
        if isinstance(value, list):
            definition[key] = []
            for item in value:
                if isinstance(item, dict):
                    definition[key].append({
                        item_key: fold(item_key, item_value)
                        for item_key, item_value in iterrate(item)
                    })
                else:
                    definition[key].append(item)

        elif isinstance(value, dict):
            definition[key] = {
                item_key: fold(item_key, item_value)
                for item_key, item_value in iterrate(value)
            }
        else:
            definition[key] = fold(key, value)

    definitions.append(definition)

yaml_string = yaml.dump(definitions, sort_keys=False, allow_unicode=True)

lines = []
for line in yaml_string.splitlines():
    if not line.startswith(' ') and lines:
        lines.append('')
    lines.append(line)
lines.append('')

output_path.write_text('\n'.join(lines))
