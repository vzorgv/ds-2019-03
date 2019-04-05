import logging
import requests
import time

logger = logging.getLogger(__name__)


class Scrapper(object):
    """Class for scrapping avito.ru site for 1-room flats sailing data"""

    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def scrap_process(self, storage):
        base_url = "https://www.avito.ru/moskva/kvartiry/prodam?p="
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0"}

        last_page = 98
        for page_num in range(1, last_page + 1):

            full_url = base_url + str(page_num)

            response = requests.get(full_url, headers=headers)

            if not response.ok:
                logger.error(response.text)
                # then continue process, or retry, or fix your code

            else:
                logger.info(f"Scrapping page {page_num} of {last_page}")
                # Note: here json can be used as response.json
                data = response.text

                # save scrapped objects here
                # you can save url to identify already scrapped objects
                if page_num == 1:
                    storage.write_data(data)
                else:
                    storage.append_data(data)

            time.sleep(0.5)
