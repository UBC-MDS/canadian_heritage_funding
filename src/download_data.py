# author: Joyce Wang
# date: 2021-11-18

"""Downloads a csv file from an url.

Usage: download_data.py --url=<url> --file_path=<file_path>

Options:
--url=<url>                  The url of the data file to download. Must be a csv file.
--file_path=<file_path>      File path (including file name with .csv extension) to store the file
"""

import pandas as pd
from docopt import docopt

opt = docopt(__doc__)

def main(url, file_path):
    data = pd.read_csv(url)
    open(file_path, 'w')
    data.to_csv(file_path)

if __name__ == "__main__":
    main(opt["--url"], opt["--file_path"])
