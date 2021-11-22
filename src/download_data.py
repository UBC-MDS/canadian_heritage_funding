# authors: Joyce Wang, Amelia Tang, Wenxin Xiang, Artan Zandian
# date: 2021-11-18

"""Downloads a csv file from an url.

Usage: download_data.py --url=<url> --file_path=<file_path>

Options:
--url=<url>                  The url of the data file to download.
--file_path=<file_path>      File path (including file name with extension) to store the file
"""

import os
import requests
from docopt import docopt

opt = docopt(__doc__)


def main(url, file_path):
    data = requests.get(url)
    try:
        open(file_path, "wb").write(data.content)
    except:
        os.makedirs(os.path.dirname(file_path))
        open(file_path, "wb").write(data.content)


if __name__ == "__main__":
    main(opt["--url"], opt["--file_path"])
