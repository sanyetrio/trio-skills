# Seedance 提示词库

为 Seedance / 即梦视频编写、改写和检查提示词。含上游 0.3.0 的中英双语模板与公开案例链接。

- [技能说明](SKILL.md)
- [完整模板库](references/style-library.md)
- [来源与修改记录](SOURCE.json)
- [MIT 许可证](LICENSE)

直接把本目录复制到所用 Agent 的 skills 目录即可使用。此技能只提供提示词，不包含视频生成模型、付费额度或生成 API。模板为固定版本，不能代表平台当前功能或案例热度。

可选安装脚本 `node bin/install.mjs install` 会写入当前用户的 Claude Code 和 Codex 技能目录，并替换同名技能文件；如需保留已有定制，请先备份或手动安装。发布整理仅做脚本语法与命令分派检查，没有执行真实安装。
