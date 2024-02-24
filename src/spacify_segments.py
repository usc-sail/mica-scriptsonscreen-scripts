"""Process segments through spacy and save the doc"""
import os
import tqdm
import pandas as pd
import spacy
from spacy.tokens import DocBin

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string("scripts_dir", default=None, help="scripts directory", required=True)

def spacify_segments(_):
    scripts_dir = FLAGS.scripts_dir
    nlp = spacy.load("en_core_web_lg")

    for imdb_id in tqdm.tqdm(os.listdir(scripts_dir), unit="script"):
        segments_file = os.path.join(scripts_dir, imdb_id, "segments.csv")
        segments_df = pd.read_csv(segments_file, index_col=None)
        doc_file = os.path.join(scripts_dir, imdb_id, "spacy-segments.bytes")
        docbin = DocBin()
        for doc in tqdm.tqdm(nlp.pipe(segments_df["segment-text"], batch_size=1024), unit="segment",
                             total=len(segments_df)):
            docbin.add(doc)
        with open(doc_file, "wb") as fw:
            fw.write(docbin.to_bytes())

if __name__ == '__main__':
    app.run(spacify_segments)