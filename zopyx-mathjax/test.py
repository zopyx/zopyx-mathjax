import os
import sys
import lxml.html
import hashlib

fn = sys.argv[1]

with open(fn, 'r') as fp:
    root = lxml.html.fromstring(fp.read())

for node in root.xpath('//math'):
    formula = node.text.strip()
    print(formula)
    h = hashlib.sha256()
    h.update(formula.encode('utf8'))
    digest = h.hexdigest()
    print(h.hexdigest())

    if not os.path.exists('{}.pdf'.format(digest)):

        with open('template.html', 'r') as fp:
            template = fp.read()

        template = template.replace('$$$$', formula)

        with open('out.html', 'w') as fp:
            fp.write(template)

        cmd = 'wkhtmltopdf out.html --javascript-delay 25000 out.pdf'                
        print(cmd)
        os.system(cmd)

        cmd = './pdfcrop.pl --margins 0 out.pdf {}.pdf'.format(digest)
        print(cmd)
        os.system(cmd)

    img_tag = lxml.html.fromstring('<img src="{}.pdf" style="display:block">'.format(digest))
    node.getparent().replace(node, img_tag)


with open('final.html', 'wb') as fp:
    fp.write(lxml.etree.tostring(root))

cmd = 'run.sh -d final.html >final.pdf'
print(cmd)
os.system(cmd)

