"""Diagram Manual Assistant domain retrieval and answer rules."""
NAME = '05-diagram-manual-assistant'

import re
from collections import deque
from common import norm,require
FIELDS = ("figure","start","end")

def validate(rows):
    keys=[tuple(norm(r[k]) for k in FIELDS) for r in rows]
    require(len(keys)==len(set(keys)),"duplicate diagram link")

def solve(rows,q):
    m=re.fullmatch(r"(.+) in (.+)",q.rstrip("?"))
    if not m: return
    request,fig=m.groups()
    links=sorted((r for r in rows if norm(r["figure"])==fig),key=lambda r:r["id"])
    for prefix,src,dest in [("what follows ","start","end"),("what feeds ","end","start")]:
        if request.startswith(prefix):
            hits=[r for r in links if norm(r[src])==request[len(prefix):]]
            if hits: return ", ".join(r[dest] for r in hits),hits,"adjacency"
    path=re.fullmatch(r"path from (.+?) to (.+)",request)
    if not path: return
    start,end=path.groups()
    queue=deque([(start,[])])
    seen={start}
    while queue:
        node,edges=queue.popleft()
        for r in links:
            target=norm(r["end"])
            if norm(r["start"])!=node or target in seen: continue
            route=edges+[r]
            if target==end: return " → ".join([route[0]["start"]]+[e["end"] for e in route]),route,"shortest directed path"
            seen.add(target)
            queue.append((target,route))
