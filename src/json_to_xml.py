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
    num = 1
    seen = []
    for comedian in comedians:
        person = ET.SubElement(listPerson, 'person')
        # if comedian last name-code is already used, increment the digit number. E.g. MOLI1, MOLI2
        # todo: write unit test to exercise the name code and also the incrementation if there are repeated last names
        # todo: ask what to do if there are no last names for a given entry. What does the xml:id become in that case?
        if comedian.last_name:
            if comedian.last_name[0:4] in seen:
                num += 1
            comedian_code = f"{comedian.last_name[0:4]}{num}"
            seen.append(comedian.last_name[0:4])

            person.set('xml:id', comedian_code)

        person.set('ana', 'comédien.ne CF')

        persName = ET.SubElement(person, 'persName')

        idno = ET.SubElement(persName, 'idno')
        idno.set('type', 'base_unifiee')
        idno.text = str(comedian.id)

        pseudonym = ET.SubElement(persName, 'reg')
        pseudonym.text = comedian.pseudonym

        forename = ET.SubElement(persName, 'forename')
        forename.text = comedian.first_name

        surname = ET.SubElement(persName, 'surname')
        surname.text = comedian.last_name

        variations = ET.SubElement(persName, 'addName')
        variations.text = comedian.variations
        variations.set('type', 'variations')

        variations = ET.SubElement(persName, 'addName')
        variations.text = comedian.title
        variations.set('titre', 'variations')


        # Prettify output (requires Python 3.9)
    ET.indent(tree)
    tree.write('../output/example_mod.xml', encoding='UTF-8', xml_declaration=True,
               method='xml')


if __name__ == '__main__':
    main()
