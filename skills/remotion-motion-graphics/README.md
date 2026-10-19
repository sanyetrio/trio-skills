# 制作视频片头、动态数字和透明动画素材

[单独下载这个技能](https://github.com/sanyetrio/trio-skills/raw/refs/heads/main/downloads/remotion-motion-graphics.zip) · [安装方法](https://github.com/sanyetrio/trio-skills/blob/main/docs/%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E4%B8%8E%E5%AE%89%E8%A3%85.md) · [返回用途导航](https://github.com/sanyetrio/trio-skills)

适合给口播、课程或产品视频做标题动画、人物条、数字变化、动态图表和片尾。技能名：`remotion-motion-graphics`。

## 你给什么，得到什么

- **你给：** 动画文案、时长、画幅、风格参考，以及自己要使用的图片、字体或音频；已有 Remotion 工程也可以直接提供。
- **你得到：** 可编辑的 React / Remotion 动画工程，以及按需求实际渲染的 MP4、透明 ProRes 或 PNG 序列。

## 一句话使用

> 使用 remotion-motion-graphics，做一段 5 秒的课程片头，标题是“今天学会连接池”，浅色背景、简洁入场和退场，交付可编辑工程和 MP4。

## 只安装这一项

1. 下载本项的**完整目录**，文件夹命名为 `remotion-motion-graphics`，保留 `SKILL.md`、`references/` 和许可证。
2. 把文件夹放入所用 AI 助手的技能目录，例如 Codex 的 `~/.codex/skills/` 或 Claude Code 的 `~/.claude/skills/`。
3. 重新打开会话，点名该技能并描述要做的动画。它可从[新工程参考](references/scaffold.md)开始，也可接入你已有的 Remotion 工程。

本项独立使用，不必下载其他技能；下载技能也不会自动安装视频渲染环境。

## 最低依赖

- 能编辑代码、执行命令和检查画面的 AI 助手。
- Node.js / npm、目标工程中的 React / Remotion 依赖，以及 Remotion 渲染所需的浏览器环境。
- 图片、字体、音频由你按项目提供。具体工程依赖见[搭建说明](references/scaffold.md)。

本项是一套制作指令和参考代码，未附带成片模板或运行环境。此次分包未实际生成视频；使用时需要检查渲染结果、画面和声音。

## 来源与说明

基于 [fernandokaraka/remotion-motion-graphics-skill](https://github.com/fernandokaraka/remotion-motion-graphics-skill/tree/1fc286924c68260b7945f1f29e474b986446b70d)，固定提交 `1fc28692`，采用 [MIT 许可证](LICENSE)。保留参考文件和许可，本次仅补中文场景入口。

[完整技能说明](SKILL.md) · [来源与已有适配记录](UPSTREAM.json) · [此前公开包说明](PREVIOUS_README.md)
