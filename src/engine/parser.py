import re
from typing import Union

class Parser:
    @staticmethod
    def parse(output: str, parse_string: str, group: int) -> Union[str, None]:
        search = re.search(parse_string, output)
        if search:
            return search.group(group)
        return None