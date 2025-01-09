import json
import xml.etree.ElementTree as ET
from unittest import mock

from src.json_to_xml import JsonToXml


class TestJsonToXml:
    @mock.patch('xml.etree.ElementTree.parse')
    @mock.patch("builtins.open", new_callable=mock.mock_open,
                read_data='{"comedians": [{"id": 1, "pseudonyme": "Comedian1", "variations": "v1", "prénom": "John", '
                          '"nom": "Doe", "titre": "Mr.", "féminin": false, "statut": "pensionnaire", "entrée": 2000, '
                          '"sociétariat": 2011, "départ": 2010}]}')
    def test_parse_json(self, mock_parse_json, mock_open):
        # Create a temporary directory structure and files

        mock_tree = ET.ElementTree(ET.Element("root"))
        ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
        root = mock_tree.getroot()
        mock_list_person = ET.SubElement(root, "listPerson")
        mock_parse_json.return_value = mock_tree
        JsonToXml.parse_json()
        # Check if the XML tree was modified correctly
        persons = mock_list_person.findall(".//person")
        assert len(persons) == 1

        person = persons[0]

        assert person.get("xml:id") == "DOE1", "The xml:id should be correctly generated from the last name"

        # Check the elements inside <persName>
        pers_name = person.find(".//persName")
        assert pers_name, "Should have <persName> tag"
        assert pers_name.find("idno").text == "1", "ID should match comedian's ID"
        assert pers_name.find("reg").text == "Comedian1", "Pseudonym should match comedian's pseudonym"
        assert pers_name.find("forename").text == "John", "First name should match comedian's first name"
        assert pers_name.find("surname").text == "Doe", "Last name should match comedian's last name"

        # Check the occupation fields
        occupation = person.find(".//occupation")
        assert occupation.get("type") == "pensionnaire", "Occupation type should match comedian's status"
        assert occupation.get("from") == 2000, "Entry year should match comedian's entry year"
        assert occupation.get("to") == 2010, "Departure year should match comedian's departure year"

    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='{"id": 1, "pseudonyme": '
                                                                        '"Comedian1", "variations": "v1", '
                                                                        '"prénom": "John","nom": "Doe", "titre": "Mr.", '
                                                                        '"féminin": false, "statut": "pensionnaire", '
                                                                        '"entrée": 2000, "sociétariat": 2011, '
                                                                        '"départ": 2010}')
    def test_open(self, mock_open):
        with open('test.json', 'r') as file:
            data = json.load(file)
            assert data['id'] == 1
            assert data['pseudonyme'] == 'Comedian1'
            # todo: finish this up
