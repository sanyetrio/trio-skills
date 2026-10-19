# 把口播稿变成拍摄分镜

[单独下载这个技能](https://github.com/sanyetrio/trio-skills/raw/refs/heads/main/downloads/ip-auto-storyboard.zip) · [安装方法](https://github.com/sanyetrio/trio-skills/blob/main/docs/%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E4%B8%8E%E5%AE%89%E8%A3%85.md) · [返回用途导航](https://github.com/sanyetrio/trio-skills)

稿件已经写好，想知道每句话配什么画面、准备什么素材、怎样交给剪辑。

| 使用前提供 | 完成后得到 |
|---|---|
| 口播原稿、画幅与时长要求、出镜人数、场地设备和现有素材。 | 逐镜头分镜表、画面与声音素材清单、台词覆盖检查。 |

## 直接这样说

> 用 $ip-auto-storyboard 把这份口播稿变成一人一手机能拍的分镜，保留原文，列出需要补拍的素材。

## 安装与依赖

把本目录作为完整的 `ip-auto-storyboard` 文件夹，放入你使用的 AI 客户端的技能目录，保留 `SKILL.md` 和所有随附资源；已有同名技能先比较，避免覆盖已有修改。在客户端重新加载技能后，发送上面的示例并附上实际材料。

分镜编排由当前 AI 完成；表格生成与校验需要 Python 3（标准库）。不依赖其他技能。

## 使用范围

本包交付分镜与清单，不直接拍摄、配音或渲染视频；无实际音频时会标明预计时间。

详细执行规则见 [SKILL.md](SKILL.md)。[来源与改动](SOURCE.md) · [使用许可说明](RIGHTS.md)
