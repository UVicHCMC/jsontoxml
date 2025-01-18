import json
import xml.etree.ElementTree as ET

from src.attributions import Attribution
from src.authors import Author
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

        authors = []
        # flatten "data" to get rid of the awkward key
        # Open and read the JSON file
        with open('../json_exports/auteurs.json', 'r') as file:
            data = json.load(file)

        for entry_list in data.values():
            for entry in entry_list:
                author = Author(entry['id'], entry['nom'], entry['féminin'])
                authors.append(author)

        attributions = []
        # flatten "data" to get rid of the awkward key
        # Open and read the JSON file
        with open('../json_exports/attributions.json', 'r') as file:
            data = json.load(file)

        for entry_list in data.values():
            for entry in entry_list:
                attribution = Attribution(entry['id'], entry['id_pièce'], entry['id_auteur'])
                attributions.append(attribution)

        seen = []

        for play in plays:
            num = 1
            item = ET.SubElement(list, 'item')

            # if play title name-code is already used, increment the digit number. E.g. PLAY1, PLAY2

            if play.title:
                JsonToXml.create_title_code(play.title, num, item, seen)

            bibl = ET.SubElement(item, 'bibl')

            idno = ET.SubElement(bibl, 'idno')
            idno.set('type', 'base_unifiée')
            idno.text = str(play.id)

            title = ET.SubElement(bibl, 'title')
            title.text = play.title

            author_el = ET.SubElement(bibl, 'author')

            for attribution in attributions:
                if attribution.play_id == play.id:
                    for author in authors:
                        if author.id == attribution.author_id:
                            author_el.text = author.pseudonym


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
