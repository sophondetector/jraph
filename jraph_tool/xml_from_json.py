import json
import typing
from lxml import etree


def json_obj_to_xml(parent_element: typing.Optional[etree.Element],
                    new_element_name: str,
                    obj: typing.Union[bool, float, int, str, dict, list]):
    """
    Recursively walk an object and return its XML representation.

    Args:
        parent_element (typing.Optional[etree.Element]):
            The element that will be the parent of the element that this
            function will create and return.

        new_element_name (str): The name of the element that will be created.

        obj (typing.Union[bool, float, int, str, dict, list]):
            The object to return XML for.  It is expected that all
            objects passed to this function can be represented in JSON.

    Returns:
        result (etree.Element): An XML element.

    """

    if parent_element is not None:
        new_element = etree.SubElement(parent_element, new_element_name)

    else:
        new_element = etree.Element(new_element_name)

    if type(obj) is dict:
        for key, value in obj.items():
            if type(value) in (dict, list):
                json_obj_to_xml(new_element, key, value)

            else:
                # Convert values to a string
                # make sure boolean values are lowercase
                new_element.attrib[key] = str(value).lower() if type(
                    value) is bool else str(value)

    elif type(obj) is list:
        for list_item in obj:
            # List items have to have a name.
            # Here we borrow "li" from HTML which stands for list item.
            json_obj_to_xml(new_element, 'li', list_item)

    else:
        # Convert everything to a string,
        # make sure boolean values are lowercase
        new_element.text = str(obj).lower() if type(obj) is bool else str(obj)

    return new_element


def xml_to_string(root_xml_element) -> str:
    return etree.tostring(
        root_xml_element, pretty_print=True, xml_declaration=True)


def json_to_xml_string(_in: object) -> str:
    return xml_to_string(
        json_obj_to_xml(None, 'root', _in))


if __name__ == '__main__':
    json_input_file = 'lib/data/edges.json'
    output_xml_file = 'output.xml'
    with open(json_input_file) as fh:
        json_dict = json.load(fh)

    # Recursively walk the dictionary to create the XML
    root_xml_element = json_obj_to_xml(None, 'root', json_dict)

    # Write the XML file
    with open(output_xml_file, 'wb') as xml_file_hndl:
        xml_file_hndl.write(xml_to_string(root_xml_element))
