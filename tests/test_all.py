import json
import xml.etree.ElementTree as ET
import pytest
from unittest import mock
from src.generate_prosopography import JsonToXml

class TestJsonToXml:

    @mock.patch('xml.etree.ElementTree.parse')
    @mock.patch("builtins.open", new_callable=mock.mock_open,
                read_data='{"comedians": [{"id": 1, "pseudonyme": "Comedian1", "variations": "v1", "pr\u00e9nom": "John", "nom": "Doe", "titre": "Mr.", "f\u00e9minin": false, "statut": "pensionnaire", "entr\u00e9e": 2000, "soci\u00e9tariat": 2011, "d\u00e9part": 2010}]}')
    def test_valid_json(self, mock_open, mock_parse):
        """Test that valid JSON data is processed correctly."""
        ns = "http://www.tei-c.org/ns/1.0"
        mock_tree = ET.ElementTree(ET.Element("root", xmlns=ns))
        root = mock_tree.getroot()
        ET.SubElement(root, f"{{{ns}}}listPerson")  # Add namespace to listPerson
        mock_parse.return_value = mock_tree

        JsonToXml.parse_comedians_jsons()

        # Debugging: Print the entire XML tree
        print("Final XML Output:")
        print(ET.tostring(root, encoding='unicode'))

        # Locate <listPerson>
        list_person = root.find(f".//{{{ns}}}listPerson")
        assert list_person is not None, "listPerson should exist in the XML."

        # Debugging: List tags of all children in <listPerson>
        print("Tags in listPerson:")
        for child in list_person:
            print(child.tag)

        # Locate <person> nodes manually
        persons = [child for child in list_person if child.tag.endswith("person")]
        assert len(persons) == 2, f"Expected 1 <person> node, but found {len(persons)}."

        # Validate the first <person> node
        person = persons[0]
        assert person.get("xml:id") == "DOE1", "The xml:id should be correctly generated from the last name."

        


    @mock.patch('xml.etree.ElementTree.parse')
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{}')
    def test_empty_json(self, mock_open, mock_parse):
        """Test that empty JSON data is handled gracefully."""
        ns = "http://www.tei-c.org/ns/1.0"
        mock_tree = ET.ElementTree(ET.Element("root", xmlns=ns))
        root = mock_tree.getroot()
        ET.SubElement(root, f"{{{ns}}}listPerson")  # Add namespace to listPerson
        mock_parse.return_value = mock_tree

        JsonToXml.parse_comedians_jsons()

        list_person = root.find(f".//{{{ns}}}listPerson")
        assert list_person is not None, "listPerson should still exist in the XML."
        persons = list_person.findall(f".//{{{ns}}}person")
        assert len(persons) == 0, "There should be no <person> nodes when the JSON is empty."

    @mock.patch('xml.etree.ElementTree.parse')
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{"comedians": [{"id": 1, "pseudonyme": "Comedian1" "variations": "v1"]}')
    def test_malformed_json(self, mock_open, mock_parse):
        """Test that malformed JSON raises a proper exception."""
        ns = "http://www.tei-c.org/ns/1.0"
        mock_tree = ET.ElementTree(ET.Element("root", xmlns=ns))
        root = mock_tree.getroot()
        ET.SubElement(root, f"{{{ns}}}listPerson")  # Add namespace to listPerson
        mock_parse.return_value = mock_tree

        with pytest.raises(json.JSONDecodeError):
            JsonToXml.parse_comedians_jsons()
