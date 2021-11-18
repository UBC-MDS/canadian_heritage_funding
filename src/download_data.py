# author: Joyce Wang
# date: 2021-11-18

'''
This script downloads a data file

Usage: download_data.py --url=<url> --file_path=<file_path>

Options:
--url=<url>                  The url of the data file
--file_path=<file_path>      File path to store the file
'''

from docopt import docopt

opt = docopt(__doc__)

