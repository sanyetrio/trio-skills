# 技能目录

本次分享 15 项技能，按用途归类。依赖栏表示运行条件；下载本仓库不会自动准备这些工具。

## 内容生产

| 技能 | 用途 | 运行条件 |
|---|---|---|
| [IP 内容生产总调度](skills/ip-content-sop/SKILL.md) `ip-content-sop` | 串联筛选、拆片、资料入库、适配写稿、分镜和检查 | Python 3；配套七个 ip-* 技能 |
| [热门作品筛选](skills/ip-reference-select/SKILL.md) `ip-reference-select` | 按已有作品数据排序，保留缺失项与来源 | Python 3；使用者提供作品 CSV |
| [视频拆片](skills/ip-video-breakdown/SKILL.md) `ip-video-breakdown` | 整理文案、画面、声音证据与逐条拆片卡 | Python 3.9+、FFmpeg / FFprobe；模型需能实际看图/听视频 |
| [内容资料入库](skills/ip-knowledge-ingest/SKILL.md) `ip-knowledge-ingest` | 一作品一笔记，保留原文、来源、索引与回执 | Markdown 写入能力；正式入库需提供自己的 vault |
| [IP 适配写稿](skills/ip-script-adapt/SKILL.md) `ip-script-adapt` | 依据真实人物资料和参考材料写稿 | 使用者提供人物资料与内容依据 |
| [自动分镜与拍摄清单](skills/ip-auto-storyboard/SKILL.md) `ip-auto-storyboard` | 将稿件编排为分镜、素材清单，校验台词覆盖 | Python 3；使用者提供稿件与拍摄条件 |
| [拍摄方案检查](skills/ip-content-review/SKILL.md) `ip-content-review` | 核对脚本、分镜、素材、来源和交付版本 | 现有脚本与分镜；成片检查另需真实视频 |

## 写作

| 技能 | 用途 | 运行条件 |
|---|---|---|
| [中文写作改稿](skills/human-writing/SKILL.md) `human-writing` | 改善中文表达，保持原意与事实 | 参考文件随包提供；可选脚本需 Python 3.9+ |

## 图片与视觉

| 技能 | 用途 | 运行条件 |
|---|---|---|
| [会议照片精选与精修](skills/conference-photo-edit/SKILL.md) `conference-photo-edit` | 选片、自然精修、尺寸压缩与交付核验 | 使用者原图、人物参照、照片编辑工具 |
| [角色视觉迭代](skills/workbench-character-iteration/SKILL.md) `workbench-character-iteration` | 沿确认参考逐轮调整角色形象 | 支持参考图编辑的图片工具与参考图 |
| [交互结构图](skills/anatomy/SKILL.md) `anatomy` | 制作交互 SVG / HTML / WebGL 结构示意 | Node.js 20.10+；可用浏览器 |

## 音视频

| 技能 | 用途 | 运行条件 |
|---|---|---|
| [口播视频包装](skills/talking-head-packaging/SKILL.md) `talking-head-packaging` | 封面、画面与字幕包装，保留固定模板 | 剪映、开拍或指定编辑器；字体模板自行提供 |
| [Remotion 动态图形](skills/remotion-motion-graphics/SKILL.md) `remotion-motion-graphics` | 使用 React / Remotion 编排和渲染 MG | Node.js、Remotion 与可用浏览器；依赖另行安装 |
| [Seedance 提示词库](skills/seedance-prompt-library/SKILL.md) `seedance-prompt-library` | 25 组中英双语提示词模板 | 文本模板可独立阅读；视频生成需自己的模型服务 |

## 浏览器

| 技能 | 用途 | 运行条件 |
|---|---|---|
| [浏览器自动化](skills/playwright/SKILL.md) `playwright` | 用 Playwright CLI 操作和验证网页 | Node.js / npm / npx、Playwright CLI 与浏览器 |

七个 `ip-*` 需放在同一技能父目录，保持相对引用。视频拆片保留 13＋6 标签名以兼容工作流程；分类定义由使用者提供其有权使用的资料，没有定义时不从标签名称猜判。
