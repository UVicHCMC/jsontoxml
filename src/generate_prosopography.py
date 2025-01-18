import json
import xml.etree.ElementTree as ET

from src.authors import Author
from src.comedians import Comedian


class JsonToXml:
    @staticmethod
    def parse_comedians_jsons():
        tree = ET.parse('../output/template_prosopography.xml')
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
            if comedian.last_name:
                JsonToXml.create_comedian_code(comedian.last_name, num, person, seen)

            elif comedian.pseudonym:
                JsonToXml.create_comedian_code(comedian.pseudonym, num, person, seen)

            if comedian.status == 'pensionnaire' or comedian.status == 'sociétaire':
                person.set('ana', 'comédien.ne CF')

            if comedian.status == 'ocasionnel':
                person.set('ana', 'comédien.ne occasionnel.le')

            idno = ET.SubElement(person, 'idno')
            idno.set('type', 'base_unifiée')
            idno.text = str(comedian.id)

            pers_name = ET.SubElement(person, 'persName')

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
                additional_occupation = ET.SubElement(person, 'occupation')
                additional_occupation.set('type', 'sociétariat')
                if comedian.society:
                    additional_occupation.set('when', str(comedian.society))
            if comedian.status == 'ocasionnel':
                occupation.set('type', 'occasionnel')

        authors = list()
        # flatten "data" to get rid of the awkward key
        # Open and read the JSON file
        with open('../json_exports/auteurs.json', 'r') as file:
            data = json.load(file)

        for entry_list in data.values():
            for entry in entry_list:
                author = Author(entry['id'], entry['nom'], entry['féminin'])
                authors.append(author)

        list_person = root.find(".//{http://www.tei-c.org/ns/1.0}listPerson")
        # add one <persName> node per <person> with all the subnodes
        # add the other fields as top-level nodes to <person>
        # <person> has an xml:id that is auto-generated

        for author in authors:
            num = 1
            person = ET.SubElement(list_person, 'person')
            # if comedian last name-code is already used, increment the digit number. E.g. MOLI1, MOLI2
            if author.pseudonym:
                JsonToXml.create_comedian_code(author.pseudonym, num, person, seen)

            idno = ET.SubElement(person, 'idno')
            idno.set('type', 'base_unifiee')
            idno.text = str(author.id)

            pers_name = ET.SubElement(person, 'persName')

            pseudonym = ET.SubElement(pers_name, 'reg')
            pseudonym.text = author.pseudonym

            # gender and occupation fields
            gender = ET.SubElement(person, 'gender')

            if author.female:
                gender.set('type', 'feminin')
            else:
                gender.set('type', 'masculin')

        # Prettify output (requires Python 3.9)
        ET.indent(tree)
        tree.write('../output/prosopography.xml', encoding='UTF-8', xml_declaration=True,
                   method='xml')

    @staticmethod
    def create_comedian_code(comedian_string, num, person, seen):
        comedian_string = comedian_string.replace(' ', '')
        comedian_string = comedian_string.replace('\'', '')
        if comedian_string[0:4] in seen:
            num = seen.count(comedian_string[0:4]) + 1
        comedian_code = f"{comedian_string[0:4].upper()}{num}"
        seen.append(comedian_string[0:4])
        person.set('xml:id', comedian_code)


if __name__ == '__main__':
    JsonToXml.parse_comedians_jsons()
