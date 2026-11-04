"""Record source HTTP reachability; this is not a content endorsement."""
import json,subprocess,concurrent.futures
from pathlib import Path
R=Path(__file__).resolve().parents[1]
A=json.loads((R/'content/articles.json').read_text()); urls=sorted({s['url'] for a in A for s in a['sources']})
def check(url):
 p=subprocess.run(['curl','-L','-sS','--max-time','18','-o','/dev/null','-w','%{http_code} %{url_effective}',url],capture_output=True,text=True)
 status,_,final=p.stdout.partition(' ')
 return dict(url=url,status=status,final_url=final,checked_on='2026-11-04',note='HTTP reachability only; manually reviewed core references separately.')
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: rows=list(pool.map(check,urls))
(R/'content/source-checks.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('Checked:',len(rows));print('\n'.join(str(r['status'])+' '+r['url'] for r in rows if r['status']!='200'))
