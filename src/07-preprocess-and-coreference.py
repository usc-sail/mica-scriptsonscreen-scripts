"""Find coreference clusters of character mentions"""
from coreference.movie_coref.preprocess import preprocess_scripts
from coreference.movie_coref.movie_coref import MovieCoreference

import os
import json
import math
from absl import app
from absl import flags

TOTAL_BATCHES = 4
SUBDOC_LEN = 10240
OVERLAP_LEN = 2048
WEIGHTS_FILE = "coreference/data/Mar09_01:31:43PM_24839/movie_coref.pt"

FLAGS = flags.FLAGS
flags.DEFINE_bool("coref", default=False, help="set to find coreference clusters, otherwise preprocess")
flags.DEFINE_string("scripts_dir", default=None, help="scripts directory", required=True)
flags.DEFINE_string("imdb_id", default=None, help="test imdb id to run coreference resolution", required=False)
flags.DEFINE_integer("batch", default=0, help="batch of scripts to resolve")
flags.DEFINE_integer("gpu_id", default=0, help="gpu to use")

def preprocess_and_find_coreference(_):
    scripts_dir = FLAGS.scripts_dir
    batch = FLAGS.batch
    gpu_id = FLAGS.gpu_id
    test_imdb_id = FLAGS.imdb_id
    coref = FLAGS.coref

    if coref:
        imdb_ids, movie_data = [], []
        if test_imdb_id is None:
            for imdb_id in sorted(os.listdir(scripts_dir)):
                coref_file = os.path.join(scripts_dir, imdb_id, "coref.json")
                clusters_file = os.path.join(scripts_dir, imdb_id, "clusters.json")
                if os.path.exists(coref_file) and not os.path.exists(clusters_file):
                    with open(coref_file) as fr:
                        mdata = json.load(fr)
                    imdb_ids.append(imdb_id)
                    movie_data.append(mdata)
        else:
            coref_file = os.path.join(scripts_dir, test_imdb_id, "coref.json")
            clusters_file = os.path.join(scripts_dir, test_imdb_id, "clusters.json")
            if os.path.exists(coref_file) and not os.path.exists(clusters_file):
                with open(coref_file) as fr:
                    mdata = json.load(fr)
                imdb_ids.append(test_imdb_id)
                movie_data.append(mdata)

        batch_size = int(math.ceil((len(imdb_ids)/TOTAL_BATCHES)))
        start = batch * batch_size
        end = min(start + batch_size, len(imdb_ids))
        imdb_ids, movie_data = imdb_ids[start: end], movie_data[start: end]

        model = MovieCoreference(preprocessed_data=movie_data, weights_file=WEIGHTS_FILE, hierarchical=False,
                                document_len=SUBDOC_LEN, overlap_len=OVERLAP_LEN)
        for imdb_id, mdata in zip(imdb_ids, model.predict()):
            clusters_file = os.path.join(scripts_dir, imdb_id, "clusters.json")
            with open(clusters_file, "w") as fw:
                json.dump(mdata, fw, indent=2, sort_keys=True)

    else:
        imdb_ids, script_files, parse_files = [], [], []
        for imdb_id in os.listdir(scripts_dir):
            script_file = os.path.join(scripts_dir, imdb_id, "script.txt")
            parse_file = os.path.join(scripts_dir, imdb_id, "trfr-parse.txt")
            if os.path.exists(script_file) and os.path.exists(parse_file):
                script_lines = open(script_file).read().strip().split("\n")
                n_unique_script_lines = len(set([line.strip() for line in script_lines if line.strip()]))
                if n_unique_script_lines >= 100:
                    imdb_ids.append(imdb_id)
                    script_files.append(script_file)
                    parse_files.append(parse_file)
        print(f"{len(imdb_ids)} scripts")

        movie_data = preprocess_scripts(script_files, parse_files, gpu_device=gpu_id)
        for imdb_id, mdata in zip(imdb_ids, movie_data):
            coref_file = os.path.join(scripts_dir, imdb_id, "coref.json")
            with open(coref_file, "w") as fw:
                json.dump(mdata, fw, indent=2, sort_keys=True)

if __name__=="__main__":
    app.run(preprocess_and_find_coreference)