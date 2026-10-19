# 文件交接与状态

任务目录是同一次生产的唯一进度入口。阶段可以独立调用，但完整任务始终引用同一个 `task.json`。

```text
任务目录/
  task.json                 IP、范围、本次起止阶段、状态、版本、文件哈希
  inputs/                   原清单、IP资料或实际来源引用
  selection/                排序结果、前N条、数据缺失
  breakdowns/               R01.md/json…逐作品拆片
  knowledge/                逐作品笔记、参考做法、索引、写入回执
  script/                   适配表、稿件、段落与来源
  storyboard/               分镜、素材需求、台词覆盖检查
  review/                   审核、交付清单、实际反馈
```

文件名可随项目保持既有规则，在任务状态中登记实际路径即可。不以模板存在证明产物已完成，不把空白表当真实拆片。

## 最小交接要求

- 每条作品保持同一个稳定ID。热门名次另列，排名变化不修改素材身份。
- 原素材层保存原作者、入口、实际取得日期、可用完整文本与视频位置。拆片中的每条视觉/声音判断对应原片时间及观察证据。
- `coverage` 或同等明确字段注明实际观看/听审/阅读范围。抽了帧不等于看了整片，有ASR不等于听过声音。
- 所有脚本事实连接当前IP的资料；外部参考连接作者与作品时间。AI新增构思标为建议，不冒充原片事实。
- 新稿的预计时长、真实音频时长、原片引用时间是三种不同字段。
- 各专业Skill规定其Markdown/JSON字段，完成后在状态中登记需要下游读取的文件。主调度读取文件正文，不能只看“成功”标志。

## 命令

以下相对路径以 `ip-content-sop` 技能目录为起点。实际操作先解析技能主目录。

```bash
python3 scripts/pipeline.py init --root /绝对路径/任务目录 --task-id 示例任务 --ip 当前IP --scope 本批范围
python3 scripts/pipeline.py status --root /绝对路径/任务目录
python3 scripts/pipeline.py record --root /绝对路径/任务目录 --stage selection --status ready --input inputs/作品.csv --artifact selection/selection.json --artifact selection/ranked.csv --note 已核排序口径和缺失表
```

`init --start-stage storyboard --end-stage review` 允许仅完成当前稿件的分镜与核验，不强迫做前面四步。此时必须在 `inputs/` 放实际稿件及资源说明，再以 `record --input inputs/稿件.json` 登记输入指纹。

`record --input` 可重复，记录本阶段实际读取的自有输入、原素材清单或其他文件。完整串联时，前一阶段的版本与输出自动形成上游依赖；有额外来源仍须显式登记。工具不判断事实真伪，负责人依据专业Skill验收后才可记录ready。

`ready`要求至少一个非空文件和检查说明；前一步未ready时不能跨过去伪报整条完成。某条独立分支能做，先保存产物并记partial，等缺口补齐后验收。`status`发现文件变化、缺失或上游版本变化会显示stale，不修改已有文件。
