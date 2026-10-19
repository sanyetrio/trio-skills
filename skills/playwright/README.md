# Playwright CLI Skill

通过 Playwright CLI 操作真实浏览器，用快照定位页面元素，检查操作后状态。

- [技能说明](SKILL.md)
- [命令参考](references/cli.md)
- [流程与配置](references/workflows.md)
- [来源与修改记录](SOURCE.json)
- [Apache 2.0 许可证](LICENSE.txt) · [原始归属说明](NOTICE.txt)

需要 Node.js / npm。包装脚本通过 `npx --yes --package @playwright/cli playwright-cli` 运行 CLI，首次实际使用可能下载依赖。会话、登录态和生成物应存入自己的工程，不能随技能分享。

本包没有预置浏览器登录态；整理时仅检查脚本语法、包装参数与引用，未登录网站或执行外部提交。
