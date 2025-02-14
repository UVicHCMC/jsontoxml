import json
from io import StringIO
from unittest import mock
from unittest.mock import patch, MagicMock, mock_open
from lxml import etree as ET
from src.generate_prosopography import JsonToXml
import pytest
from src.comedians import Comedian
from src.authors import Author


@patch("builtins.open", new_callable=mock_open)  # Mock the open function
@patch("lxml.etree.parse", new_callable=MagicMock)  # Mock the ET.parse function
@patch.object(JsonToXml, 'create_comedian_code', return_value=None)  # Mock the create_comedian_code method
def test_parse_comedians_jsons(mock_create_comedian_code, mock_parse, mock_open):
    # Sample data for the JSON files
    comedians_data = {
        "comedians": [
            {
                "id": 1,
                "pseudonyme": "Molière",
                "variations": "Moli",
                "prénom": "Jean",
                "nom": "Baptiste",
                "titre": "Mr",
                "féminin": "FALSE",
                "statut": "pensionnaire",
                "entrée": "1643",
                "sociétariat": "NULL",
                "départ": "1673"
            }
        ]
    }
    authors_data = {
        "authors": [
            {
                "id": 101,
                "nom": "Diderot",
                "féminin": "FALSE"
            }
        ]
    }

    # Mock the open function to return the mock JSON data when reading the respective files
    def mock_open_side_effect(file, mode):
        if file == 'json_exports/comédiens.json':
            return StringIO(json.dumps(comedians_data))  # Proper file-like object
        elif file == 'json_exports/auteurs.json':
            return StringIO(json.dumps(authors_data))
        return MagicMock()  # Default fallback

    mock_open.side_effect = mock_open_side_effect

    # Create a real XML tree
    NSMAP = {"tei": "http://www.tei-c.org/ns/1.0"}

    root = ET.Element("TEI", nsmap=NSMAP)
    list_person = ET.SubElement(root, "{http://www.tei-c.org/ns/1.0}listPerson") # Properly created element

    # Mock parse to return this tree
    tree = ET.ElementTree(root)
    mock_parse.return_value = tree


    # need to create an actual element tree, a mock won't do for parsing
    JsonToXml.parse_comedians_jsons(output_file='tests/test_prosopography.xml')

    # Verifying that the XML was parsed and written
    mock_parse.assert_called_once_with('output/template_prosopography.xml')

    # Check if the person was added to listPerson
    list_person.append.assert_called_once()

    # Check the content of the 'idno' element (comedian ID)
    mock_person = list_person.append.call_args[0][0]  # Get the mock person from append
    idno = mock_person.find("idno")
    assert idno is not None
    assert idno.text == "1"  # Comedian ID should be '1'

    # Check if the comedian's pseudonym is correctly added
    pers_name = mock_person.find('persName')
    assert pers_name.find('reg').text == "Molière"  # Pseudonym

    # Check occupation attribute is set correctly
    occupation = mock_person.find('occupation')
    assert occupation.attrib['type'] == "pensionnaire"  # Status is 'pensionnaire'

    # Check if author is added correctly
    mock_list_person.append.assert_called_with(mock.ANY)  # Check that append was called with any element

    # Check if the author's idno is correct
    author_person = mock_list_person.append.call_args[0][0]
    author_idno = author_person.find("idno")
    assert author_idno is not None
    assert author_idno.text == "101"  # Author ID should be '101'

# Run the test using pytest:
# pytest test_json_to_xml.py
