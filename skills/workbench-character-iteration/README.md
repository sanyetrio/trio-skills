# 角色头像改图：保留选中的样子，只改这一轮

[单独下载这个技能](https://github.com/sanyetrio/trio-skills/raw/refs/heads/main/downloads/workbench-character-iteration.zip) · [安装方法](https://github.com/sanyetrio/trio-skills/blob/main/docs/%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE%E4%B8%8E%E5%AE%89%E8%A3%85.md) · [返回用途导航](https://github.com/sanyetrio/trio-skills)

把“颜色更鲜明一点”“轮廓别动”“就按第三张继续”等反馈落实到同一张角色图上，记录每轮基准与结果，减少改着改着换了角色的问题。

适合工作台角色、团队头像、吉祥物和一组人物形象的连续修改。需要从已选版本继续时，提供准确图片，比只说“上一次第三张”更容易衔接。

| 你提供什么 | 可以拿到什么 |
|---|---|
| 基准图片、本轮要改的地方、明确保留的特征 | 可直接使用的编辑提示词，或者按已授权工具执行的修订图 |
| 一组角色、身份对应关系与参考风格 | 带稳定编号的候选方案与差异说明 |
| 已选图片、实际用途、尺寸和透明背景要求 | 按本次范围制作并检查的独立图片资产 |

**复制这句话开始：**

> 使用 $workbench-character-iteration，基于我附上的角色图，这一轮只让颜色更鲜明一些，保留轮廓、五官、表情和材质。沿用我指定的图片编辑工具，保留原图，先给一张修订预览，并告诉我实际像素尺寸。

## 需要准备

- 能查看图片的 AI 助手，以及准确的基准图。
- 只整理反馈或写提示词时，不需要图像生成服务。
- 实际生成或改图需要支持参考图编辑的图像工具及可用权限或额度。技能不附带模型、服务、历史角色素材，也不会因安装而自动获得出图能力。
- 图片预览、独立头像文件和接入你的工作台是不同交付，按你本次的要求执行。

## 安装与使用

1. 下载完整的 `workbench-character-iteration` 文件夹，保留 `agents/` 与其他随附文件。
2. 将整个文件夹放到你所用 AI 客户端支持的技能目录，按客户端的方式重新加载技能。这一项不依赖其他 Trio Skills 文件夹。
3. 在支持 `$技能名` 的客户端里使用上面的请求；其他客户端可让它先读取本文件夹的 [SKILL.md](SKILL.md)，再处理你提供的图片和反馈。

每轮指定基准图、要改的部分与保持不变的部分。实际出图后检查图片本身和像素尺寸；提示词里写了尺寸，不代表输出已经达到该尺寸。

## 来源与许可

从 [三页技能库的 workbench-character-iteration](https://github.com/sanyetrio/trio-skills/tree/main/skills/workbench-character-iteration) 拆出，保留参考图迭代和尺寸核验流程。当前未另行附加 MIT、Apache 等统一许可，详见 [权利说明](RIGHTS.md) 与 [来源记录](SOURCE.md)。
