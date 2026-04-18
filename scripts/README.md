# 自动化脚本使用说明

> 本目录包含用于辅助政策文件分析的自动化脚本工具

---

## 脚本清单

| 脚本名称 | 功能描述 | 使用场景 |
|---------|---------|---------|
| `policy_decoder.py` | 主处理脚本，整合全流程 | 完整分析流程 |
| `opportunity_scanner.py` | 机会扫描器，快速识别机会点 | 初步筛选 |
| `v_score_calculator.py` | V公式评分器，量化评估项目价值 | 项目评估 |

---

## 环境要求

### Python版本
- Python 3.8 或更高版本

### 依赖库
```bash
pip install -r requirements.txt
```

主要依赖：
- `pandas` - 数据处理
- `openpyxl` - Excel文件操作
- `python-docx` - Word文档操作
- `requests` - 网络请求（如需在线功能）

---

## 使用指南

### 1. 主处理脚本 (policy_decoder.py)

#### 功能
整合完整的四步分析流程，从政策文件输入到完整报告输出。

#### 使用方法

```bash
python policy_decoder.py --input <政策文件路径> --output <输出目录> [选项]
```

#### 参数说明

| 参数 | 简写 | 说明 | 必需 |
|-----|------|------|------|
| `--input` | `-i` | 政策文件路径（支持.txt, .docx, .pdf） | 是 |
| `--output` | `-o` | 输出目录路径 | 是 |
| `--region` | `-r` | 目标区域名称 | 否 |
| `--level` | `-l` | 政策层级（national/provincial/city/district） | 否 |
| `--template` | `-t` | 报告模板路径 | 否 |

#### 示例

```bash
# 基本使用
python policy_decoder.py -i policy.txt -o ./output

# 指定目标区域
python policy_decoder.py -i policy.docx -o ./output -r "宜宾市"

# 指定政策层级
python policy_decoder.py -i policy.pdf -o ./output -l city
```

#### 输出文件

```
output/
├── report.md              # 完整分析报告
├── step1_decoding.md      # 政策解码结果
├── step2_mining.md        # 需求挖掘结果
├── step3_planning.md      # 项目策划结果
├── step4_packaging.md     # 方案包装结果
└── data/
    ├── opportunities.json  # 机会点数据
    ├── v_scores.json       # V公式评分数据
    └── summary.xlsx        # 汇总表格
```

---

### 2. 机会扫描器 (opportunity_scanner.py)

#### 功能
快速扫描政策文件，识别潜在项目机会点。

#### 使用方法

```bash
python opportunity_scanner.py --input <政策文件路径> [选项]
```

#### 参数说明

| 参数 | 简写 | 说明 | 必需 |
|-----|------|------|------|
| `--input` | `-i` | 政策文件路径 | 是 |
| `--keywords` | `-k` | 关键词列表文件（每行一个关键词） | 否 |
| `--output` | `-o` | 输出文件路径 | 否 |
| `--format` | `-f` | 输出格式（json/csv/md） | 否 |

#### 示例

```bash
# 基本使用
python opportunity_scanner.py -i policy.txt

# 指定关键词文件
python opportunity_scanner.py -i policy.txt -k keywords.txt

# 输出为Excel格式
python opportunity_scanner.py -i policy.txt -o opportunities.xlsx -f csv
```

#### 输出示例

```json
{
  "opportunities": [
    {
      "id": 1,
      "source_text": "推动产业园区和产业集群数字化转型",
      "opportunity_type": "产业园区规划",
      "potential_clients": ["园区管委会", "平台公司"],
      "business_areas": ["园区规划", "信息化咨询"],
      "priority": "高",
      "confidence": 0.95
    }
  ]
}
```

---

### 3. V公式评分器 (v_score_calculator.py)

#### 功能
基于V公式（V = I + C + T + S）对项目机会进行量化评分。

#### 使用方法

```bash
python v_score_calculator.py [选项]
```

#### 参数说明

| 参数 | 简写 | 说明 | 必需 |
|-----|------|------|------|
| `--interactive` | `-I` | 交互式评分模式 | 否 |
| `--input` | `-i` | 项目信息JSON文件 | 否 |
| `--output` | `-o` | 评分结果输出文件 | 否 |
| `--config` | `-c` | 评分配置文件路径 | 否 |

