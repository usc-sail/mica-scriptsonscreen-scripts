"""Create segments from scripts and are saved to a csv file inside movie directory with name 'segments.csv'.
The header of the csv file is segment-id, segment-type, segment-speaker, segment-text
"""
import os
import re
import tqdm
import unidecode
import pandas as pd

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("scripts_dir", default=None, help="scripts directory", required=True)

def create_segments(_):
    # read command-line flags
    scripts_dir = FLAGS.scripts_dir

    # regex patterns
    pattern = r"(S+)|(N+)|((C+)([ED]+))"

    for imdb_id in tqdm.tqdm(os.listdir(scripts_dir), unit="script"):
        # set script, imdb, and parse file names
        script_file = os.path.join(scripts_dir, imdb_id, "script.txt")
        parse_file = os.path.join(scripts_dir, imdb_id, "trfr-parse.txt")

        if os.path.exists(script_file) and os.path.exists(parse_file):
            # data
            # each row will be segment id, type, speaker, and text
            rows = []

            # read script
            with open(script_file) as fr:
                script = fr.read().strip()
            script_lines = script.split("\n")

            # read parse tags
            with open(parse_file) as fr:
                tags = fr.read().strip().split("\n")
            tags = "".join(tags)

            # only keep N, C, D, E, and S tagged lines
            new_tags, new_script_lines = [], []
            for tag, script_line in zip(tags, script_lines):
                if tag in "NCDES":
                    new_tags.append(tag)
                    new_script_lines.append(script_line)
            tags = "".join(new_tags)
            script_lines = new_script_lines

            # populate data rows
            scene_id = 0
            segment_id = 0
            for match in re.finditer(pattern, tags):
                if match.group(1):
                    i, j = match.span(1)
                    scene_id += 1
                    _id = f"scene{scene_id}"
                    text = "\n".join(script_lines[i: j])
                    text = re.sub(r"\s+", " ", text).strip()
                    text = unidecode.unidecode(text)
                    rows.append([_id, "slugline", "", text])
                elif match.group(2):
                    i, j = match.span(2)
                    _id = f"desc{scene_id}.{segment_id}"
                    segment_id += 1
                    text = "\n".join(script_lines[i: j])
                    text = re.sub(r"\s+", " ", text).strip()
                    text = unidecode.unidecode(text)
                    rows.append([_id, "desc", "", text])
                else:
                    i, j = match.span(4)
                    k, l = match.span(5)
                    _id = f"utter{scene_id}.{segment_id}"
                    segment_id += 1
                    character = " ".join(script_lines[i: j])
                    character = re.sub(r"\s+", " ", character).strip()
                    character = unidecode.unidecode(character)
                    utterance = " ".join(script_lines[k: l])
                    utterance = re.sub(r"\s+", " ", utterance).strip()
                    utterance = unidecode.unidecode(utterance)
                    rows.append([_id, "utter", character, utterance])

            # save to file
            output_file = os.path.join(scripts_dir, imdb_id, "segments.csv")
            segments_df = pd.DataFrame(rows, columns=["segment-id", "segment-type", "segment-speaker",
                                                        "segment-text"])
            segments_df.to_csv(output_file, index=False)

if __name__ == '__main__':
    app.run(create_segments)