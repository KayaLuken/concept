
from typing import List




def parse(s: str) -> List[str]:
    parsed = s.split(" ")
    if not parsed[-1] == ';':
        parsed.append(';')
    return parsed