# 拆片产物约定

机器可读模板以 [breakdown-template.json](../assets/breakdown-template.json) 为唯一字段样例。本文只说明含义。独立使用时输出 `breakdowns/{source_id}.json` 与同名 `.md`，证据位于 `evidence/{source_id}/`；也可沿用用户指定项目结构。与主控配合时再读 `ip-content-sop/references/handoff.md`。

- `stage` 固定 `breakdown`。`status` 为 `needs_input` 或 `ready`。`ready` 只表示完整拆片阶段验收通过，不表示知识库已写入、IP 已采用或视频已发布。
- `media_path`、`transcript_ref` 保留真实来源；`media_sha256` 来自原片，供后续核对。原片时长以真实探测为准。
- `coverage.video.ranges` 只写连续画面实际查看范围，元素用 `{"start": 起点秒, "end": 终点秒}`；仅看静帧用 `frame_refs`，`mode: frames_only`，不能填全片范围。`audio` 同理只记录实际听取范围；`transcript` 记录实际阅读范围。`reviewed` 表示至少观察过声明范围，不等于全片；完整性同时看范围和 mode。
- 无音轨：`audio.reviewed:false`、`mode:no_audio_stream`、`audio_stream_present:false`，附 `probe.json` 作为轨道证据；不要写“听过，确认静音”。有音轨但未听，声音相关字段保持 null。
- `evidence` 集中注册可打开的原片/图片/转写/观察记录，每项写 `id`、`kind`、`path`、`start`、`end`、`observation`；`segments[].evidence_refs` 和 `reusable_points[].evidence_refs` 引用这些编号。静帧起止可相同，文字原文无时间时起止为 null。观察记录包括时间范围、实际操作/工具、看听到的内容，不只有“已核实”。
- `segments` 以真实时间划分，覆盖全部原片，必要时无口播画面也单独成段。每段 `quote` 对应转写原文；无口播写空字符串并说明，未取得原文写 null。不要用分析替换原文。
- `camera` 与 `visual` 记录观察事实，`edit`、`audio` 记录可核实手法，`analysis` 单独解释作用。未知值为 null，并在 `missing` 记录影响；无此元素写明确“无”须有实际观察证据。
- 拆片 11 字段对应：`segment_id` 镜头号；`camera.scene/angle/movement` 场景/角度/状态；`visual.screenshot_refs` 截图；`visual.subtitle_text/subtitle_style/emphasis_text/animation` 字幕/样式/花字/动画；`audio.sfx` 音效；`end-start` 时长。另加文案、画面作用、剪辑、音乐与来源，便于脚本转用。
- `reusable_points` 每项用 `point_id`（如 `R01-P01`）、`method`、`evidence_refs`、`use_conditions`、`do_not_copy`，写手法、具体证据、适用条件、不能搬走的经历观点。此处先提参考点，当前 IP 是否适合由后续脚本步骤判断。

**完整交接检查**：字段已填不等于有证据；全片视听或无音轨证明、原文/无口播记录、段落时码、引用可打开、未解决缺口影响范围、分类标准、MD/JSON 一致都检查后，才能 `ready`。部分步骤完成就保留文件并写 `needs_input`，主控可以并行处理其他作品。
