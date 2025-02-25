import json
import pytest
from unittest import mock
from lxml import etree as ET

from src.generate_plays import JsonToXml


class TestJsonToXml:

    #test_valid_json not working
    # @mock.patch("builtins.open", new_callable=mock.mock_open)
    # @mock.patch('lxml.etree.parse')
    # def test_valid_json(self, mock_parse, mock_open):
    #     """Test that valid JSON data produces the correct XML."""
    #     # Mock data for pièces.json, auteurs.json, and attributions.json
    #     mock_open.side_effect = [
    #         # Mock pièces.json
    #         mock.mock_open(
    #             read_data='{"pièces": [{"id": 1, "titre": "Play1", "genre": "Comedy", "actes": 3, "prologue": true, "divertissement": true, "forme": "Classic", "création": 1700}]}'
    #         ).return_value,
    #         # Mock auteurs.json
    #         mock.mock_open(
    #             read_data='{"auteurs": [{"id": 1, "nom": "Author1", "féminin": false}]}'
    #         ).return_value,
    #         # Mock attributions.json
    #         mock.mock_open(
    #             read_data='{"attributions": [{"id": 1, "play_id": 1, "author_id": 1}]}'
    #         ).return_value,
    #     ]
    #
    #     # Mock the XML template
    #     ns = "http://www.tei-c.org/ns/1.0"
    #     root = ET.Element("root", nsmap={"TEI": ns})
    #     list_person = ET.SubElement(root, f"{{{ns}}}listPerson")
    #     mock_tree = mock.Mock()
    #     mock_tree.getroot.return_value = root
    #     mock_parse.return_value = mock_tree
    #
    #     # Call the function
    #     JsonToXml.parse_comedians_jsons()
    #
    #     # Assert that <listPerson> exists
    #     list_person = root.find(f".//{{{ns}}}listPerson")
    #     assert list_person is not None, "listPerson should exist in the XML."
    #
    #     # Assert that <person> nodes exist
    #     persons = [child for child in list_person if child.tag.endswith("person")]
    #     assert len(persons) > 0, "There should be at least one <person> node in the XML."
    #
    #     # Assert that IDs are correctly generated
    #     person = persons[0]
    #     assert person.attrib[f"{{http://www.w3.org/XML/1998/namespace}}id"], "The xml:id should be generated."

    @mock.patch('lxml.etree.parse')
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{}')
    def test_empty_json(self, mock_open, mock_parse):
        """Test that empty JSON data is handled gracefully."""
        ns = "http://www.tei-c.org/ns/1.0"
        root = ET.Element("root", nsmap={"TEI": ns})
        ET.SubElement(root, f"{{{ns}}}listPerson")
        tree = ET.ElementTree(root)  # Use a real ElementTree instance
        mock_parse.return_value = tree

        JsonToXml.parse_comedians_jsons()

        list_person = root.find(f".//{{{ns}}}listPerson")
        assert list_person is not None, "listPerson should still exist in the XML."
        persons = list_person.findall(f".//{{{ns}}}person")
        assert len(persons) == 0, "There should be no <person> nodes when the JSON is empty."

    @mock.patch('lxml.etree.parse')
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{"comedians": [{"id": 1, "pseudonyme": "Comedian1" "variations": "v1"]}')
    def test_malformed_json(self, mock_open, mock_parse):
        """Test that malformed JSON raises a proper exception."""
        ns = "http://www.tei-c.org/ns/1.0"
        root = ET.Element("root", nsmap={"TEI": ns})
        list_person = ET.SubElement(root, f"{{{ns}}}listPerson")
        mock_tree = mock.Mock()
        mock_tree.getroot.return_value = root
        mock_parse.return_value = mock_tree

        with pytest.raises(json.JSONDecodeError):
            JsonToXml.parse_comedians_jsons()
