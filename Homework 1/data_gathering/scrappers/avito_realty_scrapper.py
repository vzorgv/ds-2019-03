import logging
import requests


logger = logging.getLogger(__name__)


class Scrapper(object):
    """Class for scrapping avito.ru site for 1-room flats sailing data"""

    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def scrap_process(self, storage):

        # You can iterate over ids, or get list of objects
        # from any API, or iterate through pages of any site
        # Do not forget to skip already gathered data
        # Here is an example for you
        head_url = "https://www.avito.ru/moskva/kvartiry/prodam/1-komnatnye?p="
        page_num = "1"
        full_url = head_url + page_num
        response = requests.get(full_url)

        if not response.ok:
            logger.error(response.text)
            # then continue process, or retry, or fix your code

        else:
            # Note: here json can be used as response.json
            data = response.text

            # save scrapped objects here
            # you can save url to identify already scrapped objects
            storage.write_data(data)
