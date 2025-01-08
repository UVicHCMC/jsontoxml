import json
import xml.etree.ElementTree as ET

from src.comedians import Comedian


class JsonToXml:
    @staticmethod
    def parse_json():
        tree = ET.parse('../output/example_prosopography.xml')
        ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
        root = tree.getroot()

        comedians = list()
        # flatten "data" to get rid of the awkward key
        # Open and read the JSON file
        with open('../json_exports/comédiens.json', 'r') as file:
            data = json.load(file)

        for entry_list in data.values():
            for entry in entry_list:
                comedian = Comedian(entry['id'], entry['pseudonyme'], entry['variations'], entry['prénom'],
                                    entry['nom'],
                                    entry['titre'], entry['féminin'], entry['statut'], entry['entrée'],
                                    entry['sociétariat'],
                                    entry['départ'])
                comedians.append(comedian)

        list_person = root.find(".//{http://www.tei-c.org/ns/1.0}listPerson")
        # add one <persName> node per <person> with all the subnodes
        # add the other fields as top-level nodes to <person>
        # <person> has an xml:id that is auto-generated

        seen = []

        for comedian in comedians:
            num = 1
            person = ET.SubElement(list_person, 'person')
            # if comedian last name-code is already used, increment the digit number. E.g. MOLI1, MOLI2
            # todo: write unit test to exercise the name code and also the incrementation if there are repeated last names
            # todo: ask what to do if there are no last names for a given entry. What does the xml:id become in that case?
            if comedian.last_name:
                if comedian.last_name[0:4] in seen:
                    num = seen.count(comedian.last_name[0:4]) + 1
                comedian_code = f"{comedian.last_name[0:4].upper()}{num}"
                seen.append(comedian.last_name[0:4])

                person.set('xml:id', comedian_code)

            person.set('ana', 'comédien.ne CF')

            pers_name = ET.SubElement(person, 'persName')

            idno = ET.SubElement(pers_name, 'idno')
            idno.set('type', 'base_unifiee')
            idno.text = str(comedian.id)

            pseudonym = ET.SubElement(pers_name, 'reg')
            pseudonym.text = comedian.pseudonym

            forename = ET.SubElement(pers_name, 'forename')
            forename.text = comedian.first_name

            surname = ET.SubElement(pers_name, 'surname')
            surname.text = comedian.last_name

            variations = ET.SubElement(pers_name, 'addName')
            variations.text = comedian.variations
            variations.set('type', 'variations')

            variations = ET.SubElement(pers_name, 'addName')
            variations.text = comedian.title
            variations.set('type', 'titre')

            # gender and occupation fields
            gender = ET.SubElement(person, 'gender')

            if comedian.female:
                gender.set('type', 'feminin')
            else:
                gender.set('type', 'masculin')

            occupation = ET.SubElement(person, 'occupation')

            if comedian.status == 'pensionnaire':
                occupation.set('type', comedian.status)
                if comedian.entry and comedian.departure:
                    occupation.set('from', str(comedian.entry))
                    occupation.set('to', str(comedian.departure))
            if comedian.status == 'sociétaire':
                occupation.set('type', 'acteur.rice')
                if comedian.entry and comedian.departure:
                    occupation.set('from', str(comedian.entry))
                    occupation.set('to', str(comedian.departure))
                occupation2 = ET.SubElement(person, 'occupation')
                occupation2.set('type', 'sociétariat')
                if comedian.society:
                    occupation2.set('when', str(comedian.society))
            if comedian.status == 'ocasionnel':
                occupation.set('type', comedian.status)

            # Prettify output (requires Python 3.9)
        ET.indent(tree)
        tree.write('../output/example_mod.xml', encoding='UTF-8', xml_declaration=True,
                   method='xml')



if __name__ == '__main__':
    JsonToXml.parse_json()
