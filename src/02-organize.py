import pandas as pd
import os
import json
import tqdm

from absl import app
from absl import flags

FLAGS = flags.FLAGS
data_dir = os.path.join(os.getenv("DATA_DIR"), "mica-movie-scripts/scriptsonscreen")
flags.DEFINE_string("download", default=os.path.join(data_dir, "download"), 
                    help="directory containing downloaded script text or pdf files")
flags.DEFINE_string("scripts", default=os.path.join(data_dir, "scripts"), 
                    help="directory containing script text files and imdb data arranged by imdb id")

def organize(_):
    downloads_dir = FLAGS.download
    scripts_dir = FLAGS.scripts

    index_file = os.path.join(downloads_dir, "index.csv")
    imdb_file = os.path.join(downloads_dir, "imdb_id_to_movie.json")

    index_df = pd.read_csv(index_file, index_col=None)
    with open(imdb_file) as fr:
        imdb_data = json.load(fr)

    gby = index_df.groupby("imdb_id", dropna=True)
    for imdb_id, imdb_df in tqdm.tqdm(gby, total=gby.ngroups, unit="imdb", desc="organizing"):
        files = imdb_df["file"].dropna().astype(str).unique().tolist()
        max_file, max_content_size = None, 0

        for f in files:
            if os.path.exists(os.path.join(downloads_dir, f + ".txt")):
                with open(os.path.join(downloads_dir, f + ".txt")) as ff:
                    content = ff.read()
                if len(content) > max_content_size:
                    max_content_size = len(content)
                    max_file = f

        if max_file is not None and imdb_id in imdb_data:
            out_dir = os.path.join(scripts_dir, str(imdb_id[2:]))
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(downloads_dir, max_file + ".txt")) as f:
                content = f.read().replace("", "")
            with open(os.path.join(out_dir, "script.txt"), "w") as fw:
                fw.write(content)
            with open(os.path.join(out_dir, "imdb.json"), "w") as fw:
                json.dump(imdb_data[imdb_id], fw)

if __name__ == '__main__':
    app.run(organize)