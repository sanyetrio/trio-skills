# script → storyboard 交接格式

`script/script.json` 使用 UTF-8 JSON。实际文字与 `script.md` 的口播正文一致，标题和操作说明不属于口播段落。

```json
{
  "schema_version": "1.0",
  "project_id": "project-001",
  "ip_id": "current-ip",
  "script_version": "v1",
  "title": "本条标题",
  "status": "draft",
  "topic_selection_basis": "user_selected",
  "evidence": [
    {
      "id": "E01",
      "kind": "ip_fact",
      "source_uri": "原资料路径或链接",
      "locator": "段落、块ID或原片00:03–00:07",
      "summary": "该来源直接支持什么",
      "ownership": "本IP确认材料"
    }
  ],
  "segments": [
    {"id": "P01", "text": "这里放实际口播原句。", "source_refs": ["E01"]}
  ]
}
```

- `topic_selection_basis`：`user_selected` / `delegated_selection`；选择依据说明放 adaptation.md。只有候选时不生成正式 script.json。
- `evidence.kind`：`ip_fact` / `third_party_fact` / `reference_observation` / `source_method` / `creative_proposal` / `teaching`。ID在本项目中唯一；每段引用必须能在这里解析。创作过渡句可以没有事实引用，但应在适配说明区分其用途。
- `source_uri` 是可回查路径/URL；教学演示可使用 `teaching://`，必须明确是自制而非真实博主观察。`locator` 必须能定位，不使用含糊的“网上”。
- 原片时间写在证据条目 `source_start_s` / `source_end_s` 或 `locator`。它不是新稿镜头时间。证据没有时间码时说明段落定位，不补一个数字。
- `segments[].text` 按原稿保留标点。分镜以Python字符串字符索引 `[start_char:end_char]` 匹配口播，起点含、终点不含；换行与标点都算字符，不使用UTF-16字节索引。
- 同一句计划说两次，脚本中就写为两个不同ID的段落；分镜不得通过重复映射同一段来掩盖复读。
- 当前稿需要修改：更新 `script_version`，再重建或校正分镜。旧文件留在现有项目版本目录；不悄悄替换用户已审版本。

最小教学输入见 [script.teaching.json](../assets/script.teaching.json)。这些文字只说明格式，不代表用户本人身份。
