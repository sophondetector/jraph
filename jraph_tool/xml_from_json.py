import typing
import json
from lxml import etree


def json_obj_to_xml(parent_element: typing.Optional[etree.Element], new_element_name: str, obj: typing.Union[bool, float, int, str, dict, list]):
    """
    Recursively walk an object and return its XML representation.

    Args:
        parent_element (typing.Optional[etree.Element]): The element that will be the parent of the element that this
            function will create and return.

        new_element_name (str): The name of the element that will be created.

        obj (typing.Union[bool, float, int, str, dict, list]): The object to return XML for.  It is expected that all
            objects passed to this function can be represented in JSON.

    Returns:
        result (etree.Element): An XML element.

    """

    if parent_element is not None:
        new_element = etree.SubElement(parent_element, new_element_name)

    else:
        new_element = etree.Element(new_element_name)

    if type(obj) == dict:
        for key, value in obj.items():
            if type(value) in (dict, list):
                json_obj_to_xml(new_element, key, value)

            else:
                # Convert values to a string, make sure boolean values are lowercase
                new_element.attrib[key] = str(value).lower() if type(
                    value) == bool else str(value)

    elif type(obj) == list:
        for list_item in obj:
            # List items have to have a name.  Here we borrow "li" from HTML which stands for list item.
            json_obj_to_xml(new_element, 'li', list_item)

    else:
        # Convert everything to a string, make sure boolean values are lowercase
        new_element.text = str(obj).lower() if type(obj) == bool else str(obj)

    return new_element


if __name__ == '__main__':
    # Read JSON file into a dictionary
    json_file = 'lib/data/nodes.json'
    json_file_hndl = open(json_file)
    json_dict = json.load(json_file_hndl)
    json_file_hndl.close()

    # Recursively walk the dictionary to create the XML
    root_xml_element = json_obj_to_xml(None, 'root', json_dict)

    # Write the XML file
    xml_file = f'{json_file}.xml'
    with open(xml_file, 'wb') as xml_file_hndl:
        xml_file_hndl.write(etree.tostring(
            root_xml_element, pretty_print=True, xml_declaration=True))
