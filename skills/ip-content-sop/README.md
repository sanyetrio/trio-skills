# 把多项内容任务串起来（高级可选）

[单独下载这个技能](https://github.com/sanyetrio/trio-skills/raw/refs/heads/main/downloads/ip-content-sop.zip) · [安装方法](https://github.com/sanyetrio/trio-skills/blob/main/docs/%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E4%B8%8E%E5%AE%89%E8%A3%85.md) · [返回用途导航](https://github.com/sanyetrio/trio-skills)

你已经会用各个单项技能，确实需要把选参考、拆片、资料整理、写稿、分镜和检查接成同一任务。

| 使用前提供 | 完成后得到 |
|---|---|
| 项目目标、已有资料、允许执行的起止步骤和任务输出文件夹。 | 同一项目的阶段产物、版本与缺口记录；只完成你指定的步骤。 |

## 直接这样说

> 用 $ip-content-sop 把这份已有稿件接到分镜和拍摄前检查，只执行这两步并记录产物位置。

## 安装与依赖

把本目录作为完整的 `ip-content-sop` 文件夹，放入你使用的 AI 客户端的技能目录，保留 `SKILL.md` 和所有随附资源；已有同名技能先比较，避免覆盖已有修改。在客户端重新加载技能后，发送上面的示例并附上实际材料。

状态脚本需要 Python 3（标准库）。完整流程依赖六项分别安装的功能技能，见下表；只运行部分流程时需安装对应阶段。

## 使用范围

本包不捆绑六项技能，也不包含采集、云转写或制作服务。只做单项任务时无需安装这个包。

详细执行规则见 [SKILL.md](SKILL.md)。[来源与改动](SOURCE.md) · [使用许可说明](RIGHTS.md)

## 分别安装的功能技能

| 任务 | 技能目录名 |
|---|---|
| 从作品表里选出热门视频 | [ip-reference-select](https://github.com/sanyetrio/trio-skills/tree/main/skills/ip-reference-select) |
| 看懂一条视频怎样拍、怎样剪 | [ip-video-breakdown](https://github.com/sanyetrio/trio-skills/tree/main/skills/ip-video-breakdown) |
| 把参考素材存成能查回的笔记 | [ip-knowledge-ingest](https://github.com/sanyetrio/trio-skills/tree/main/skills/ip-knowledge-ingest) |
| 参考别人的做法，写自己的口播稿 | [ip-script-adapt](https://github.com/sanyetrio/trio-skills/tree/main/skills/ip-script-adapt) |
| 把口播稿变成拍摄分镜 | [ip-auto-storyboard](https://github.com/sanyetrio/trio-skills/tree/main/skills/ip-auto-storyboard) |
| 拍摄前检查稿件和分镜 | [ip-content-review](https://github.com/sanyetrio/trio-skills/tree/main/skills/ip-content-review) |
