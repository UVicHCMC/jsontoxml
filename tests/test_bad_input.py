import json
import pytest
from unittest import mock
from lxml import etree as ET

from src.generate_plays import JsonToXmlPlays


class TestJsonToXml:

    @mock.patch('lxml.etree.parse')
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data='{}')
    def test_empty_json(self, mock_open, mock_parse):
        """Test that empty JSON data is handled gracefully."""
        ns = "http://www.tei-c.org/ns/1.0"
        root = ET.Element("root", nsmap={"TEI": ns})
        ET.SubElement(root, f"{{{ns}}}listPerson")
        tree = ET.ElementTree(root)  # Use a real ElementTree instance
        mock_parse.return_value = tree

        JsonToXmlPlays.parse_comedians_jsons()

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
            JsonToXmlPlays.parse_comedians_jsons()
