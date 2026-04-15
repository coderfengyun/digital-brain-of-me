# 核心任务
统计指定时间范围内的金融交易的盈亏情况。
盈亏分两个层次：
1. 第一个层次是每个品种的盈亏
  1.1 第一个层次中，同时标记出浮盈、浮亏、实现盈利、实现亏损。
2. 第二个层次是整体的盈亏。

# 实现方式要求
因为涉及大量的数值计算，要求准确性，尽量有程序完成，只有碰到非结构化无法解析数据时才使用LLM完成。

# 待办
- [x] 交易日志汇总表.csv 已迁移为符合 schema 的格式（由 `write_trade_journal.py migrate` 完成）
- [ ] 运行 `.claude/skills/investment/scripts/calc_pnl.py` 生成盈亏统计报告，并运行 `.claude/skills/investment/scripts/test_calc_pnl.py` 验证集成测试通过