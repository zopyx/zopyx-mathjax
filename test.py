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

    if not os.path.exists(f'{digest}.pdf'):

        with open('template.html', 'r') as fp:
            template = fp.read()

        template = template.replace('$$$$', formula)

        with open('out.html', 'w') as fp:
            fp.write(template)

        cmd = 'wkhtmltopdf out.html --javascript-delay 7500 out.pdf'
#        cmd = 'phantomjs pdf.js out.html out.pdf'                
        print(cmd)
        os.system(cmd)

        cmd = f'./pdfcrop.pl --margins 0 out.pdf {digest}.pdf'
        print(cmd)
        os.system(cmd)

    img_tag = lxml.html.fromstring(
        f'<img src="{digest}.pdf" style="display:block">'
    )

    node.getparent().replace(node, img_tag)


with open('final.html', 'wb') as fp:
    fp.write(lxml.etree.tostring(root))

cmd = 'run.sh -d final.html >final.pdf'
print(cmd)
os.system(cmd)

