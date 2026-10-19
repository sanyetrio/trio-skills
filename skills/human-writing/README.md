# 中文改稿：把现有文字写得自然、顺畅

[单独下载这个技能](https://github.com/sanyetrio/trio-skills/raw/refs/heads/main/downloads/human-writing.zip) · [安装方法](https://github.com/sanyetrio/trio-skills/blob/main/docs/%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E4%B8%8E%E5%AE%89%E8%A3%85.md) · [返回用途导航](https://github.com/sanyetrio/trio-skills)

把已有的中文稿件改成读者容易读下去的表达，保留原来的事实和重点，清理空话、重复解释和生硬句式。

| 你想做什么 | 准备什么 | 可以拿到什么 |
|---|---|---|
| 公众号文章、长帖或回答读起来太生硬 | 原稿、读者是谁、希望保留的内容 | 可直接复制的改稿 |
| 口播稿说起来不顺 | 文案、使用场景、大致时长 | 更适合开口说的稿件 |
| 有材料，需要从头写一篇 | 真实材料、文体、读者、篇幅 | 与材料相符的成稿；缺关键事实时会说明缺口 |

**复制这句话开始：**

> 使用 $human-writing，把下面这篇稿子改得更自然、顺畅。读者是第一次了解这个话题的人，保留事实和核心观点，不添加我的个人经历。只给改好的正文。原稿如下：

## 需要准备

- 一个能读取本地技能文件的 AI 助手，以及你要处理的文字。
- 写作本身不需要额外账号、API Key 或软件。需要查证的新事实，仍要有可靠资料或可用检索工具。
- 可选的文字检查脚本使用 Python 3.9+，只用标准库，不联网，也不自动修改文件。它能提示部分句式问题，不能代替事实核验。

## 安装与使用

1. 下载这一项的完整文件夹，保留名称 `human-writing`。其中的 `references/`、`scripts/`、`agents/` 和 `LICENSE` 一起保留，不只复制 `SKILL.md`。
2. 将整个文件夹放到你所用 AI 客户端支持的技能目录，按客户端的方式重新加载技能。此文件夹已经包含本技能所需资料，不需要下载整套 Trio Skills。
3. 在支持 `$技能名` 的客户端里，用上面的示例开始；其他客户端可明确要求它先读取本文件夹的 [SKILL.md](SKILL.md)，再处理你的稿件。

需要检查成稿时，在本技能文件夹里运行：

```bash
python3 scripts/check_prose.py /你的路径/稿件.md
```

不要把检查脚本的通过理解成事实已经核实。涉及真实人物、数据和亲历的内容，需要有相应材料。

## 来源与许可

来自 [三页技能库的 human-writing](https://github.com/sanyetrio/trio-skills/tree/main/skills/human-writing)。保留原 [MIT 许可证](LICENSE)；现有记录未提供可核实的更早上游仓库地址。详见 [来源记录](SOURCE.md) 与 [权利说明](RIGHTS.md)。
