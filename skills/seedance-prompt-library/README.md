# 把视频想法写成 Seedance 提示词

[单独下载这个技能](https://github.com/sanyetrio/trio-skills/raw/refs/heads/main/downloads/seedance-prompt-library.zip) · [安装方法](https://github.com/sanyetrio/trio-skills/blob/main/docs/%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E4%B8%8E%E5%AE%89%E8%A3%85.md) · [返回用途导航](https://github.com/sanyetrio/trio-skills)

适合你已有一段视频想法，却不确定怎样描述镜头、动作、场景和节奏时使用。技能名：`seedance-prompt-library`。

## 你给什么，得到什么

- **你给：** 想拍什么、主体是谁、发生什么、需要什么风格，以及是否有参考图片或视频。
- **你得到：** 可复制的提示词、所用模板名称和原库公开案例链接。包含广告、产品展示、对话、旅行、动作等 25 组中英双语模板。

## 一句话使用

> 使用 seedance-prompt-library，把“雨后的城市街头，一只橘猫跳上窗台看向屋内”写成一段 8 秒视频提示词，交代镜头、动作和光线，给我中文版。

## 只安装这一项

1. 下载本项的**完整目录**，文件夹命名为 `seedance-prompt-library`，保留 `SKILL.md`、`references/` 和许可证。
2. 把文件夹放入所用 AI 助手的技能目录，例如 Codex 的 `~/.codex/skills/` 或 Claude Code 的 `~/.claude/skills/`。
3. 重新打开会话，点名该技能并说明想做的镜头。也可以直接阅读[完整模板库](references/style-library.md)，自行填写。

本项独立使用，不必下载其他技能。可选的 `bin/install.mjs` 会写入当前用户的 Claude Code 和 Codex 技能目录并替换同名文件；保留已有定制时建议手动安装。

## 最低依赖

阅读模板不需要额外软件。由 AI 自动选模板和改写时，需要能读取技能的 AI 助手；真正生成视频时，需要你自己的 Seedance / 即梦账号或模型服务及相应额度。

**这是一套提示词模板，不是视频生成工具。** 不包含生成 API、模型或付费额度。上游关于案例热度、验证效果、模型版本和能力的描述保留在原材料中，本轮没有重新验证；使用前以你所用平台当前能力为准。

## 来源与说明

基于 [LearnPrompt/awesome-seedance](https://github.com/LearnPrompt/awesome-seedance/tree/9927d9b5bc2d1c305b2945917e461b3547642497/agents/skills/seedance-prompt-library) 的 `0.3.0` 版本，固定提交 `9927d9b5`，采用 [MIT 许可证](LICENSE)。本次仅补中文场景入口，模板和既有安装脚本保持原样。

[完整技能说明](SKILL.md) · [来源与已有适配记录](SOURCE.json) · [此前公开包说明](PREVIOUS_README.md)
