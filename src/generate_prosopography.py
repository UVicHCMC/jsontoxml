import json
import pytest
from unittest import mock
from lxml import etree as ET

from src.generate_plays import JsonToXml


class TestJsonToXml:

    @mock.patch('lxml.etree.parse')
    @mock.patch("builtins.open", new_callable=mock.mock_open,
                read_data='{"comedians": [{"id": 1, "pseudonyme": "Comedian1", "variations": "v1", "pr\u00e9nom": "John", "nom": "Doe", "titre": "Mr.", "f\u00e9minin": false, "statut": "pensionnaire", "entr\u00e9e": 2000, "soci\u00e9tariat": 2011, "d\u00e9part": 2010}]}')
    def test_valid_json(self, mock_parse):
        """Test that valid JSON data is processed correctly."""
        ns = "http://www.tei-c.org/ns/1.0"
        root = ET.Element("root", nsmap={"TEI": ns})
        list_person = ET.SubElement(root, f"{{{ns}}}listPerson")
        mock_tree = mock.Mock()
        mock_tree.getroot.return_value = root
        mock_parse.return_value = mock_tree

        JsonToXml.parse_comedians_jsons()

        list_person = root.find(f".//{{{ns}}}listPerson")
        assert list_person is not None, "listPerson should exist in the XML."

        persons = [child for child in list_person if child.tag.endswith("person")]
        assert len(persons) == 2, f"Expected 1 <person> node, but found {len(persons)}."

        person = persons[0]
        assert person.attrib[f"{{http://www.w3.org/XML/1998/namespace}}id"] == "DOE1", "The xml:id should be correctly generated from the last name."

    @mock.patch('lxml.etree.parse')
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{}')
    def test_empty_json(self, mock_open, mock_parse):
        """Test that empty JSON data is handled gracefully."""
        ns = "http://www.tei-c.org/ns/1.0"
        root = ET.Element("root", nsmap={"TEI": ns})
        list_person = ET.SubElement(root, f"{{{ns}}}listPerson")
        mock_tree = mock.Mock()
        mock_tree.getroot.return_value = root
        mock_parse.return_value = mock_tree

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
