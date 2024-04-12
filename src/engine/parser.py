import re
from typing import Union

class Parser:
    @staticmethod
    def parse(output: str, parse_string: str, group: int) -> str:
        search = re.search(parse_string, output)
        if search:
            output = search.group(group)
        return output