import mellea
import re
from statute_data import alabama

def parse_AL(file: str) -> list[str]:
    citations = []
    pattern = r"Ala\. Code §"
    matches = [m.start() for m in re.finditer(pattern, file)]
    for match in matches:
        end = re.search(r"\d{4}\)", file[match+1:])
        citations.append(file[match:end.end()+match+1])
    return citations

def check_AL(citations: list[str]) -> list[bool]:
    statute_exists = []
    for citation in citations:
        start = citation.find("§") + 1
        end = citation[start:].find(" ")
        statute = citation[start:start+end]
        [title, section, rest] = statute.split("-")
        print(title, section, rest)
        if title not in alabama:
            statute_exists.append(False)
            continue
        if section not in alabama[title]:
            statute_exists.append(False)
            continue
        search = alabama[title][section]
        if float(rest) in search:
            statute_exists.append(True)
            continue
        if isinstance(search, list):
            found = False
            for item in search:
                if isinstance(item, tuple):
                    if int(rest) >= item[0] and int(rest) < item[1]:
                        statute_exists.append(True)
                        found = True
                        break
                else:
                    continue
            if not found:
                statute_exists.append(False)
                continue
        else:
            if "." not in rest:
                statute_exists.append(False)
                continue
            [a, b] = rest.split(".")
            if a in search:
                found = False
                for item in search[a]:
                    if isinstance(item, tuple):
                        if int(b) >= item[0] and int(b) < item[1]:
                            statute_exists.append(True)
                            found = True
                            break
                    else:
                        continue
                if not found:
                    statute_exists.append(False)
                    continue
            else:
                statute_exists.append(False)
                continue
    return statute_exists




text = """
blah blah Ala. Code §1-9-20 (2020) blah blah blah Ala. Code §10A-21-8 (1999) blah blah
Ala. Code §2-7A-3 (2024)
"""

statutes = parse_AL(text)
print(statutes)
print(check_AL(statutes))