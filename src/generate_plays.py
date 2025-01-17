import json
import xml.etree.ElementTree as ET

from src.plays import Play


class JsonToXml:
    @staticmethod
    def parse_comedians_jsons():
        tree = ET.parse('../output/template_plays.xml')
        ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
        root = tree.getroot()

        plays = []
        # flatten "data" to get rid of the awkward key
        # Open and read the JSON file
        with open('../json_exports/pièces.json', 'r') as file:
            data = json.load(file)

        for play_list in data.values():
            for entry in play_list:
                play = Play(entry['id'], entry['titre'], entry['genre'], entry['actes'],
                                    entry['prologue'],
                                    entry['divertissement'], entry['forme'], entry['création'])
                plays.append(play)

        list = root.find(".//{http://www.tei-c.org/ns/1.0}list")
        # add one <persName> node per <person> with all the subnodes
        # add the other fields as top-level nodes to <person>
        # <person> has an xml:id that is auto-generated

        seen = []

        for play in plays:
            num = 1
            item = ET.SubElement(list, 'item')

            # if play title name-code is already used, increment the digit number. E.g. PLAY1, PLAY2

            if play.title:
                JsonToXml.create_title_code(play.title, num, item, seen)



        # Prettify output (requires Python 3.9)
        ET.indent(tree)
        tree.write('../output/plays.xml', encoding='UTF-8', xml_declaration=True,
                   method='xml')

    @staticmethod
    def create_title_code(title_string, num, item, seen):

        title_string = title_string.replace(' ', '')
        title_string = title_string.replace('\'', '')
        if title_string[0:4] in seen:
            num = seen.count(title_string[0:4]) + 1
        comedian_code = f"{title_string[0:4].upper()}{num}"
        seen.append(title_string[0:4])
        item.set('xml:id', comedian_code)


if __name__ == '__main__':
    JsonToXml.parse_comedians_jsons()
