# 文件索引

> 快速查找本技能包中的所有文件

---

## 主文档

| 文件 | 说明 | 适用场景 |
|-----|------|---------|
| [README.md](README.md) | 技能总览 | 首次使用，了解全貌 |
| [QUICKSTART.md](QUICKSTART.md) | 快速入门指南 | 5分钟上手 |
| [FAQ.md](FAQ.md) | 常见问题解答 | 遇到问题查阅 |
| [CHECKLIST.md](CHECKLIST.md) | 质量检查清单 | 检查报告质量 |
| [INDEX.md](INDEX.md) | 本文件 | 快速查找 |
| [RELEASE_NOTES.md](RELEASE_NOTES.md) | 发布说明 | 了解版本更新 |
| [MANIFEST.json](MANIFEST.json) | 技能元数据 | 系统集成 |
| [DIRECTORY_TREE.txt](DIRECTORY_TREE.txt) | 目录结构 | 了解文件组织 |

---

## 参考资料 (references/)

### 政策分析框架

| 文件 | 说明 | 适用场景 |
|-----|------|---------|
| [policy_analysis_framework.md](references/policy_analysis_framework.md) | 政策分析框架详解 | 深入学习方法论 |

### 示例报告

| 文件 | 说明 | 适用场景 |
|-----|------|---------|
| [example_national_policy.md](references/example_reports/example_national_policy.md) | 国家级政策示例 | 学习国家级政策分析 |
| [example_local_policy.md](references/example_reports/example_local_policy.md) | 市级政策示例 | 学习市级政策分析 |

---

## 资源文件 (assets/)

### 模板

| 文件 | 说明 | 适用场景 |
|-----|------|---------|
| [decoding_template.md](assets/templates/decoding_template.md) | 解码报告模板 | 编写报告时使用 |
| [v_score_calculator.json](assets/templates/v_score_calculator.json) | V公式评分配置 | V公式评分参考 |
| [elevator_pitch_template.md](assets/templates/elevator_pitch_template.md) | 电梯演讲模板 | 准备汇报话术 |

### AI提示词

| 文件 | 说明 | 适用场景 |
|-----|------|---------|
| [system_prompt.md](assets/prompts/system_prompt.md) | 系统提示词 | AI助手角色定义 |
| [step1_decoding_prompt.md](assets/prompts/step1_decoding_prompt.md) | 步骤1提示词 | 政策解码 |
| [step2_mining_prompt.md](assets/prompts/step2_mining_prompt.md) | 步骤2提示词 | 需求挖掘 |
| [step3_planning_prompt.md](assets/prompts/step3_planning_prompt.md) | 步骤3提示词 | 项目策划 |
| [step4_packaging_prompt.md](assets/prompts/step4_packaging_prompt.md) | 步骤4提示词 | 方案包装 |

---

## 自动化脚本 (scripts/)

| 文件 | 说明 | 适用场景 |
|-----|------|---------|
| [README.md](scripts/README.md) | 脚本使用说明 | 使用脚本前阅读 |
| [policy_decoder.py](scripts/policy_decoder.py) | 主处理脚本 | 完整分析流程 |
| [opportunity_scanner.py](scripts/opportunity_scanner.py) | 机会扫描器 | 快速识别机会 |
| [v_score_calculator.py](scripts/v_score_calculator.py) | V公式评分器 | 项目价值评估 |

---

## 按使用场景索引

### 场景1：首次使用

推荐阅读顺序：
1. [README.md](README.md) - 了解技能全貌
2. [QUICKSTART.md](QUICKSTART.md) - 5分钟快速上手
3. [references/example_reports/](references/example_reports/) - 查看示例

### 场景2：准备分析政策文件

推荐参考资料：
1. [references/policy_analysis_framework.md](references/policy_analysis_framework.md) - 学习方法论
2. [assets/templates/decoding_template.md](assets/templates/decoding_template.md) - 使用报告模板
3. [CHECKLIST.md](CHECKLIST.md) - 对照检查质量

### 场景3：进行项目策划

推荐参考资料：
1. [assets/templates/v_score_calculator.json](assets/templates/v_score_calculator.json) - V公式评分
2. [assets/prompts/step3_planning_prompt.md](assets/prompts/step3_planning_prompt.md) - 项目策划提示词

### 场景4：准备客户汇报

推荐参考资料：
1. [assets/templates/elevator_pitch_template.md](assets/templates/elevator_pitch_template.md) - 电梯演讲模板
2. [assets/prompts/step4_packaging_prompt.md](assets/prompts/step4_packaging_prompt.md) - 方案包装提示词

### 场景5：遇到问题

推荐参考资料：
1. [FAQ.md](FAQ.md) - 常见问题解答
2. [references/policy_analysis_framework.md](references/policy_analysis_framework.md) - 框架详解

### 场景6：使用自动化脚本

推荐参考资料：
1. [scripts/README.md](scripts/README.md) - 脚本使用说明
2. [scripts/policy_decoder.py](scripts/policy_decoder.py) - 主脚本

---

## 关键词索引

| 关键词 | 相关文件 |
|-------|---------|
| 政策解码 | [step1_decoding_prompt.md](assets/prompts/step1_decoding_prompt.md), [policy_analysis_framework.md](references/policy_analysis_framework.md) |
| 需求挖掘 | [step2_mining_prompt.md](assets/prompts/step2_mining_prompt.md) |
| 项目策划 | [step3_planning_prompt.md](assets/prompts/step3_planning_prompt.md), [v_score_calculator.json](assets/templates/v_score_calculator.json) |
| 方案包装 | [step4_packaging_prompt.md](assets/prompts/step4_packaging_prompt.md), [elevator_pitch_template.md](assets/templates/elevator_pitch_template.md) |
| V公式 | [v_score_calculator.json](assets/templates/v_score_calculator.json), [v_score_calculator.py](scripts/v_score_calculator.py) |
| SCQA | [step4_packaging_prompt.md](assets/prompts/step4_packaging_prompt.md), [elevator_pitch_template.md](assets/templates/elevator_pitch_template.md) |
| 电梯演讲 | [elevator_pitch_template.md](assets/templates/elevator_pitch_template.md) |
| 客户画像 | [step2_mining_prompt.md](assets/prompts/step2_mining_prompt.md) |
| 机会扫描 | [opportunity_scanner.py](scripts/opportunity_scanner.py) |

---

## 文件更新记录

| 日期 | 更新内容 | 版本 |
|-----|---------|------|
| 2024-XX-XX | 初始版本发布 | v1.0.0 |

---

> 📌 **提示**：本索引文件会随技能包更新而更新，建议定期查看最新版本。
