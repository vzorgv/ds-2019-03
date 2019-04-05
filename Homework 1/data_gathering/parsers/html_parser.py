from parsers.parser import Parser

from bs4 import BeautifulSoup


class AvitoRealtyParser(Parser):
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

            item_table_description = item_container.find("div", {"class": "item_table-wrapper"}) \
                .find("div", {"class": "item_table-description"})
            item_table_header = item_table_description.find("div", {"class": "item_table-header"})
            flat_text_description = item_table_header.find("h3") \
                .find("a") \
                .find("span") \
                .text

            self.__parse_flat_description(flat_text_description, values)

            # Price
            raw_price_value = item_table_header.find("div", {"class": "about"}) \
                .find("span", {"class": "price"}) \
                .get("content")
            try:
                values["Total price"] = float(raw_price_value)
            except ValueError:
                values["Total price"] = None

            item_address = item_table_description.find("p", {"class": "address"})
            is_subway = item_address.find("i", {"class": "i-metro"})

            address = str(item_address.text).strip()
            values["Address"] = address
            values["Subway"] = None
            values["Subway distance (m)"] = None

            if is_subway:
                subway_distance = item_address.find("span", {"class": "c-2"})
                if subway_distance:
                    subway_distance_txt = str(subway_distance.text)
                    values["Subway distance (m)"] = self.__parse_distance(subway_distance_txt)
                    idx = address.find(subway_distance_txt)
                    if idx > 0:
                        values["Subway"] = address[:idx - 1]

            # print(values)
            ret.append(values)

        return ret

    def __parse_distance(self, str_distance):
        factor = 1.0
        idx = str_distance.find(" м")
        if idx != -1:
            str_value = str_distance.replace(" м", "")
        else:
            str_value = str_distance.replace(" км", "")
            factor = 1000

        try:
            ret = float(str_value) * factor
        except ValueError:
            ret = None

        return ret

    def __flat_description_to_list(self, description, delimiter=','):
        return list(map(str.strip, description.split(delimiter)))

    def __parse_flat_description(self, description, labeled_values):
        description_list = self.__flat_description_to_list(description)

        # rooms number
        field_name = "Rooms"
        if description_list[0] in AvitoRealtyParser.__DESCRIPTION_ROOMS:
            labeled_values[field_name] = AvitoRealtyParser.__DESCRIPTION_ROOMS[description_list[0]]
        else:
            labeled_values[field_name] = None

        # area size
        field_name = "Area"
        area_description = self.__flat_description_to_list(description_list[1], " ")
        if len(area_description) == 2:
            try:
                labeled_values[field_name] = float(area_description[0])
            except ValueError:
                labeled_values[field_name] = None
        else:
            labeled_values[field_name] = None

        # floor & floors
        floors_description = self.__flat_description_to_list(description_list[2], "/")
        if len(floors_description) == 2:
            labeled_values["Floor"] = int(floors_description[0])
            labeled_values["Floors"] = int(self.__flat_description_to_list(floors_description[1], " ")[0])
        else:
            labeled_values["Floor"] = None
            labeled_values["Floors"] = None
