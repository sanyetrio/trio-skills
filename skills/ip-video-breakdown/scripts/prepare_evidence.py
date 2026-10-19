#!/usr/bin/env python3
"""Prepare local video evidence without claiming a human/model has reviewed it."""
import argparse
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys



def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def tool(name, override):
    if override:
        path = Path(override)
        if path.is_file() and os.access(path, os.X_OK):
            return str(path.resolve())
        raise ValueError(f'指定的 {name} 不可执行：{override}；未换用其他程序')
    candidates = [shutil.which(name)]
    candidates += [str(Path(prefix) / name) for prefix in
                   ('/opt/homebrew/bin', '/usr/local/bin', '/usr/bin')]
    for candidate in candidates:
        if candidate and Path(candidate).is_file() and os.access(candidate, os.X_OK):
            return str(Path(candidate).resolve())
    raise ValueError(f'找不到可执行的 {name}；用 --{name} 指定已安装程序。本脚本不会自动安装。')


def run(args):
    p = subprocess.run(args, capture_output=True, text=True, timeout=1800)
    if p.returncode:
        raise RuntimeError(f'{Path(args[0]).name} 失败：{p.stderr[-1200:]}')
    return p


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def seconds(value):
    if isinstance(value, bool):
        raise ValueError('时间不能是布尔值')
    n = float(value)
    if not math.isfinite(n):
        raise ValueError('时间必须是有限数字')
    return n


