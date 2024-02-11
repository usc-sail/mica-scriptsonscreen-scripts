scriptsonscreen in a dataset of movie scripts downloaded from the https://scripts-onscreen.com/ website.

The **cache** directory contains webpages downloaded from the scripts-onscreen website.
They are cached here to reduce finish times for future updates.

The **downloads** directory contains the text and pdf files of movie scripts scrapped from the webpages (and linked webpages of other websites hosting movie
scripts) of scripts-onscreen website.
The directory contains an index file which maps filenames to urls, IMDB ids, and MOVIEDB ids. Each entry also contains the date when the file was downloaded.
The directory contains a imdb\_id\_to\_movie.json file which contains IMDB data, such as title, cast, and genre information, about the movie scripts.

The **scripts** directory arranges the movie script files of **downloads** directory in folders named after their IMDB ids.
It is a more accessible version of the contents of **downloads**.
Each movie script directory in the **scripts** directory also contains the structural tags of the movie script and a json file containing the IMDB data.
