import json
import xml.etree.ElementTree as ET
from typing import Optional


class Comedian:
    def __init__(self, id: Optional[int], pseudonym: Optional[str], variations: Optional[str],
                 first_name: Optional[str], last_name: Optional[str], title: Optional[str], female: Optional[bool],
                 status: Optional[str], entry: Optional[int], society: Optional[int], departure: Optional[int]) -> None:
        self.id = id
        self.pseudonym = pseudonym
        self.variations = variations
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.female = female
        self.status = status
        self.entry = entry
        self.society = society
        self.departure = departure


def main():
    tree = ET.parse('../output/example_prosopohgraphy.xml')
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    comedians = list()
    # flatten "data" to get rid of the awkward key
    # Open and read the JSON file
    with open('../json_exports/comédiens_CF.json', 'r') as file:
        data = json.load(file)

    for entry_list in data.values():
        for entry in entry_list:
            comedian = Comedian(entry['id'], entry['pseudonyme'], entry['variations'], entry['prénom'], entry['nom'],
                                entry['titre'], entry['féminin'], entry['statut'], entry['entrée'], entry['sociétariat'],
                                entry['départ'])
            comedians.append(comedian)

    listPerson = root.find(".//{http://www.tei-c.org/ns/1.0}listPerson")
    # add one <persName> node per <person> with all the subnodes
    # add the other fields as top-level nodes to <person>
    # <person> has an xml:id that is auto-generated

    for comedian in comedians:
        person = ET.SubElement(listPerson, 'person')
        persName = ET.SubElement(person, 'persName')
        forename = ET.SubElement(persName, 'forename')
        forename.text = comedian.first_name

        # Prettify output (requires Python 3.9)
    ET.indent(tree)
    tree.write('../output/example_mod.xml', encoding='UTF-8', xml_declaration=True,
               method='xml')


if __name__ == '__main__':
    main()
