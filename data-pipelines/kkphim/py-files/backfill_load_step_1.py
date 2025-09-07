from datetime import datetime
import sys

sys.path.append('../common')
from utils import Kkphim

def main(args):
    """
    Crawls data from the kkphim webiste based on the specified start and end times.

    The function retrieves the page IDs corresponding to the given start and end times,
    then crawls data from the starting page ID to the ending page ID. The collected
    data is stored as JSON files in the local directory

    Global variables:
        args (dict): A dictionary containining 'start_time' and 'end_time' keys

    Returns:
        int: Returns 0 upon successful completion.
    """

    # global args

    start_time = args['start_time']
    end_time = args['end_time']

    start_page_id = Kkphim.find_page_id(start_time)
    end_page_id = Kkphim.find_page_id(end_time)

    # crawl data from start_page_id to end_page_id
    Kkphim.crawl_data(start_page_id, end_page_id)

    return 0

if __name__ == "__main__":
    args = {
        'start_time': '2024-11-01',
        'end_time': '2024-11-10'
    }

    main()