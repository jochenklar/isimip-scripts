import argparse
import json
from pathlib import Path

import yaml

parser = argparse.ArgumentParser()
parser.add_argument('input_file')

args = parser.parse_args()

input_path = Path(args.input_file)
output_path = input_path.with_suffix('.yaml')

definitions = []
schema = json.load(input_path.open())
yaml_string = yaml.dump(schema, sort_keys=False, allow_unicode=True)

output_path.write_text(yaml_string)
