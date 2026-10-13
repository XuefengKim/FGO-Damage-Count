# FGO 数据快照与辅助增伤笔记

保存本次讨论使用的 Chaldea 数据，供以后离线查询与核算。不是自动更新的数据库，也不是完整 Chaldea 应用。

- 来源：[chaldea-center/chaldea-data](https://github.com/chaldea-center/chaldea-data)。具体提交、版本、文件 SHA-256 见 [data/manifest.json](data/manifest.json)。
- 数据版本：2026-10-12 21:22:34 UTC，即北京时间 2026-10-13 05:22:34。
- 486 条英灵、8,673 条基础技能、3,248 条效果函数；另含宝具、常量和翻译映射。
- [计算结论与适用条件](notes/conclusions.zh.md)。这些是条件化的候选比较，不是完整战斗模拟器或全游戏最优性的证明。

## 调用

只需要 Python 3.9+，无额外依赖、无需 API 密钥：

```bash
python3 scripts/query.py 梅林
python3 scripts/query.py 500800 --full
python3 scripts/query.py 诺克娜蕾 --full
python3 scripts/query.py Oberon --full > /tmp/oberon.json
```

`--full` 默认按每个技能槽最高 `priority` 选择技能版本，展开技能、宝具和效果函数引用；保留强化任务、再临等使用条件，不能把最高版本当作每个服务器都已开放。宝具保留所有版本，需要根据再临、强化和实际宝具选取；被动保留原始引用。加 `--all-skills` 可查看旧技能。

原始数据分片在 `data/chaldea/`。`servants.*.json` 中技能是引用，需要关联 `baseSkills.json`，再关联 `baseFunctions.json`；宝具关联 `baseTds.json`。技能数值采用压缩存储：各等级/OC 行缺失的字段继承 **svals 第一行**，不是上一等级。脚本已展开这一层；效果类型、特性条件、触发技能仍须按游戏规则解释。不同效果数值的单位不同，不能把所有 `Value` 都当作百分比。

## 来源与权利

原始 JSON 保持来源文件内容不变；该项目使用的数据链包括 Atlas Academy 与 Chaldea 的整理、翻译。这里的保存不对上游数据、翻译或游戏素材新增授权，也不把 Chaldea 应用源码的许可证自动套到独立数据仓库上。需要再分发时应核查对应来源的使用规则。
