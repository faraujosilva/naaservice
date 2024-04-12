import json
import re
import xml.etree.ElementTree as ET
import yaml
from typing import Union
from src.utils.utils import get_nested_value
from src.models.models import ResultOutput

class OutputParser:
    def format(self, data, output_filter):
        raise NotImplementedError("Each parser must implement the format method.")

class JsonParser(OutputParser):
    def format(self, data, output_filter=''):
        formatted_data = {}
        if output_filter:
            if ',' in output_filter or ', ' in output_filter or ' ,' in output_filter:
                output_filter = output_filter.split(',')
                for filter in output_filter:
                    print('Filter:', filter)
                return formatted_data
            jsonpath_expr = get_nested_value(data, output_filter) #cpu_usage
        return data

class PrettyParser(OutputParser):
    def format(self, data, output_filter=''):
        return json.dumps(data, indent=4)

class XmlParser(OutputParser):
    def format(self, data, output_filter=''):
        # Transforming dict to XML requires more logic, this is just a placeholder
        root = ET.Element("data")
        ET.SubElement(root, "output").text = str(data)
        return ET.tostring(root, encoding='unicode')

class YamlParser(OutputParser):
    def format(self, data, output_filter=''):
        return yaml.dump(data)

# Factory to create parser instances
class ParserFactory:
    parsers = {
        'json': JsonParser(),
        'pretty': PrettyParser(),
        'xml': XmlParser(),
        'yaml': YamlParser(),
    }

    @staticmethod
    def get_parser(output_format):
        return ParserFactory.parsers.get(output_format, PrettyParser())

# Main Parser class
class Parser:
    @staticmethod
    def parse_output(output: str, parse_string: str=None, group: int= None):       
        if parse_string:
            match = re.search(parse_string, output)
            if match:
                output = match.group(group)
        return output

    @staticmethod
    def parse_result(output: dict, output_format: str = 'json', output_filter: str = '') -> Union[ResultOutput, str]:
        raise NotImplementedError("Each parser must implement the parse_result method.")