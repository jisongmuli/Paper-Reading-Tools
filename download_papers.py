import concurrent.futures
import json
import pathlib
import urllib.request

from pypdf import PdfReader

import argparse
parser = argparse.ArgumentParser(description='Download PDFs from a public paper URL manifest.')
parser.add_argument('--manifest', type=pathlib.Path, default=pathlib.Path(__file__).with_name('paper_set_2020plus.json'))
parser.add_argument('--output', type=pathlib.Path, default=pathlib.Path('downloads'))
args = parser.parse_args()
ROOT = args.output
PAPERS = json.loads(args.manifest.read_text(encoding='utf-8'))
NUMS = ["第一篇", "第二篇", "第三篇", "第四篇", "第五篇", "第六篇", "第七篇", "第八篇", "第九篇", "第十篇"]


def fetch(p):
    folder = ROOT / f"{NUMS[p['n']-1]}-{p['short']}-{p['year']}"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"{p['short']}-原论文.pdf"
    if not target.exists():
        req = urllib.request.Request(p["pdf"], headers={"User-Agent": "Mozilla/5.0 (academic paper reading)"})
        with urllib.request.urlopen(req, timeout=90) as response:
            data = response.read()
        if not data.startswith(b"%PDF-"):
            raise ValueError(f"not PDF: {p['short']} {len(data)} bytes")
        target.write_bytes(data)
    reader = PdfReader(str(target))
    return f"{p['short']}: {len(reader.pages)} pages, {target.stat().st_size} bytes"


if __name__ == "__main__":
    ROOT.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for result in pool.map(fetch, PAPERS):
            print(result)
