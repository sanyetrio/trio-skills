# 从作品表里选出热门视频

[单独下载这个技能](https://github.com/sanyetrio/trio-skills/raw/refs/heads/main/downloads/ip-reference-select.zip) · [安装方法](https://github.com/sanyetrio/trio-skills/blob/main/docs/%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E4%B8%8E%E5%AE%89%E8%A3%85.md) · [返回用途导航](https://github.com/sanyetrio/trio-skills)

已经有同一博主的一批作品数据，想找值得参考的前 N 条。

| 使用前提供 | 完成后得到 |
|---|---|
| 作品 CSV 或导出表，包含作品入口、记录日期、点赞或播放等同一指标；指定要选几条。 | 完整排序、入选作品表、未能排序的缺失项，以及每项排名的依据。 |

## 直接这样说

> 用 $ip-reference-select 按点赞量从这份作品表选前 10 条，保留全部排序并标出缺失数据。

## 安装与依赖

把本目录作为完整的 `ip-reference-select` 文件夹，放入你使用的 AI 客户端的技能目录，保留 `SKILL.md` 和所有随附资源；已有同名技能先比较，避免覆盖已有修改。在客户端重新加载技能后，发送上面的示例并附上实际材料。

本地排序需要 Python 3（标准库）；不依赖其他技能。只有作品链接、尚无清单时，需要你提供导出表或当前可用的采集工具。

## 使用范围

本包不会自动抓取全账号，也不能由一份局部清单证明全账号最热门。

详细执行规则见 [SKILL.md](SKILL.md)。[来源与改动](SOURCE.md) · [使用许可说明](RIGHTS.md)
