# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=1.9,<2", "httpx>=0.27"]
# ///
"""A small MCP server: it lets the agent search PubMed and read abstracts, through NCBI's public E-utilities.
OpenCode starts it (see opencode.json); its two tools show up as pubmed_search and pubmed_abstract.
No key needed. NCBI allows 3 requests a second without one; set NCBI_API_KEY for more."""
import os
import re
import time

import httpx
from mcp.server.fastmcp import FastMCP

EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
mcp = FastMCP('pubmed')


def eutils(tool, **params):
    params |= {'db': 'pubmed', 'tool': 'egfr-lab'}   # NCBI asks callers to name their tool
    if os.environ.get('NCBI_API_KEY'):
        params['api_key'] = os.environ['NCBI_API_KEY']
    for attempt in range(4):
        r = httpx.get(EUTILS + tool + '.fcgi', params=params, timeout=30)
        if r.status_code == 429 and attempt < 3:      # too many requests: wait, then try again
            time.sleep(1 + attempt)
            continue
        r.raise_for_status()
        return r


SKIP = {'study', 'studies', 'paper', 'article', 'linked', 'link', 'later', 'over', 'with', 'that', 'this', 'from', 'into',
        'years', 'year', 'month', 'months', 'two', 'three', 'risk', 'find', 'about', 'which', 'their', 'between'}


def plain(query):
    """What PubMed reads best: eGFR spelled out (otherwise it finds the EGFR gene), no quotes or %."""
    return re.sub(r'\begfr\b', 'glomerular filtration rate', query, flags=re.I).replace('"', ' ').replace('%', ' ')


def content(query):
    """A failed query cut down to its content words, with any year as a publication-date filter."""
    words = re.findall(r"[A-Za-z][A-Za-z-]+|\d{4}", query)
    years = [w for w in words if re.fullmatch(r'(19|20)\d\d', w)]
    keep = [w for w in words if len(w) > 3 and w.lower() not in SKIP and w not in years]
    return ' '.join(keep[:6] + [f'{y}[dp]' for y in years[:1]])


@mcp.tool()
def search(query: str, max_results: int = 5) -> list[dict]:
    """Search PubMed. Returns up to max_results articles, most relevant first: PMID, title, first author, journal, year.
    Plain words work best; add a year or an author's surname to narrow it down."""
    tried = [plain(query)]
    tried.append(content(tried[0]))
    for term in tried:   # if the whole query finds nothing, try again with just its content words
        hits = eutils('esearch', term=term, retmode='json', retmax=min(max_results, 20), sort='relevance').json()['esearchresult']
        ids = hits['idlist']
        if ids:
            break
    if not ids:   # say why, so the agent can try again
        return [{'note': 'No results, even as: ' + tried[-1] + '. Try fewer, plainer words.'}]
    found = eutils('esummary', id=','.join(ids), retmode='json').json()['result']
    return [{'pmid': i, 'title': found[i]['title'], 'first_author': (found[i]['authors'] or [{'name': ''}])[0]['name'],
             'journal': found[i]['source'], 'year': found[i]['pubdate'][:4]} for i in ids if i in found]


@mcp.tool()
def abstract(pmid: str) -> str:
    """Title, authors and abstract of one PubMed article, by its PMID."""
    return eutils('efetch', id=pmid, rettype='abstract', retmode='text').text.strip()[:6000]


if __name__ == '__main__':
    mcp.run()
