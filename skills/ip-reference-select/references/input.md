# CSV输入约定

读取原导出字段后由AI做明确映射，不通过猜测把收藏/点赞/分享混成同一指标。保留原CSV和一份字段映射说明。

必需列为 `video_id,author,title,url,observed_at` 加所选指标。指标为 `plays,likes,comments,favorites,shares` 之一。可选列包括 `published_at,duration_seconds,local_video,transcript_path`，其他原列会保留。

- `video_id`是平台作品ID或本批稳定来源编号，不能使用每次变化的热门名次作ID。
- `observed_at`填实际记录数据的ISO日期或带时区时间，未知不能默认今天；`published_at`同理，但未取得时可空。
- `url`保留实际原作品入口，工具不会验证远程链接是否可打开，执行者仍须核对。
- 数值可为整数、千分位整数或平台缩写如1.2万。缩写会标为approximate，可能舍入；含加号、区间或无法解释的数值列到excluded。
- 空白/未取得不会当成0。没有主指标的记录不入排序，并提醒当前榜单不代表全范围真实排名。
- 同一指标同值按作品ID升序稳定展示；位于前N边界时须说明人工取舍或补精确值，不能声称ID较小更热门。
- 数据跨日只作提醒，不把旧值自动更新为今天。

例子只展示字段，不包含真实博主或热度数据。

```csv
video_id,author,title,url,published_at,observed_at,likes,comments,duration_seconds,local_video,transcript_path
```

视频是否已取得不参与热门排序。热门前10里有视频缺失时，原排名保留并标记该条待补画面；不要把低排名片自动替换进来。
