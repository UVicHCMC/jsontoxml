import json
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open
from lxml import etree as ET
from src.generate_prosopography import JsonToXmlProsopography


@patch("builtins.open", new_callable=mock_open)  # Mock the open function
@patch("lxml.etree.parse", new_callable=MagicMock)  # Mock the ET.parse function
@patch.object(JsonToXmlProsopography, 'create_comedian_code', return_value=None)  # Mock the create_comedian_code method
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
    nsmap = {"tei": "http://www.tei-c.org/ns/1.0"}

    root = ET.Element("TEI", nsmap=nsmap)
    list_person = ET.SubElement(root, "{http://www.tei-c.org/ns/1.0}listPerson")  # Properly created element

    # Mock parse to return this tree
    tree = ET.ElementTree(root)
    mock_parse.return_value = tree

    # need to create an actual element tree, a mock won't do for parsing
    # also have to change the output file, lest it override the actual prosopography
    JsonToXmlProsopography.parse_comedians_jsons(output_file='tests/test_prosopography.xml')

    # Verifying that the XML was parsed and written
    mock_parse.assert_called_once_with('templates/template_prosopography.xml')

    # test the output results
    output_tree = ET.parse('tests/test_prosopography.xml')
    ET.register_namespace('TEI', "http://www.tei-c.org/ns/1.0")
    root = output_tree.getroot()
    comedian = root.find(".//{http://www.tei-c.org/ns/1.0}listPerson/person[@ana='comédien.ne CF']")
    comedian_idno = comedian.find('idno')
    # Check the content of the 'idno' element (comedian ID)

    assert comedian_idno is not None
    assert comedian_idno.text == "1"  # Comedian ID should be '1'

    # Check if the comedian's pseudonym is correctly added
    comedian_name = comedian.find('persName')
    assert comedian_name.find('reg').text == "Molière"  # Pseudonym

    # Check occupation attribute is set correctly
    comedian_occupation = comedian.find('occupation')
    assert comedian_occupation.attrib['type'] == "pensionnaire"  # Status is 'pensionnaire'

    # Check if the author's idno is correct
    author_person = root.find(".//{http://www.tei-c.org/ns/1.0}listPerson/person[@ana='auteur.rice']")
    author_idno = author_person.find("idno")
    assert author_idno is not None
    assert author_idno.text == "101"  # Author ID should be '101'

    author_name = author_person.find("persName")
    assert author_name.find('reg').text == "Diderot"  # Pseudonym

    author_gender = author_person.find("gender")
    assert author_gender.attrib['value'] == 'féminin'


