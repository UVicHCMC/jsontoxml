import json
import pytest
from unittest import mock
from lxml import etree as ET

from src.generate_plays import JsonToXml

EXPECTED_XML = """<person xml:id="DOE1" ana="comédien.ne CF">  <idno type="base_unifiée">1</idno>  <persName>    <reg>Monsieur Doe</reg>    <forename>John</forename>    <surname>Doe</surname>    <addName type="variations">Doe V1</addName>    <addName type="titre">Monsieur</addName>  </persName>  <gender type="masculin"/>  <occupation type="acteur.rice" from="1685" to="1712"/>  <occupation type="sociétariat" when="1685"/></person>"""


class TestJsonToXml:
    @mock.patch('lxml.etree.parse')
    def test_valid_json(self, mock_parse):
        input_json = {
            "comedians": [{"id": 1, "nom": "Doe", "prénom": "John"}]
        }

        ns = "http://www.tei-c.org/ns/1.0"
        root = ET.Element("root", nsmap={"TEI": ns})
        tree = ET.ElementTree(root)
        mock_parse.return_value = tree

        JsonToXml.parse_comedians_jsons(input_json)

        person = root.find(f".//{{{ns}}}person")
        assert person is not None, "Person element should be present."