def transcript(path, duration):
    if path is None:
        return []
    raw = path.read_text(encoding='utf-8-sig')
    if path.suffix.lower() == '.json':
        data = json.loads(raw)
        rows = data if isinstance(data, list) else data.get('segments')
        if not isinstance(rows, list):
            raise ValueError('转写 JSON 需要数组或包含 segments 数组')
        rows = [{'start': seconds(r['start']), 'end': seconds(r['end']), 'text': r['text']} for r in rows]
    elif path.suffix.lower() == '.srt':
        raw = raw.replace('\r\n', '\n').replace('\r', '\n').strip()
        blocks = re.split(r'\n\s*\n', raw) if raw else []
        rows = []
        pattern = re.compile(r'^(\d{2,}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2,}):(\d{2}):(\d{2})[,.](\d{3})(?:\s.*)?$')
        for block in blocks:
            lines = block.splitlines()
            if lines and lines[0].strip().isdigit():
                lines = lines[1:]
            match = pattern.match(lines[0].strip()) if lines else None
            if not match or len(lines) < 2:
                raise ValueError('SRT 存在无法解析的段落；请修正，不会静默丢句')
            v = list(map(int, match.groups()))
            if any(v[i] >= 60 for i in [1, 2, 5, 6]):
                raise ValueError('SRT 分秒超出范围')
            rows.append({'start': v[0]*3600+v[1]*60+v[2]+v[3]/1000,
                         'end': v[4]*3600+v[5]*60+v[6]+v[7]/1000,
                         'text': '\n'.join(lines[1:])})
    else:
        raise ValueError('仅接受已有 .srt 或秒单位的 .json 转写；纯文本不能虚构时码')
    previous = -1
    for i, row in enumerate(rows):
        a, b = row['start'], row['end']
        if not (0 <= a < b <= duration + .001) or a < previous:
            raise ValueError(f'转写第 {i+1} 段时码越界或起点乱序，请核对原片与转写')
        if not isinstance(row['text'], str) or not row['text'].strip():
            raise ValueError(f'转写第 {i+1} 段文本为空')
        previous = a
    if not rows:
        raise ValueError('转写没有可用段落')
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--media', required=True, type=Path)
    p.add_argument('--source-id', required=True)
    p.add_argument('--transcript', type=Path)
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--interval', type=float, default=5, help='额外采样间隔秒数，默认5')
    p.add_argument('--threshold', type=float, default=.25, help='ffmpeg scene 候选阈值；不是语义镜头阈值')
    p.add_argument('--max-frames', type=int, default=120)
    p.add_argument('--extract-audio', action='store_true')
    p.add_argument('--ffmpeg')
    p.add_argument('--ffprobe')
    args = p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', args.source_id):
        raise ValueError('source-id 只允许英文字母、数字、下划线或短横线')
    if not math.isfinite(args.interval) or args.interval <= 0 or not math.isfinite(args.threshold) or not 0 < args.threshold <= 1 or not 1 <= args.max_frames <= 1000:
        raise ValueError('interval须大于0，threshold须在(0,1]，max-frames须为1至1000')
    media = args.media.resolve(strict=True)
    if not media.is_file():
        raise ValueError('media 必须是本地文件')
    trans = args.transcript.resolve(strict=True) if args.transcript else None
    out = args.out.resolve()
    if out.exists():
        raise ValueError('输出目录已存在；请换新目录，避免覆盖已有人工作业')
    ffmpeg, ffprobe = tool('ffmpeg', args.ffmpeg), tool('ffprobe', args.ffprobe)
    source_hash = digest(media)
    meta = json.loads(run([ffprobe, '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(media)]).stdout)
    video = next((s for s in meta['streams'] if s['codec_type'] == 'video'
                  and not s.get('disposition', {}).get('attached_pic')), None)
    audio = [s for s in meta['streams'] if s['codec_type'] == 'audio']
    if not video:
        raise ValueError('没有视频轨；请用音频/文字分析流程')
    duration = seconds(video.get('duration') or meta['format'].get('duration'))
    if duration <= 0:
        raise ValueError('无法确定正数时长')
    rows = transcript(trans, duration)
    transcript_hash = digest(trans) if trans else None
    if duration / args.interval > 100000:
        raise ValueError('额外采样点超过100000，请调大 interval；未生成部分结果')
    out.mkdir(parents=True)
    try:
        dump(out / 'probe.json', meta)
        scan = run([ffmpeg, '-hide_banner', '-nostdin', '-i', str(media), '-map', f'0:{video["index"]}', '-an', '-vf',
                    f'scale=320:-2,select=gt(scene\\,{args.threshold}),showinfo', '-vsync', '0', '-f', 'null', '-'])
        (out / 'scene-scan.log').write_text(scan.stderr, encoding='utf-8')
        cuts = sorted(set(round(float(x), 6) for x in re.findall(r'pts_time:([\d.eE+-]+)', scan.stderr)
                          if 0 < float(x) < duration))
        times = {0.0: {'start'}}
        for n in range(1, math.ceil(duration / args.interval)):
            times.setdefault(round(n * args.interval, 6), set()).add('interval')
        boundaries = [0.0, *cuts, duration]
        for a, b in zip(boundaries, boundaries[1:]):
            times.setdefault(round((a+b)/2, 6), set()).add('candidate_segment_midpoint')
        for c in cuts:
            times.setdefault(c, set()).add('candidate_change')
        points = sorted(times)
        all_count = len(points)
        if all_count > args.max_frames:
            if args.max_frames == 1:
                points = [points[0]]
            else:
                points = [points[round(i*(all_count-1)/(args.max_frames-1))] for i in range(args.max_frames)]
        frame_dir = out / 'frames'
        frame_dir.mkdir()
        frames = []
        for i, t in enumerate(points, 1):
            name = f'{args.source_id}_{i:04d}_{t:010.3f}.jpg'
            target = frame_dir / name
            run([ffmpeg, '-v', 'error', '-nostdin', '-ss', str(t), '-i', str(media), '-map', f'0:{video["index"]}',
                 '-frames:v', '1', '-vf', "scale='min(1280,iw)':-2", '-q:v', '2', str(target)])
            if not target.exists() or target.stat().st_size == 0:
                raise ValueError(f'{t}秒截图失败，未生成完成清单')
            frames.append({'id': f'{args.source_id}-F{i:04d}', 'requested_time_seconds': t,
                           'path': f'frames/{name}', 'reason': sorted(times[t]), 'reviewed': False})
        audio_path = None
        if args.extract_audio and audio:
            audio_path = 'audio.wav'
            run([ffmpeg, '-v', 'error', '-nostdin', '-i', str(media), '-map', '0:a:0',
                 '-vn', '-c:a', 'pcm_s16le', str(out / audio_path)])
            if (out / audio_path).stat().st_size <= 44:
                raise ValueError('音频代理为空，未生成完成清单')
        if digest(media) != source_hash:
            raise ValueError('准备期间原片发生变化，请保留当前结果为无效并重新准备')
        if trans and digest(trans) != transcript_hash:
            raise ValueError('准备期间转写发生变化，请核对后重新准备')
        warnings = ['本结果只准备候选证据，未观看视频、未听音频、未阅读核验转写。',
                    '颜色变化不一定是切镜；快速转场、相似画面切换、运动与字幕动画可能漏检。',
                    '截图记录请求时间，非逐帧测量值；不能据截图证明运镜、转场或动画时长。',
                    '完整转写已读取并解析仅表示机器处理，不代表人工或模型已理解。']
        if all_count > len(frames):
            warnings.append(f'候选截图{all_count}张，按上限均匀保留{len(frames)}张；未截图位置必须回看。')
        if len(audio) > 1:
            warnings.append('有多个音轨，导出仅第一音轨；其他音轨需按任务另行核对。')
        if len([s for s in meta['streams'] if s['codec_type'] == 'video']) > 1:
            warnings.append('有多个视频轨，仅准备首条非封面视频轨；其他视频轨需按任务另行核对。')
        coverage = {k: {'reviewed': False, 'ranges': [], 'observer': None, 'mode': None}
                    for k in ['video', 'audio', 'transcript']}
        manifest = {'schema_version': '1.0', 'source_id': args.source_id, 'status': 'prepared',
                    'media_path': str(media), 'media_sha256': source_hash, 'duration_seconds': duration,
                    'video_stream_index': video['index'],
                    'transcript_ref': str(trans) if trans else None, 'transcript_sha256': transcript_hash,
                    'has_audio_stream': bool(audio), 'audio_stream_count': len(audio), 'extracted_audio': audio_path,
                    'candidate_cut_seconds': cuts, 'frames': frames, 'transcript_segments': rows,
                    'coverage': coverage, 'warnings': warnings,
                    'settings': {'threshold': args.threshold, 'interval': args.interval, 'max_frames': args.max_frames},
                    'tools': {'ffmpeg': ffmpeg, 'ffprobe': ffprobe}}
        dump(out / 'evidence-manifest.json', manifest)
        cards = ''.join(f'<figure><img loading="lazy" src="{html.escape(f["path"], quote=True)}"><figcaption>{html.escape(f["id"])} · 请求 {f["requested_time_seconds"]:.3f}s · 未观察</figcaption></figure>' for f in frames)
        page = '<!doctype html><meta charset="utf-8"><title>候选画面｜未观察</title><style>body{font-family:system-ui;margin:24px;background:#f4f6fa}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}figure{margin:0;padding:12px;background:white}img{width:100%;height:230px;object-fit:contain}figcaption{padding-top:8px}</style>'
        page += '<h1>' + html.escape(args.source_id) + ' 候选画面</h1><p>这些截图尚未观察，不能代表已拆片。先看画面，再回原片复核动态和声音。</p><main>' + cards + '</main>'
        (out / 'index.html').write_text(page, encoding='utf-8')
        print(json.dumps({'status': 'prepared', 'manifest': str(out / 'evidence-manifest.json'),
                          'candidate_cuts': len(cuts), 'frames': len(frames), 'analysis_complete': False}, ensure_ascii=False))
    except Exception as e:
        dump(out / 'failure.json', {'status': 'failed', 'reason': str(e), 'analysis_complete': False})
        raise


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, RuntimeError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'status': 'failed', 'reason': str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
