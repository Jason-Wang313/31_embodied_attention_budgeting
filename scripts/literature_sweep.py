import csv
import html
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ARXIV_QUERIES = [
    "cat:cs.RO",
    "cat:cs.CV AND robotics",
    "cat:eess.SY AND robot",
    "cat:eess.IV AND robot",
    "cat:cs.AI AND robot",
    "cat:cs.LG AND robot perception",
    "cat:cs.RO AND active perception",
    "cat:cs.RO AND tactile",
    "cat:cs.RO AND manipulation",
    "cat:cs.RO AND planning",
    "cat:cs.RO AND control",
    "cat:cs.RO AND world model",
    "cat:cs.RO AND multimodal",
    "cat:cs.RO AND 3D perception",
    "cat:cs.RO AND visual servoing",
    "cat:cs.RO AND sensor",
    "cat:cs.RO AND uncertainty",
    "cat:cs.RO AND affordance",
    "cat:cs.RO AND exploration",
    "cat:cs.RO AND navigation",
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "codex-literature-sweep/1.0"})
    with urllib.request.urlopen(req, timeout=40) as resp:
        return resp.read()


def text(elem, path):
    found = elem.find(path)
    return "" if found is None or found.text is None else html.unescape(found.text.strip())


def parse_entry(entry):
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    title = text(entry, "{http://www.w3.org/2005/Atom}title")
    summary = text(entry, "{http://www.w3.org/2005/Atom}summary")
    published = text(entry, "{http://www.w3.org/2005/Atom}published")
    year = published[:4] if published else ""
    authors = ", ".join(
        a.findtext("{http://www.w3.org/2005/Atom}name", default="").strip()
        for a in entry.findall("{http://www.w3.org/2005/Atom}author")
        if a.findtext("{http://www.w3.org/2005/Atom}name", default="").strip()
    )
    links = entry.findall("{http://www.w3.org/2005/Atom}link")
    pdf = ""
    for link in links:
        if link.attrib.get("title") == "pdf":
            pdf = link.attrib.get("href", "")
            break
    arxiv_id = text(entry, "{http://www.w3.org/2005/Atom}id")
    doi = text(entry, "{http://arxiv.org/schemas/atom}doi")
    categories = ",".join(cat.attrib.get("term", "") for cat in entry.findall("{http://www.w3.org/2005/Atom}category"))
    return {
        "title": title,
        "year": year,
        "venue": "arXiv",
        "authors": authors,
        "doi": doi,
        "openalex_id": arxiv_id,
        "citation_count": 0,
        "query_seed": "",
        "type": "preprint",
        "abstract": summary.replace("\n", " "),
        "pdf": pdf,
        "categories": categories,
    }


def arxiv_search(query, start=0, max_results=100):
    base = "https://export.arxiv.org/api/query"
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "start": start,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
    )
    xml_bytes = fetch(f"{base}?{params}")
    root = ET.fromstring(xml_bytes)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    return root.findall("atom:entry", ns)


def normalize(s):
    return " ".join((s or "").lower().split())


def main():
    out = Path("docs/related_work_matrix.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = {}
    for qi, q in enumerate(ARXIV_QUERIES, 1):
        print(f"[{qi}/{len(ARXIV_QUERIES)}] querying {q}", file=sys.stderr)
        for page in range(0, 5):
            try:
                entries = arxiv_search(q, start=page * 100, max_results=100)
            except Exception as e:
                print(f"query failed {q} page {page}: {e}", file=sys.stderr)
                break
            if not entries:
                break
            for entry in entries:
                row = parse_entry(entry)
                key = normalize(row["title"])
                row["query_seed"] = q
                if key not in rows:
                    rows[key] = row
            time.sleep(0.5)
    ordered = sorted(rows.values(), key=lambda r: (r["query_seed"], r["title"]))
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["title", "year", "venue", "authors", "doi", "openalex_id", "citation_count", "query_seed", "type", "abstract", "pdf", "categories"],
        )
        writer.writeheader()
        for row in ordered:
            writer.writerow(row)
    print(f"wrote {len(ordered)} rows to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
