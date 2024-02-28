# Movie Scripts Dataset

scriptsonscreen in a dataset of movie scripts downloaded from the https://scripts-onscreen.com/ website.

This repository contains the data and source code used to scrape and preprocess the scripts from the scriptsonscreen
website.
You can find the movie scripts in the [scripts](scripts/) directory.

The scripts directory contains subdirectories named after the IMDB id of the movie.
Each such subdirectory contains the movie script and related processed files of the movie corresponding to the IMDB id.

The contents of a movie subdirectory are:

1. **script.txt** contains the raw movie script.

2. **parse-rule.txt** and **parse-trfr.txt** contains the parsed output of the movie script.
The parsed output is a single structural label for each script line.
The labels could be *S* (slugline), *N* (description), *C* (character), *D* (utterance), *E* (utterance expression), 
*T* (transition), *M* (metadata), or *O* (other, usually blank lines).
The **parse-rule.txt** has been created by a rule-based parser.
The **parse-trfr.txt** has been created by a transformer-based parser.
We recommend you use **parse-trfr.txt** file because it is more accurate.
We provide **parse-rule.txt** file for sake of comparison.

3. **imdb.json** contains some basic metadata about the movie.
This information has been obtained from the IMDB website.
It contains the cast list, character names, title, genres, year of production, earnings, etc.

4. **clusters.json** contains the coreference clusters of the characters of the movie.

We use the [Movie Screenplay Parser](https://github.com/usc-sail/mica-screenplay-parser) to parse the scripts, and the
[Character Coreference Resolution](https://github.com/usc-sail/mica-character-coref) models to find the coreference
clusters.