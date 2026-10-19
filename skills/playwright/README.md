# 让 AI 帮你操作和检查网页

[单独下载这个技能](https://github.com/sanyetrio/trio-skills/raw/refs/heads/main/downloads/playwright.zip) · [安装方法](https://github.com/sanyetrio/trio-skills/blob/main/docs/%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E4%B8%8E%E5%AE%89%E8%A3%85.md) · [返回用途导航](https://github.com/sanyetrio/trio-skills)

适合网页截图、读取页面信息、检查按钮和表单流程，或复现网页操作问题。技能名：`playwright`。

## 你给什么，得到什么

- **你给：** 网页地址、要检查的内容和允许执行的操作范围。
- **你得到：** 实际浏览器中的操作结果、页面状态、截图或整理后的页面信息；需要账号的页面使用你自己的登录方式。

## 一句话使用

> 使用 playwright，打开我提供的网站，检查首页导航是否能正常进入各页面，保存截图并列出实际发现的问题。

## 只安装这一项

1. 下载本项的**完整目录**，文件夹命名为 `playwright`。保留 `scripts/`、`references/`、`assets/`、`LICENSE.txt` 和 `NOTICE.txt`。
2. 把文件夹放入所用 AI 助手的技能目录，例如 Codex 的 `~/.codex/skills/` 或 Claude Code 的 `~/.claude/skills/`。
3. 重新打开会话，点名 `playwright` 并提供网址与任务。若技能安装在非默认位置，按 [SKILL.md](SKILL.md) 将 `PW_SKILL_DIR` 设为实际技能目录。

本项独立使用，不必下载其他技能；安装技能不会自动登录网站。

## 最低依赖

- 能执行终端命令的 AI 助手。
- Node.js / npm / npx、Playwright CLI 及可用浏览器。
- 自带脚本通过 npx 调用 Playwright CLI，首次实际使用可能下载依赖。

分享包不含浏览器登录态。登录、会话和操作结果保存到你自己的项目；发送消息、提交表单或发布内容等动作，需要你在任务中说明。此次分包只核对文件与引用，没有登录网站或执行外部提交。

## 来源与说明

材料源于 [Microsoft playwright-cli](https://github.com/microsoft/playwright-cli/tree/main/skills/playwright-cli)，采用 [Apache 2.0 许可证](LICENSE.txt)，保留 [NOTICE 归属说明](NOTICE.txt)。此版本含已有的 Codex 适配和包装脚本，未记录精确上游提交；本次仅补中文场景入口。

[完整技能说明](SKILL.md) · [命令参考](references/cli.md) · [常用流程](references/workflows.md) · [来源记录](SOURCE.json) · [此前公开包说明](PREVIOUS_README.md)
