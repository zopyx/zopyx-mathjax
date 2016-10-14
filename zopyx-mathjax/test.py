import sys
import lxml.html
import hashlib

fn = sys.argv[1]

with open(fn, 'r') as fp:
    root = lxml.html.fromstring(fp.read())

for node in root.xpath('//math'):
    formula = node.text.strip().encode('utf8')
    print(formula)
    h = hashlib.sha256()
    h.update(formula)
    print(h.hexdigest())

                