#### 交互式评分示例

```bash
python v_score_calculator.py -I
```

运行后将依次提示输入：

```
=== V公式评分计算器 ===

项目名称: 宜宾三江新区数字经济产业园规划

--- Impact（战略影响力）---
1 - 低影响力
2 - 较低影响力
3 - 中等影响力
4 - 高影响力
5 - 极高影响力

请输入评分 (1-5): 5
请输入评分理由: 可写入市政府工作报告，打造省级标杆

--- Connection（诉求连接度）---
...

=== 评分结果 ===
项目名称: 宜宾三江新区数字经济产业园规划
I (Impact): 5
C (Connection): 5
T (Timing): 4
S (Synergy): 5
总分: 400
评估等级: 极高价值
建议行动: 必须拿下
```

#### 批量评分示例

```bash
# 准备项目信息文件 projects.json
python v_score_calculator.py -i projects.json -o scores.json
```

#### 项目信息文件格式 (projects.json)

```json
{
  "projects": [
    {
      "name": "项目A",
      "scores": {
        "I": 5,
        "C": 5,
        "T": 4,
        "S": 4
      }
    },
    {
      "name": "项目B",
      "scores": {
        "I": 4,
        "C": 4,
        "T": 3,
        "S": 3
      }
    }
  ]
}
```

---

## 配置文件

### 评分配置文件 (v_score_config.json)

```json
{
  "thresholds": {
    "high_value": 12,
    "medium_value": 8,
    "low_value": 0
  },
  "dimensions": {
    "I": {
      "name": "战略影响力",
      "description": "项目能否写入政府工作报告？能否成为区域标杆？"
    },
    "C": {
      "name": "诉求连接度",
      "description": "是否直接解决核心决策者的KPI或痛点？"
    },
    "T": {
      "name": "时间匹配度",
      "description": "是否契合政策窗口期和资金申报节奏？"
    },
    "S": {
      "name": "业务协同度",
      "description": "能否带动机构内部3个及以上业务部门参与？"
    }
  }
}
```

### 关键词配置文件 (keywords.txt)

```
# 产业升级关键词
产业园区
产业集群
数字化转型
智能制造

# 城市更新关键词
城市更新
老旧小区
棚户区改造
历史文化保护

# 生态环保关键词
生态修复
EOD模式
碳达峰
碳中和

# 基础设施关键词
新基建
智慧城市
交通基础设施
水利设施
```

---

## 高级用法

### 批量处理多个政策文件

```bash
# 使用shell脚本批量处理
for file in policies/*.txt; do
    python policy_decoder.py -i "$file" -o "output/$(basename $file .txt)"
done
```

### 自定义报告模板

1. 复制模板文件
```bash
cp templates/decoding_template.md my_template.md
```

2. 修改模板内容

3. 使用自定义模板
```bash
python policy_decoder.py -i policy.txt -o ./output -t my_template.md
```

### 集成到工作流

```python
# 在Python代码中调用
from policy_decoder import PolicyDecoder

decoder = PolicyDecoder(
    region="宜宾市",
    level="city"
)

result = decoder.decode("policy.txt")
report = decoder.generate_report(result)
```

---

## 故障排除

### 常见问题

#### Q1: 中文乱码
**原因**: 文件编码问题  
**解决**: 确保文件使用UTF-8编码

```bash
# 转换文件编码
iconv -f GBK -t UTF-8 policy.txt > policy_utf8.txt
```

#### Q2: PDF文件无法读取
**原因**: 缺少PDF解析库  
**解决**: 安装pdfplumber

```bash
pip install pdfplumber
```

#### Q3: 评分结果异常
**原因**: 配置文件格式错误  
**解决**: 检查JSON格式，使用在线工具验证

---

## 更新日志

### v1.0.0 (2024-XX-XX)
- 初始版本发布
- 实现基础的四步分析流程
- 支持常见文档格式

---

## 技术支持

如有问题或建议，请联系：
- 邮箱: [support@example.com]
- 电话: [联系电话]

---

> 📌 **提示**：脚本工具为辅助分析手段，分析结果需要结合专业判断，不能完全依赖自动化输出。
