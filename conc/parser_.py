
from typing import List




def parse(s: str) -> List[str]:
    parsed = s.split(" ")
    if not parsed[-1] == ';':
        parsed.append(';')
    if not parsed[0] == 'EP':
        parsed.insert(0, 'EP')
    return parsed
