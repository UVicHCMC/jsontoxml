import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
from typing import Optional

# Open and read the JSON file
with open('actors.json', 'r') as file:
    data = json.load(file)


class Actor:
    def __init__(self, id: Optional[int], pseudonym: Optional[str], pseudonym_number: Optional[int], honorific: Optional[str],
                 first_name: Optional[str], last_name: Optional[str], alias: Optional[str], status: Optional[str], entree: Optional[int],
                 societariat: Optional[int], depart: Optional[int], debut: Optional[list[int]], notes: Optional[str]) -> None:
        self.notes = notes
        self.debut = debut
        self.depart = depart
        self.societariat = societariat
        self.entree = entree
        self.status = status
        self.alias = alias
        self.last_name = last_name
        self.first_name = first_name
        self.honorific = honorific
        self.pseudonym_number = pseudonym_number
        self.pseudonym = pseudonym
        self.id = id


tree = ET.parse('example.xml')
ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
root = tree.getroot()

actors = list()

for entry in data:
    actor = Actor
    actor.id = entry['id']
    actor.pseudonym = entry['pseudonym']
    actor.pseudonym_number = entry['pseudonym_number']
    actor.honorific = entry['honorific']
    actor.first_name = entry['first_name']
    actor.last_name = entry['last_name']
    actor.alias = entry['alias']
    actor.status = entry['status']
    actor.entree = entry['entree']
    actor.societariat = entry['societariat']
    actor.depart = entry['depart']
    actor.debut = entry['debut']
    actor.notes = entry['notes']
    actors.append(actor)

spot = root.find(".//{http://www.tei-c.org/ns/1.0}people")

for actor in actors:
    text_to_write = "\n<person>\n"
    text_to_write += f"<id>{actor.id}</id>\n"
    text_to_write += f"<pseudonym>{actor.pseudonym}</pseudonym>\n"
    text_to_write += f"<pseudonymNumber>{actor.pseudonym_number}</pseudonymNumber>\n"
    text_to_write += f"<honorific>{actor.honorific}</honorific>\n"
    text_to_write += f"<firstName>{actor.first_name}</firstName>\n"
    text_to_write += f"<lastName>{actor.last_name}</lastName>\n"
    text_to_write += f"<alias>{actor.alias}</alias>\n"
    text_to_write += f"<status>{actor.status}</status>\n"
    text_to_write += f"<entree>{actor.entree}</entree>\n"
    text_to_write += f"<societariat>{actor.societariat}</societariat>\n"
    text_to_write += f"<depart>{actor.depart}</depart>\n"
    text_to_write += f"<debut>{actor.debut}</debut>\n"
    text_to_write += f"<notes>{actor.notes}</notes>\n"
    text_to_write += "</person>\n"
    spot.append(ET.fromstring(text_to_write))

    # Prettify output (requires Python 3.9)
ET.indent(tree)
tree.write('example_mod.xml', encoding='UTF-8', xml_declaration=True,
            method='xml')

