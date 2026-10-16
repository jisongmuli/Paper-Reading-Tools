import json
import pathlib
import re
import subprocess
from pypdf import PdfReader
from PIL import Image

import argparse
parser=argparse.ArgumentParser(description='Render up to two candidate figure pages from each paper.')
parser.add_argument('--manifest', type=pathlib.Path, default=pathlib.Path(__file__).with_name('paper_set_2020plus.json'))
parser.add_argument('--root', type=pathlib.Path, default=pathlib.Path('downloads'))
parser.add_argument('--output', type=pathlib.Path, default=pathlib.Path('figures'))
parser.add_argument('--pdftoppm', default='pdftoppm', help='Executable on PATH, or its full path.')
args=parser.parse_args()
root=args.root
out=args.output
out.mkdir(parents=True,exist_ok=True)
poppler=args.pdftoppm
papers=json.loads(args.manifest.read_text(encoding='utf-8'))
for p in papers:
    name=p["short"]
    pdf=next(root.glob(f"*-{name}-{p['year']}/{name}-原论文.pdf"))
    pages=PdfReader(str(pdf)).pages
    figure_pages=[]
    for i,page in enumerate(pages):
        txt=page.extract_text() or ""
        if re.search(r"(?:Figure\s*[12]\s*[:.]|Fig\.\s*[12]\s*[|:])",txt,re.I):
            figure_pages.append(i+1)
        if len(figure_pages)>=2: break
    if not figure_pages:
        figure_pages=list(range(1,min(3,len(pages))+1))[-2:]
    for j,page_no in enumerate(figure_pages[:2],1):
        prefix=out/f"{name}-{j}"
        subprocess.run([str(poppler),"-f",str(page_no),"-l",str(page_no),"-singlefile","-r","130","-png",str(pdf),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        im=Image.open(str(prefix)+".png")
        print(name,j,"PDF p",page_no,im.size)
