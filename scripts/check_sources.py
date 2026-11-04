"""Record HTTP reachability separately from editorial verification of concepts."""
import concurrent.futures
import json
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo

from catalog import ROOT, load_articles

DEST = ROOT / 'content' / 'source-checks.json'
old = {row['url']: row for row in json.loads(DEST.read_text())} if DEST.exists() else {}
urls = sorted({s['url'] for a in load_articles() for s in a['sources']})
today = datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m-%d')

def check(url):
    if url in old:
        return old[url]
    proc = subprocess.run(
        ['curl', '-L', '-sS', '--max-time', '18', '-o', '/dev/null',
         '-w', '%{http_code} %{url_effective}', url], capture_output=True, text=True)
    status, _, final = proc.stdout.partition(' ')
    if status == '200':
        note = 'HTTP reachability only; not a review of every claim on this page.'
    elif status == '000':
        note = 'Execution network could not reach this URL; validity remains unconfirmed by curl.'
    else:
        note = 'Non-200 automatic request; review separately before declaring a broken source.'
    return dict(url=url, status=status, final_url=final, checked_on=today, note=note)

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    rows = list(pool.map(check, urls))
DEST.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
print(f'Recorded {len(rows)} URLs; {sum(r["status"] == "200" for r in rows)} returned HTTP 200.')
for row in rows:
    if row['status'] != '200':
        print(row['status'], row['url'])
