#!/usr/bin/env python3
"""Offline smoke test using synthetic footage; never reads user media or credentials."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from prepare_evidence import tool


def invoke(args, ok=True):
    p = subprocess.run(args, capture_output=True, text=True, timeout=120)
    assert (p.returncode == 0) == ok, (p.returncode, p.stdout, p.stderr)
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True, help='必须不存在的隔离测试目录')
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    root = a.out.resolve()
    ffmpeg = tool('ffmpeg', None)
    media = root / 'synthetic red blue green.mp4'
    invoke([ffmpeg, '-v', 'error', '-nostdin', '-f', 'lavfi', '-i', 'color=c=red:s=320x180:r=25:d=2',
            '-f', 'lavfi', '-i', 'color=c=blue:s=320x180:r=25:d=2',
            '-f', 'lavfi', '-i', 'color=c=green:s=320x180:r=25:d=2',
            '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=16000:duration=6',
            '-filter_complex', '[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]',
            '-map', '[v]', '-map', '3:a', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', str(media)])
    source_sha = hashlib.sha256(media.read_bytes()).hexdigest()
    trans = root / 'synthetic.srt'
    trans.write_text('1\n00:00:00,000 --> 00:00:01,800\n合成测试字幕一，不代表真实口播。\n\n2\n00:00:02,000 --> 00:00:05,800\n合成测试字幕二。\n', encoding='utf-8')
    script = Path(__file__).with_name('prepare_evidence.py')
    base = [sys.executable, str(script), '--media', str(media), '--source-id', 'TEST01']
    first = root / 'evidence'
    invoke(base + ['--transcript', str(trans), '--out', str(first), '--interval', '1', '--extract-audio'])
    manifest = json.loads((first / 'evidence-manifest.json').read_text())
    assert all(not x['reviewed'] and x['ranges'] == [] for x in manifest['coverage'].values())
    assert manifest['status'] == 'prepared' and manifest['has_audio_stream']
    assert len(manifest['transcript_segments']) == 2
    assert all(any(abs(v - t) < .1 for v in manifest['candidate_cut_seconds']) for t in [2, 4])
    assert (first / 'audio.wav').stat().st_size > 1000
    assert all((first / f['path']).stat().st_size > 0 and not f['reviewed'] for f in manifest['frames'])
    assert hashlib.sha256(media.read_bytes()).hexdigest() == source_sha
    before = (first / 'evidence-manifest.json').read_bytes()
    invoke(base + ['--out', str(first)], ok=False)
    assert (first / 'evidence-manifest.json').read_bytes() == before
    capped = root / 'capped'
    invoke(base + ['--out', str(capped), '--interval', '0.1', '--max-frames', '2'])
    cap = json.loads((capped / 'evidence-manifest.json').read_text())
    assert len(cap['frames']) == 2 and any('均匀保留' in x for x in cap['warnings'])
    broken = root / 'bad.json'
    broken.write_text('[{"start":0,"end":999,"text":"越界"}]', encoding='utf-8')
    invoke(base + ['--out', str(root / 'rejected'), '--transcript', str(broken)], ok=False)
    assert not (root / 'rejected').exists()
    malformed = root / 'malformed.srt'
    malformed.write_text('1\nnot timestamps\nshould fail\n', encoding='utf-8')
    invoke(base + ['--out', str(root / 'rejected_srt'), '--transcript', str(malformed)], ok=False)
    assert not (root / 'rejected_srt').exists()
    invoke(base + ['--out', str(root / 'bad_explicit_tool'), '--ffmpeg', str(root / 'not-installed')], ok=False)
    assert not (root / 'bad_explicit_tool').exists()
    mute = root / 'no-audio.mp4'
    invoke([ffmpeg, '-v', 'error', '-nostdin', '-i', str(media), '-map', '0:v:0', '-c', 'copy', str(mute)])
    noaudio = root / 'no-audio-evidence'
    invoke([sys.executable, str(script), '--media', str(mute), '--source-id', 'TEST02',
            '--out', str(noaudio), '--extract-audio'])
    silent = json.loads((noaudio / 'evidence-manifest.json').read_text())
    assert not silent['has_audio_stream'] and silent['extracted_audio'] is None
    assert not (noaudio / 'audio.wav').exists() and not silent['coverage']['audio']['reviewed']
    report = {'result': 'pass', 'source': '6秒红蓝绿合成视频＋440Hz合成正弦音，非真实博主素材',
              'candidate_cut_seconds': manifest['candidate_cut_seconds'], 'frames': len(manifest['frames']),
              'checks': ['合成切点2s/4s进入候选', 'SRT完整读取两段', '源片前后哈希不变',
                         '候选截图真实存在', '全部看听读覆盖仍为未审', '听审音频成功导出但未声称听过',
                         '重复运行不覆盖原结果', '截图上限明确披露', '越界JSON拒绝', '损坏SRT拒绝',
                         '指定工具不可用时不静默改用其他工具', '无音轨不造音频、不假称听审'],
              'not_validated': ['真实博主视频拆片', '语义理解准确性', '连续动态观看', '真实声音听审', '知识库写入']}
    (root / '测试结果.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
