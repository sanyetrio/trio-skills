#!/usr/bin/env python3
"""Local stage ledger. Does not run models, collect content, or publish."""
import argparse, hashlib, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

STAGES=['selection','breakdown','knowledge','script','storyboard','review']
DIRS=['inputs','selection','breakdowns','knowledge','script','storyboard','review']

def stamp(): return datetime.now(timezone.utc).isoformat()
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
 return h.hexdigest()
def save(path,data):
 tmp=path.with_name(path.name+'.tmp')
 with tmp.open('w',encoding='utf-8') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
 os.replace(tmp,path)
def read(root):
 p=root/'task.json'
 j=json.loads(p.read_text())
 if j.get('schema_version')!=1:raise ValueError('不支持的task.json版本')
 return j

def file_entry(root,name):
 p=Path(name);p=p if p.is_absolute() else root/p;p=p.resolve()
 if not p.is_file() or not p.stat().st_size:raise ValueError(f'文件不存在或为空: {p}')
 try:label=str(p.relative_to(root))
 except ValueError:label=str(p)
 return {'path':label,'sha256':digest(p),'bytes':p.stat().st_size}

def scoped(j):return STAGES[STAGES.index(j['start_stage']):STAGES.index(j['end_stage'])+1]
def assess(root,j):
 result={};active=scoped(j)
 for s in STAGES:
  st=j['stages'][s];issues=[]
  if s not in active:result[s]={'status':'out_of_scope','issues':[]};continue
  for f in st.get('artifacts',[])+st.get('inputs',[]):
   p=Path(f['path']);p=p if p.is_absolute() else root/p
   if not p.is_file():issues.append('文件缺失: '+f['path'])
   elif digest(p)!=f['sha256']:issues.append('文件已变更: '+f['path'])
  up=st.get('upstream')
  if up:
   if j['stages'][up['stage']]['revision']!=up['revision']:issues.append('上游版本已变更: '+up['stage'])
   if result.get(up['stage'],{}).get('status')!='ready':issues.append('上游当前未就绪: '+up['stage'])
  state='stale' if issues and st['status'] in ['ready','partial'] else st['status']
  result[s]={'status':state,'recorded_status':st['status'],'revision':st['revision'],'issues':issues,'note':st.get('note',''),'artifacts':st.get('artifacts',[])}
 return result

def main():
 ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='command',required=True)
 p=sub.add_parser('init');p.add_argument('--root',required=True);p.add_argument('--task-id',required=True);p.add_argument('--ip',required=True);p.add_argument('--scope',required=True);p.add_argument('--start-stage',choices=STAGES,default='selection');p.add_argument('--end-stage',choices=STAGES,default='review')
 p=sub.add_parser('status');p.add_argument('--root',required=True)
 p=sub.add_parser('record');p.add_argument('--root',required=True);p.add_argument('--stage',choices=STAGES,required=True);p.add_argument('--status',choices=['running','partial','blocked','ready'],required=True);p.add_argument('--artifact',action='append',default=[]);p.add_argument('--input',action='append',default=[]);p.add_argument('--note',required=True)
 a=ap.parse_args();root=Path(a.root).expanduser().resolve()
 if a.command=='init':
  if STAGES.index(a.start_stage)>STAGES.index(a.end_stage):raise ValueError('起始阶段不能在结束阶段之后')
  if (root/'task.json').exists():raise ValueError('task.json已存在，请status后续接；未覆盖')
  root.mkdir(parents=True,exist_ok=True)
  for d in DIRS:(root/d).mkdir(exist_ok=True)
  j={'schema_version':1,'task_id':a.task_id,'target_ip':a.ip,'scope':a.scope,'start_stage':a.start_stage,'end_stage':a.end_stage,'created_at':stamp(),'updated_at':stamp(),'stages':{s:{'status':'not_started','revision':0,'artifacts':[],'inputs':[],'upstream':None,'note':''} for s in STAGES},'history':[]}
  save(root/'task.json',j);print(json.dumps({'created':str(root/'task.json'),'stages':scoped(j)},ensure_ascii=False));return
 j=read(root)
 if a.command=='status':
  states=assess(root,j);complete=all(states[s]['status']=='ready' for s in scoped(j));print(json.dumps({'task_id':j['task_id'],'stages':states,'requested_stages_ready':complete,'meaning':'仅阶段产物检查状态，不代表用户确认或发布'},ensure_ascii=False,indent=2));return
 if a.stage not in scoped(j):raise ValueError('该阶段不在本次任务范围内')
 if not a.note.strip():raise ValueError('必须填写实际检查说明或阻塞原因')
 artifacts=[file_entry(root,f) for f in a.artifact];inputs=[file_entry(root,f) for f in a.input]
 active=scoped(j);pos=active.index(a.stage);prev=active[pos-1] if pos else None
 if a.status=='ready':
  if not artifacts:raise ValueError('ready必须登记至少一个实际非空产物')
  if prev and assess(root,j)[prev]['status']!='ready':raise ValueError('上一阶段未就绪或已过期，不能伪报ready')
  if not prev and not inputs:raise ValueError('起始阶段ready须显式登记实际输入 --input')
 old=j['stages'][a.stage];revision=old['revision']+1
 j['history'].append({'at':stamp(),'stage':a.stage,'previous':old})
 j['stages'][a.stage]={'status':a.status,'revision':revision,'artifacts':artifacts,'inputs':inputs,'upstream':{'stage':prev,'revision':j['stages'][prev]['revision']} if prev else None,'note':a.note,'checked_at':stamp()}
 j['updated_at']=stamp();save(root/'task.json',j);print(json.dumps({'stage':a.stage,'status':a.status,'revision':revision,'task':str(root/'task.json')},ensure_ascii=False))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,KeyError,json.JSONDecodeError) as exc:print(json.dumps({'error':str(exc)},ensure_ascii=False),file=sys.stderr);sys.exit(2)
