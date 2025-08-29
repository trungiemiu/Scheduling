import re

_gene_re = re.compile(r"^J(\d+)O(\d+)$")

def parse_gene(g):
    m = _gene_re.match(g)
    if not m:
        raise ValueError(f"Invalid gene format: {g}")
    j = int(m.group(1))
    o = int(m.group(2))
    return j, o
