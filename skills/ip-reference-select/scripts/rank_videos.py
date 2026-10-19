#!/usr/bin/env python3
"""Rank supplied CSV only; no collection or platform inference."""
import argparse,csv,hashlib,json,re,sys
from datetime import datetime
from decimal import Decimal,InvalidOperation
from pathlib import Path

METRICS=['plays','likes','comments','favorites','shares']
def number(v):
 s=str(v or '').strip().replace(',','')
 if s in ('','-','—','未知','未取得','null','None'):return None,False
 m=re.fullmatch(r'(\d+(?:\.\d+)?)\s*([万亿千wWkK]?)',s)
 if not m:raise ValueError('数值无法精确解释（区间、加号需先回源核对）: '+s)
 n=Decimal(m[1])*{'':1,'万':10000,'亿':100000000,'千':1000,'w':10000,'W':10000,'k':1000,'K':1000}[m[2]]
 if n!=n.to_integral_value():raise ValueError('计数不能有小数: '+s)
 return int(n),bool(m[2])
def date(s,field):
 try:datetime.fromisoformat(s.replace('Z','+00:00'))
 except (ValueError,AttributeError):raise ValueError(f'{field}必须为ISO日期/日期时间，得到 {s!r}')
def write_csv(path,rows,fields):
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input',required=True);ap.add_argument('--out',required=True);ap.add_argument('--account',required=True);ap.add_argument('--metric',choices=METRICS,required=True);ap.add_argument('--count',type=int,default=10);ap.add_argument('--scope',required=True,help='如本次已取得作品、发布时间范围与遗漏范围');a=ap.parse_args()
 if a.count<1:raise ValueError('count必须大于0')
 p=Path(a.input);out=Path(a.out)
 if out.exists() and any(out.iterdir()):raise ValueError('输出目录非空，请使用新的版本目录；未覆盖')
 with p.open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f);fields=reader.fieldnames or [];rows=list(reader)
 needed=['video_id','author','title','url','observed_at',a.metric]
 if any(k not in fields for k in needed):raise ValueError('缺少字段: '+','.join(k for k in needed if k not in fields))
 seen=set();seen_urls=set();usable=[];excluded=[];warnings=[]
 for row_no,r in enumerate(rows,2):
  rid=r['video_id'].strip();url=r['url'].strip()
  if not rid or not url or not r['title'].strip():raise ValueError(f'第{row_no}行缺少ID、标题或来源')
  if rid in seen or url in seen_urls:raise ValueError(f'第{row_no}行重复ID/来源，先核对重复与日期再运行: {rid}')
  seen.add(rid);seen_urls.add(url)
  if r['author'].strip()!=a.account:raise ValueError(f'第{row_no}行不属于指定账号: {r["author"]}')
  date(r['observed_at'].strip(),'observed_at')
  if r.get('published_at','').strip():date(r['published_at'].strip(),'published_at')
  try:value,approx=number(r[a.metric])
  except ValueError as exc:excluded.append({**r,'reason':str(exc)});continue
  if value is None:excluded.append({**r,'reason':'主指标未取得，未按0处理'});continue
  r={**r,'metric_value':value,'approximate':approx}
  usable.append(r)
 usable.sort(key=lambda r:(-r['metric_value'],r['video_id']))
 for i,r in enumerate(usable,1):r['rank']=i;r['selected']='yes' if i<=a.count else 'no'
 chosen=usable[:a.count]
 if len(chosen)<a.count:warnings.append(f'有效记录仅{len(chosen)}条，未凑足{a.count}条')
 if excluded:warnings.append('主指标缺失或无法解释的作品未参与排序，不能声称全范围真实前N')
 if any(r['approximate'] for r in usable):warnings.append('含平台缩写/舍入数值，仅按显示值排序；临界或并列名次回源核对')
 if len(usable)>a.count and usable[a.count-1]['metric_value']==usable[a.count]['metric_value']:warnings.append('第N名存在同分作品；当前按作品ID稳定排序，最终取舍需写明理由')
 observed=sorted(set(r['observed_at'] for r in rows))
 if len(set(v[:10] for v in observed))>1:warnings.append('数据记录日期跨日，比较前确认是否需要刷新同一快照')
 report={'schema_version':1,'source_csv':str(p.resolve()),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'account':a.account,'scope':a.scope,'metric':a.metric,'requested_count':a.count,'input_count':len(rows),'rankable_count':len(usable),'selected_count':len(chosen),'excluded_count':len(excluded),'observed_at_values':observed,'tie_break':'作品ID升序，只为稳定展示；不据此断言热度更高','status':'partial' if warnings else 'ready_for_review','warnings':warnings,'selected':chosen,'excluded':excluded}
 out.mkdir(parents=True,exist_ok=True);common=['rank','selected',*fields,'metric_value','approximate'];write_csv(out/'ranked.csv',usable,common);write_csv(out/'top.csv',chosen,common);write_csv(out/'excluded.csv',excluded,[*fields,'reason']);(out/'selection.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['input_count','selected_count','excluded_count','status','warnings']},ensure_ascii=False))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,InvalidOperation,csv.Error) as exc:print(json.dumps({'error':str(exc)},ensure_ascii=False),file=sys.stderr);sys.exit(2)
