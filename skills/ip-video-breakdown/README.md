# 看懂一条视频怎样拍、怎样剪

[单独下载这个技能](https://github.com/sanyetrio/trio-skills/raw/refs/heads/main/downloads/ip-video-breakdown.zip) · [安装方法](https://github.com/sanyetrio/trio-skills/blob/main/docs/%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E4%B8%8E%E5%AE%89%E8%A3%85.md) · [返回用途导航](https://github.com/sanyetrio/trio-skills)

手里有参考视频，想拆清文案、镜头、花字、动画和声音，供自己制作参考。

| 使用前提供 | 完成后得到 |
|---|---|
| 视频文件、已有字幕或时码转写（有就提供）、作者与作品入口。 | 逐段拆片卡、时间位置、截图证据、可参考做法和未确认项。 |

## 直接这样说

> 用 $ip-video-breakdown 拆解这条视频的文案、镜头、花字、动画和声音，每个判断标出原片时间。

## 安装与依赖

把本目录作为完整的 `ip-video-breakdown` 文件夹，放入你使用的 AI 客户端的技能目录，保留 `SKILL.md` 和所有随附资源；已有同名技能先比较，避免覆盖已有修改。在客户端重新加载技能后，发送上面的示例并附上实际材料。

证据准备脚本需要 Python 3、ffmpeg 和 ffprobe；完整拆片还需要当前 AI 能查看视频或截图、播放声音。不依赖其他技能。

## 使用范围

只有文字或截图时会标明观察范围；13＋6 分类需要你提供有权使用的定义，未提供仍可拆解其余内容。

详细执行规则见 [SKILL.md](SKILL.md)。[来源与改动](SOURCE.md) · [使用许可说明](RIGHTS.md)
