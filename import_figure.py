"""Read directed links from a semantically labeled manual SVG."""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import core


def convert(path):
    with path.open("rb") as f:
        raw=f.read(8_000_001)
    core.require(len(raw)<=8_000_000, "SVG exceeds 8 MB")
    root=ET.fromstring(raw)
    core.require(root.tag=="{http://www.w3.org/2000/svg}svg","expected SVG")
    rows=[]
    for link in root.iter():
        fields=("data-figure","data-from","data-to")
        if not any(k in link.attrib for k in fields):
            continue
        core.require(all(k in link.attrib for k in (*fields,"id")),"incomplete link metadata")
        ident=link.attrib["id"]
        rows.append(dict(id=ident,source=f"{path.name}#{ident}",figure=link.attrib["data-figure"],
                         start=link.attrib["data-from"],end=link.attrib["data-to"]))
    core.require(rows,"no labeled links")
    return core.validate(rows)


if __name__=="__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("figure",type=Path)
    print(json.dumps(convert(cli.parse_args().figure),ensure_ascii=False,indent=2))
