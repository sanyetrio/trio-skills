# 分镜与素材格式

输入稿至少包含 `schema_version="1.0"`、`project_id`、`ip_id`、`script_version`、`title`、`status`、`evidence`、`segments`。`segments` 每项是 `{id, text, source_refs}`；证据每项是 `{id, kind, source_uri, locator, summary, ownership}`。外部稿件按这个最小结构整理，保留原文，不强制调用写稿技能。

`script.status` 只接受 `draft` 或 `ready_for_storyboard`。用户已经给定且要求保留的稿件，在核对输入完整后可记为 `ready_for_storyboard`；用户给定/锁定原文是本次任务约束，在任务说明中记录，不另造 `user_supplied_locked` 等状态。两个允许值都不表示用户批准发布。

分镜 JSON：

```json
{
  "schema_version": "1.0",
  "project_id": "project-001",
  "source_script_version": "v1",
  "timing_basis": "estimated",
  "timing_note": "逐段估时，待真人实读校准。",
  "shots": [
    {
      "id": "S01",
      "new_start_s": 0,
      "new_end_s": 4,
      "narration_parts": [
        {"segment_id": "P01", "start_char": 0, "end_char": 8, "text": "示例口播文字。"}
      ],
      "framing": "正面平视近景，固定机位",
      "visual": "人物看镜头，说完问题后停半拍。",
      "edit": "问题完整说完再切；不截断尾音。",
      "on_screen_text": "本镜头上屏文字",
      "audio": "保留原声，不另加音乐。",
      "asset_ids": ["A01"],
      "source_refs": ["T01"],
      "fallback": "无法拍近景时用固定中景。"
    }
  ],
  "assets": [
    {"id": "A01", "name": "人物主机位", "status": "to_capture", "location": "待拍", "owner": "本次拍摄者", "action": "拍全稿并补录近景。", "fallback": "固定中景"}
  ]
}
```

上例仅展示字段，字符区间需按实际段落计算。完整可运行例见 assets/teaching/。

- 新片时间使用秒；第一镜从0开始，相邻镜头首尾相接且结束大于开始。时间值为预估时只能用于拍摄计划。
- `narration_parts` 从原段落按Python字符串的 `[start_char:end_char]` 切片，起点含、终点不含；不能漏标点/文字。允许无口播镜头 `[]`，但其余镜头仍必须完整按顺序覆盖全部口播。
- 素材 `status`：`existing` / `to_capture` / `to_obtain` / `proposed_generation`。`existing` 必填 `location`；本地文件可继续核查实际存在，URL存在不等于授权、下载或播放已验证。
- `shots[].asset_ids` 必须列出本镜头实际使用的**画面和声音全部素材**，不只列可见画面。例：录屏A02上继续播放主机位A01的口播，填写 `["A01", "A02"]`；连续口播覆盖全部镜头时，A01应在每镜列出，素材CSV才能准确汇总使用位置。`audio`再写具体保留、静音和切入方式。
- 每镜引用 `source_refs` 必须在 script.evidence 中存在。纯新设计可创建 `creative_proposal`；教学演示可创建 `teaching`，均不能标为真实观察。
- `timing_basis=aligned_audio` 时必须有 `audio_alignment={audio_uri,alignment_uri,method,checked_by}`。只有实际执行了对齐与核验才能填写；本地脚本只检查字段，无法证明听审正确。缺音频不能改标签冒充精准对齐。
- `assets` 包含每一项镜头资源；共享素材可被多镜头引用，CSV汇总关联镜头。未用的资源仅报提示，避免错误删除本来准备的素材。
- 校验失败时不生成可交付表，先修复数据；缺实际素材不算数据错误，但清单中必须留下缺口和替代。

验收含两层：本地工具验证结构；当前执行者复核语义、事实与拍摄可行性。两者不能互相替代。
