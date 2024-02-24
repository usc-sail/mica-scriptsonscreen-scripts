"""Parse the scripts using both rule-based and transformer-based parser"""
import os
import tqdm
from parser.screenplayparser import ScreenplayParser

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("scripts_dir", default=None, help="scripts directory", required=True)
flags.DEFINE_integer("gpu", default=0, help="GPU id")

def parse_scripts(_):
    scripts_dir = FLAGS.scripts_dir
    gpu_id = FLAGS.gpu

    rule_parser = ScreenplayParser(use_rules=True)
    trfr_parser = ScreenplayParser(use_rules=False, device_id=gpu_id)

    for imdb_id in tqdm.tqdm(os.listdir(scripts_dir), unit="script"):
        script_file = os.path.join(scripts_dir, imdb_id, "script.txt")
        with open(script_file) as fr:
            script = fr.read().strip().split("\n")
        rule_tags = rule_parser.parse(script)
        trfr_tags = trfr_parser.parse(script)
        rule_tags_file = os.path.join(scripts_dir, imdb_id, "rule-parse.txt")
        trfr_tags_file = os.path.join(scripts_dir, imdb_id, "trfr-parse.txt")
        with open(rule_tags_file, "w") as fw:
            fw.write("\n".join(rule_tags))
        with open(trfr_tags_file, "w") as fw:
            fw.write("\n".join(trfr_tags))

if __name__ == '__main__':
    app.run(parse_scripts)