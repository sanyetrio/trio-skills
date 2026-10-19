#!/usr/bin/env python3
"""Validate narration coverage and render planning tables; no model or cloud calls."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

ASSET_STATUSES = {'existing', 'to_capture', 'to_obtain', 'proposed_generation'}
EVIDENCE_KINDS = {'ip_fact', 'third_party_fact', 'reference_observation', 'source_method', 'creative_proposal', 'teaching'}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def ids(items, label, errors):
    if not isinstance(items, list):
        errors.append(f'{label} 必须是数组')
        return {}
    result = {}
    for i, item in enumerate(items):
        if not isinstance(item, dict) or not nonempty(item.get('id')):
            errors.append(f'{label}[{i}] 缺少有效 id')
            continue
        ident = item['id']
        if ident in result:
            errors.append(f'{label} 重复 id: {ident}')
        result[ident] = item
    return result


def validate(script, board):
    errors, warnings = [], []
    if not isinstance(script, dict) or not isinstance(board, dict):
        return {'valid': False, 'errors': ['script 与 board 必须为 JSON 对象'], 'warnings': []}
    for obj, label in [(script, 'script'), (board, 'board')]:
        if obj.get('schema_version') != '1.0':
            errors.append(f'{label}.schema_version 必须为 1.0')
        if not nonempty(obj.get('project_id')):
            errors.append(f'{label}.project_id 不可为空')
    for field in ['ip_id', 'script_version', 'title']:
        if not nonempty(script.get(field)):
            errors.append(f'script.{field} 不可为空')
    if script.get('status') not in ['draft', 'ready_for_storyboard']:
        errors.append('script.status 必须为 draft 或 ready_for_storyboard')
    if script.get('project_id') != board.get('project_id'):
        errors.append('项目不一致')
    if script.get('script_version') != board.get('source_script_version'):
        errors.append('稿件版本不一致，请重新对应当前稿件')
    mode = board.get('timing_basis')
    if mode not in ['estimated', 'aligned_audio']:
        errors.append('timing_basis 必须为 estimated 或 aligned_audio')
    if not nonempty(board.get('timing_note')):
        errors.append('timing_note 不可为空')
    if mode == 'aligned_audio':
        alignment = board.get('audio_alignment')
        if not isinstance(alignment, dict) or any(not nonempty(alignment.get(k)) for k in ['audio_uri', 'alignment_uri', 'method', 'checked_by']):
            errors.append('aligned_audio 缺实际音频、对齐结果、方法或核验者记录')
        warnings.append('音频对齐记录仅检查字段；听审与对齐准确性需实际音频验证。')
    else:
        warnings.append('全部新时间为估算；尚未实际口播对齐。')
    evidence = ids(script.get('evidence'), 'evidence', errors)
    for eid, item in evidence.items():
        if item.get('kind') not in EVIDENCE_KINDS:
            errors.append(f'{eid}: evidence.kind 不在支持范围')
        for field in ['source_uri', 'locator', 'summary', 'ownership']:
            if not nonempty(item.get(field)):
                errors.append(f'{eid}: 缺 {field}')
        if 'source_start_s' in item or 'source_end_s' in item:
            a,b=item.get('source_start_s'),item.get('source_end_s')
            if not finite(a) or not finite(b) or a < 0 or b <= a:
                errors.append(f'{eid}: 原片起止时间无效')
    segments = ids(script.get('segments'), 'segments', errors)
    shots = ids(board.get('shots'), 'shots', errors)
    assets = ids(board.get('assets'), 'assets', errors)
    if not segments:
        errors.append('口播段落不可为空')
    if not shots:
        errors.append('镜头不可为空')

    def check_refs(value, label):
        if not isinstance(value, list) or any(not isinstance(r, str) for r in value):
            errors.append(f'{label}: source_refs 必须是来源ID字符串数组')
        else:
            for ref in value:
                if ref not in evidence:
                    errors.append(f'{label}: 来源不存在 {ref}')

    total_chars = 0
    for sid, seg in segments.items():
        if not nonempty(seg.get('text')):
            errors.append(f'{sid}: text 不可为空')
        else:
            total_chars += len(seg['text'])
        check_refs(seg.get('source_refs'), sid)
    cursor_by_segment = {sid: 0 for sid in segments}
    order = list(segments)
    expected_segment_index = 0
    previous_end = 0
    used_assets = set()
    mapped_chars = 0
    for shot_id, shot in shots.items():
        start, end = shot.get('new_start_s'), shot.get('new_end_s')
        if not finite(start) or not finite(end) or start < 0 or end <= start:
            errors.append(f'{shot_id}: 新稿起止时间无效')
        else:
            if not math.isclose(start, previous_end, abs_tol=0.001):
                errors.append(f'{shot_id}: 时间不连续，期望从 {previous_end:g} 秒开始')
            previous_end = end
        for field in ['framing','visual','edit','audio','fallback']:
            if not nonempty(shot.get(field)):
                errors.append(f'{shot_id}: 缺 {field}')
        if not isinstance(shot.get('on_screen_text'), str):
            errors.append(f'{shot_id}: on_screen_text 必须为字符串，可留空')
        check_refs(shot.get('source_refs'), shot_id)
        asset_refs = shot.get('asset_ids')
        if not isinstance(asset_refs, list) or not asset_refs or any(not isinstance(a,str) for a in asset_refs):
            errors.append(f'{shot_id}: asset_ids 必须至少包含一个素材ID')
        else:
            for asset_id in asset_refs:
                if asset_id not in assets:
                    errors.append(f'{shot_id}: 素材不存在 {asset_id}')
                used_assets.add(asset_id)
        parts = shot.get('narration_parts')
        if not isinstance(parts, list):
            errors.append(f'{shot_id}: narration_parts 必须为数组，无口播时写 []')
            continue
        for part in parts:
            if not isinstance(part, dict):
                errors.append(f'{shot_id}: 口播映射必须为对象')
                continue
            sid, a, b, text = (part.get(k) for k in ['segment_id','start_char','end_char','text'])
            if not isinstance(sid,str) or sid not in segments:
                errors.append(f'{shot_id}: 未知口播段落 {sid}')
                continue
            src = segments[sid].get('text')
            if not isinstance(src,str):
                continue
            if type(a) is not int or type(b) is not int or a < 0 or b <= a or b > len(src):
                errors.append(f'{shot_id}/{sid}: 字符区间无效')
                continue
            if not isinstance(text,str) or text != src[a:b]:
                errors.append(f'{shot_id}/{sid}: 口播与原稿字符区间不一致')
            if a != cursor_by_segment[sid]:
                errors.append(f'{shot_id}/{sid}: 漏字、重复或顺序错误，期望 start_char={cursor_by_segment[sid]}，实际 {a}')
            while expected_segment_index < len(order):
                current = order[expected_segment_index]
                current_text = segments[current].get('text')
                if not isinstance(current_text,str) or cursor_by_segment[current] < len(current_text):
                    break
                expected_segment_index += 1
            if expected_segment_index >= len(order) or sid != order[expected_segment_index]:
                errors.append(f'{shot_id}/{sid}: 段落顺序错误或重复映射')
            cursor_by_segment[sid] = b
            mapped_chars += b-a
    for sid, seg in segments.items():
        if isinstance(seg.get('text'), str) and cursor_by_segment[sid] != len(seg['text']):
            errors.append(f'{sid}: 口播未完整覆盖，结束于 {cursor_by_segment[sid]} / {len(seg["text"])}')
    for aid, asset in assets.items():
        if asset.get('status') not in ASSET_STATUSES:
            errors.append(f'{aid}: 素材状态无效')
        for field in ['name','owner','action','fallback']:
            if not nonempty(asset.get(field)):
                errors.append(f'{aid}: 缺 {field}')
        if asset.get('status') == 'existing' and not nonempty(asset.get('location')):
            errors.append(f'{aid}: 已有素材缺实际位置')
        location = asset.get('location','')
        if asset.get('status') == 'existing' and isinstance(location,str) and location.startswith('/') and not Path(location).exists():
            errors.append(f'{aid}: 已有本地素材不存在 {location}')
        if aid not in used_assets:
            warnings.append(f'{aid}: 清单中存在但当前镜头未引用')
    warnings.append('本检查不证明来源真实、引用正确、素材获准使用、内容适合该IP或画面可拍；需执行者逐项复核。')
    return {
        'valid': not errors, 'errors': errors, 'warnings': warnings,
        'segments': len(segments), 'shots': len(shots), 'script_chars': total_chars,
        'mapped_chars': mapped_chars, 'planned_duration_s': previous_end,
        'time_basis': mode, 'assets': len(assets),
        'source_verification': 'not_performed_by_validator',
        'semantic_and_shootability_review': 'not_performed_by_validator',
    }


def cell(value):
    return str(value).replace('|','\\|').replace('\n','<br>')


def render(script, board, report, output, overwrite):
    output.mkdir(parents=True, exist_ok=True)
    destinations = [output/'storyboard.md', output/'assets-needed.csv', output/'validation.json']
    if not overwrite and any(p.exists() for p in destinations):
        raise ValueError('目标文件已存在；先读现有改动，再按需选择新目录或 --overwrite。')
    lines = [f'# {script["title"]}｜分镜与拍摄清单', '',
             f'稿件版本：{script["script_version"]}；时间依据：{board["timing_basis"]}。', '',
             board['timing_note'], '',
             '本表为拍摄计划；生成分镜不代表已拍摄、已生图、已配音或已渲染。', '',
             '| 镜头/新稿时间 | 口播原句 | 镜头与画面 | 剪辑/字幕/声音 | 素材/来源/替代 |',
             '|---|---|---|---|---|']
    shot_usage = {a['id']:[] for a in board['assets']}
    for shot in board['shots']:
        for aid in shot['asset_ids']:
            shot_usage[aid].append(shot['id'])
        narration=''.join(p['text'] for p in shot['narration_parts']) or '（无口播）'
        row = [f'{shot["id"]} / {shot["new_start_s"]:g}–{shot["new_end_s"]:g}秒', narration,
               shot['framing']+'；'+shot['visual'],
               '剪辑：'+shot['edit']+'；上屏：'+(shot['on_screen_text'] or '无额外文字')+'；声音：'+shot['audio'],
               '素材：'+','.join(shot['asset_ids'])+'；来源：'+','.join(shot['source_refs'])+'；替代：'+shot['fallback']]
        lines.append('| '+' | '.join(cell(v) for v in row)+' |')
    lines += ['', '## 素材准备', '', '| 编号/名称 | 状态/实际位置 | 用在哪些镜头 | 准备动作/负责人与替代 |', '|---|---|---|---|']
    status={'existing':'已有','to_capture':'待拍','to_obtain':'待取得','proposed_generation':'拟生成，尚未执行'}
    csv_rows=[]
    for asset in board['assets']:
        usage=','.join(shot_usage[asset['id']])
        lines.append('| '+' | '.join(cell(v) for v in [asset['id']+'/'+asset['name'], status[asset['status']]+' / '+asset.get('location','待准备'),usage,asset['action']+'；负责人：'+asset['owner']+'；替代：'+asset['fallback']])+' |')
        csv_rows.append({**asset,'shot_ids':usage})
    lines += ['', '## 来源与原片定位', '', '下列定位属于原资料；不得用作新片时间轴。', '', '| 来源ID/类型 | 来源入口与定位 | 支持内容/归属 |', '|---|---|---|']
    for ev in script['evidence']:
        lines.append('| '+' | '.join(cell(v) for v in [ev['id']+'/'+ev['kind'],ev['source_uri']+'；'+ev['locator'],ev['summary']+'；'+ev['ownership']])+' |')
    lines += ['', '## 验证范围', '', f'结构校验通过：{report["script_chars"]} 个原稿字符按序覆盖，{report["shots"]} 个镜头，{report["assets"]} 项素材。']
    lines += ['- '+w for w in report['warnings']]
    destinations[0].write_text('\n'.join(lines)+'\n',encoding='utf-8')
    with destinations[1].open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['id','name','status','location','owner','action','fallback','shot_ids'],extrasaction='ignore')
        writer.writeheader(); writer.writerows(csv_rows)
    destinations[2].write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return [str(p) for p in destinations]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['validate','render'])
    parser.add_argument('--script',required=True,type=Path)
    parser.add_argument('--board',required=True,type=Path)
    parser.add_argument('--out',type=Path)
    parser.add_argument('--overwrite',action='store_true')
    args=parser.parse_args()
    try:
        script=json.loads(args.script.read_text(encoding='utf-8'))
        board=json.loads(args.board.read_text(encoding='utf-8'))
        report=validate(script,board)
        report['script_sha256']=hashlib.sha256(args.script.read_bytes()).hexdigest()
        report['storyboard_sha256']=hashlib.sha256(args.board.read_bytes()).hexdigest()
        if report['valid'] and args.command=='render':
            if args.out is None:
                raise ValueError('render 必须提供 --out')
            report['outputs']=render(script,board,report,args.out,args.overwrite)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return 0 if report['valid'] else 1
    except (OSError,ValueError,TypeError,KeyError) as exc:
        print(json.dumps({'valid':False,'errors':[str(exc)]},ensure_ascii=False,indent=2))
        return 2

if __name__=='__main__':
    sys.exit(main())
