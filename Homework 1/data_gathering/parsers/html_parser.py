from parsers.parser import Parser

from bs4 import BeautifulSoup


class AvitoParser(Parser):

    __DESCRIPTION_ROOMS = {"1-к квартира": 1, "2-к квартира": 2, "3-к квартира": 3, "4-к квартира": 4}

    def parse(self, data):
        """
        Parses html text and extracts field values
        :param data: html text (page)
        :return: a dictionary where key is one
        of defined fields and value is this field's value
        """
        soup = BeautifulSoup(data, "html.parser")
        catalog = soup.find_all("div", {"class": "item_table"})

        ret = list()

        for item_container in catalog:
            values = dict()
            flat_text_dscription = item_container.find("div", {"class": "item_table-wrapper"})\
                                .find("div", {"class": "item_table-description"})\
                                .find("div", {"class": "item_table-header"})\
                                .find("h3")\
                                .find("a")\
                                .find("span")\
                                .text

            self.__description_to_dictionary(flat_text_dscription, values)
            ret.append(values)

            print(values)

        return ret

    def __parse_description(self, description):
        return list(map(str.strip, description.split(',')))

    def __description_to_dictionary(self, description, labeled_values):
        description_list = self.__parse_description(description)

        for fieldname in self.fields:
            if fieldname == "Rooms":
                if description_list[0] in AvitoParser.__DESCRIPTION_ROOMS:
                    labeled_values[fieldname] = AvitoParser.__DESCRIPTION_ROOMS[description_list[0]]
