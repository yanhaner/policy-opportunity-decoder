#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
政策文件项目机会解码与包装 - 主处理脚本

功能：整合完整的四步分析流程，从政策文件输入到完整报告输出
作者：区域发展规划设计咨询机构
版本：1.0.0
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PolicyDecoder:
    """政策解码器主类"""
    
    def __init__(self, region: str = "", level: str = ""):
        """
        初始化解码器
        
        Args:
            region: 目标区域名称
            level: 政策层级（national/provincial/city/district）
        """
        self.region = region
        self.level = level
        self.policy_text = ""
        self.results = {
            "step1": {},
            "step2": {},
            "step3": {},
            "step4": {}
        }
    
    def load_policy(self, file_path: str) -> str:
        """
        加载政策文件
        
        Args:
            file_path: 政策文件路径
            
        Returns:
            文件内容文本
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        suffix = path.suffix.lower()
        
        if suffix in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.policy_text = f.read()
        elif suffix in ['.docx', '.doc']:
            try:
                from docx import Document
                doc = Document(file_path)
                self.policy_text = '\n'.join([para.text for para in doc.paragraphs])
            except ImportError:
                print("请先安装python-docx: pip install python-docx")
                sys.exit(1)
        elif suffix == '.pdf':
            try:
                import pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    self.policy_text = '\n'.join([page.extract_text() or '' for page in pdf.pages])
            except ImportError:
                print("请先安装pdfplumber: pip install pdfplumber")
                sys.exit(1)
        else:
            raise ValueError(f"不支持的文件格式: {suffix}")
        
        return self.policy_text
    
    def step1_decoding(self) -> Dict:
        """
        第一步：政策解码与机会扫描
        
        Returns:
            解码结果字典
        """
        print("\n=== 步骤1：政策解码与机会扫描 ===")
        
        # 提取关键信息（简化版实现）
        result = {
            "policy_info": {
                "region": self.region,
                "level": self.level,
                "text_length": len(self.policy_text)
            },
            "keywords": self._extract_keywords(),
            "opportunities": self._identify_opportunities()
        }
        
        self.results["step1"] = result
        print(f"✓ 识别到 {len(result['opportunities'])} 个潜在机会点")
        return result
    
    def _extract_keywords(self) -> Dict[str, List[str]]:
        """提取关键词"""
        keywords = {
            "development_direction": [],
            "key_tasks": [],
            "support_areas": [],
            "funding": [],
            "constraints": []
        }
        
        # 预定义关键词库
        keyword_dict = {
            "development_direction": [
                "产业发展", "转型升级", "创新发展", "绿色发展", "高质量发展",
                "数字经济", "智能制造", "新型城镇化", "乡村振兴"
            ],
            "key_tasks": [
                "重点任务", "重点工作", "主要任务", "专项行动", "建设工程"
            ],
            "support_areas": [
                "支持", "鼓励", "引导", "扶持", "奖励", "补贴"
            ],
            "funding": [
                "资金", "投资", "专项债", "预算", "基金", "融资"
            ],
            "constraints": [
                "禁止", "限制", "必须", "应当", "严格", "不得"
            ]
        }
        
        for category, words in keyword_dict.items():
            for word in words:
                if word in self.policy_text:
                    keywords[category].append(word)
        
        return keywords
    
    def _identify_opportunities(self) -> List[Dict]:
        """识别机会点"""
        opportunities = []
        
        # 业务领域映射
        business_mapping = [
            {
                "keywords": ["产业", "园区", "集群"],
                "opportunity": "产业规划与园区策划",
                "clients": ["园区管委会", "工信局"],
                "business": ["规划类", "咨询类", "运营类"]
            },
            {
                "keywords": ["城市更新", "老旧小区", "改造"],
                "opportunity": "城市更新规划设计",
                "clients": ["住建局", "城投公司"],
                "business": ["规划类", "设计类", "投融资"]
            },
            {
                "keywords": ["生态", "环保", "EOD"],
                "opportunity": "生态环保项目策划",
                "clients": ["生态环境局", "平台公司"],
                "business": ["EOD策划", "环境规划"]
            },
            {
                "keywords": ["乡村振兴", "农业", "农村"],
                "opportunity": "乡村振兴规划",
                "clients": ["农业农村局", "乡村振兴局"],
                "business": ["乡村规划", "农业规划"]
            },
            {
                "keywords": ["数字", "智慧", "信息"],
                "opportunity": "数字化规划咨询",
                "clients": ["大数据局", "工信局"],
                "business": ["数字化", "咨询类"]
            }
        ]
        
        for mapping in business_mapping:
            if any(kw in self.policy_text for kw in mapping["keywords"]):
                opportunities.append({
                    "opportunity": mapping["opportunity"],
                    "potential_clients": mapping["clients"],
                    "business_areas": mapping["business"],
                    "priority": "高" if sum(1 for kw in mapping["keywords"] if kw in self.policy_text) >= 2 else "中"
                })
        
        return opportunities
    
    def step2_mining(self) -> Dict:
        """
        第二步：需求挖掘与痛点诊断
        
        Returns:
            需求挖掘结果字典
        """
        print("\n=== 步骤2：需求挖掘与痛点诊断 ===")
        
        # 基于机会点生成客户画像和痛点分析
        clients = []
        pain_points = []
        
        for opp in self.results["step1"].get("opportunities", []):
            for client_type in opp.get("potential_clients", []):
                clients.append({
                    "type": client_type,
                    "pain_points": self._generate_pain_points(client_type),
                    "needs": self._generate_needs(client_type)
                })
        
        result = {
            "clients": clients,
            "pain_points": pain_points
        }
        
        self.results["step2"] = result
        print(f"✓ 完成 {len(clients)} 类客户画像分析")
        return result
    
    def _generate_pain_points(self, client_type: str) -> List[str]:
        """生成痛点列表"""
        pain_point_templates = {
            "园区管委会": [
                "产业定位不清晰，同质化竞争严重",
                "招商资源有限，龙头企业引进难",
                "运营经验不足，园区活力不够"
            ],
            "住建局": [
                "改造资金缺口大，筹措渠道有限",
                "居民协调难度大，意见难以统一",
                "技术标准复杂，质量把控困难"
            ],
            "平台公司": [
                "融资压力大，债务风险高",
                "项目收益不确定，投资回报难保障",
                "专业人才缺乏，运营能力弱"
            ],
            "城投公司": [
                "融资压力大，债务风险高",
                "项目收益不确定，投资回报难保障",
                "专业人才缺乏，运营能力弱"
            ]
        }
        return pain_point_templates.get(client_type, ["资金不足", "人才短缺", "经验缺乏"])
    
    def _generate_needs(self, client_type: str) -> List[str]:
        """生成需求列表"""
        need_templates = {
            "园区管委会": [
                "清晰的产业定位和差异化策略",
                "系统的招商方案和靶向企业清单",
                "可持续的园区运营管理模式"
            ],
            "住建局": [
                "多元化的资金筹措方案",
                "有效的居民协调机制",
                "全过程的质量管控体系"
            ],
            "平台公司": [
                "可行的投融资方案",
                "明确的盈利模式设计",
                "专业的运营团队支持"
            ],
            "城投公司": [
                "可行的投融资方案",
                "明确的盈利模式设计",
                "专业的运营团队支持"
            ]
        }
        return need_templates.get(client_type, ["专业咨询服务", "技术支持", "资源整合"])
    
    def step3_planning(self) -> Dict:
        """
        第三步：项目策划与产品定义
        
        Returns:
            项目策划结果字典
        """
        print("\n=== 步骤3：项目策划与产品定义 ===")
        
        projects = []
        
        for opp in self.results["step1"].get("opportunities", [])[:3]:
            project = {
                "name": f"{self.region or '某市'} {opp['opportunity']}项目",
                "opportunity": opp["opportunity"],
                "v_score": self._calculate_v_score(opp),
                "service_modules": self._design_service_modules(opp)
            }
            projects.append(project)
        
        result = {
            "projects": projects
        }
        
        self.results["step3"] = result
        print(f"✓ 策划 {len(projects)} 个高价值项目")
        return result
    
    def _calculate_v_score(self, opportunity: Dict) -> Dict:
        """计算V公式评分"""
        # 简化版评分逻辑
        scores = {
            "I": 4,  # 战略影响力
            "C": 4,  # 诉求连接度
            "T": 4,  # 时间匹配度
            "S": 3   # 业务协同度
        }
        
        total = scores["I"] * scores["C"] * scores["T"] * scores["S"]
        
        return {
            "scores": scores,
            "total": total,
            "level": "高价值" if total >= 12 else "中等价值"
        }
    
    def _design_service_modules(self, opportunity: Dict) -> Dict:
        """设计服务模块"""
        return {
            "basic": [
                "现状调研与诊断分析",
                "总体规划方案编制",
                "专题研究与技术咨询",
                "实施路径与保障措施"
            ],
            "upgrade": [
                "详细设计方案（+30万）",
                "专项申报方案（+20万）",
                "运营管理模式设计（+25万）"
            ]
        }
    
    def step4_packaging(self) -> Dict:
        """
        第四步：方案包装与呈现
        
        Returns:
            方案包装结果字典
        """
        print("\n=== 步骤4：方案包装与呈现 ===")
        
        if not self.results["step3"].get("projects"):
            return {}
        
        main_project = self.results["step3"]["projects"][0]
        
        result = {
            "main_project": {
                "name": main_project["name"],
                "value_proposition": f"以专业规划引领{self.region or '区域'}发展，以创新模式保障落地成效",
                "highlights": [
                    "定位创新：差异化竞争策略",
                    "模式创新：可持续发展模式",
                    "运营创新：专业化运营体系"
                ],
                "key_metrics": {
                    "投资规模": "10亿元",
                    "预期收益": "年产值20亿元",
                    "就业带动": "5000人",
                    "税收贡献": "1亿元/年"
                }
            },
            "presentation": {
                "elevator_pitch": self._generate_elevator_pitch(main_project),
                "presentation_points": self._generate_presentation_points()
            }
        }
        
        self.results["step4"] = result
        print("✓ 完成方案包装")
        return result
    
    def _generate_elevator_pitch(self, project: Dict) -> str:
        """生成电梯演讲稿"""
        return f"""
针对{self.region or '区域'}在{project['opportunity']}领域的发展需求，
我们提供从规划到落地的全链条服务，
助力打造区域标杆项目，
预计拉动投资10亿元，创造就业岗位5000个。
        """.strip()
    
    def _generate_presentation_points(self) -> Dict:
        """生成汇报要点"""
        return {
            "市委书记/市长": {
                "focus": "战略价值、政绩亮点",
                "key_points": ["打造省级标杆", "写入政府工作报告", "区域影响力提升"]
            },
            "分管副市长": {
                "focus": "实施路径、资金保障",
                "key_points": ["分期实施计划", "多元化融资渠道", "风险可控"]
            },
            "部门负责人": {
                "focus": "操作便利、考核达标",
                "key_points": ["工作流程清晰", "成果可考核", "技术支持到位"]
            }
        }
    
    def generate_report(self, output_dir: str) -> str:
        """
        生成完整报告
        
        Args:
            output_dir: 输出目录
            
        Returns:
            报告文件路径
        """
        print("\n=== 生成完整报告 ===")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 生成Markdown报告
        report_file = output_path / "report.md"
        
        report_content = self._generate_markdown_report()
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # 保存JSON数据
        data_dir = output_path / "data"
        data_dir.mkdir(exist_ok=True)
        
        with open(data_dir / "results.json", 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 报告已生成: {report_file}")
        return str(report_file)
    
    def _generate_markdown_report(self) -> str:
        """生成Markdown格式报告"""
        report = f"""# 政策文件项目机会解码与包装报告

> 生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
> 目标区域: {self.region or '未指定'}
> 政策层级: {self.level or '未指定'}

---

## 一、政策解码摘要

### 1.1 政策基本信息

| 项目 | 内容 |
|-----|------|
| **目标区域** | {self.region or '未指定'} |
| **政策层级** | {self.level or '未指定'} |
| **文本长度** | {len(self.policy_text)} 字符 |

### 1.2 识别的机会点

"""
        
        # 添加机会点表格
        opportunities = self.results["step1"].get("opportunities", [])
        report += "| 序号 | 机会方向 | 潜在客户 | 业务板块 | 优先级 |\n"
        report += "|-----|---------|---------|---------|-------|\n"
        
        for i, opp in enumerate(opportunities, 1):
            clients = ", ".join(opp.get("potential_clients", [])[:2])
            business = ", ".join(opp.get("business_areas", [])[:2])
            report += f"| {i} | {opp['opportunity']} | {clients} | {business} | {opp.get('priority', '中')} |\n"
        
        # 添加客户分析
        report += """

## 二、目标客户与需求洞察

### 2.1 客户画像

"""
        
        clients = self.results["step2"].get("clients", [])
        for client in clients:
            report += f"""
#### {client['type']}

**痛点问题**:
"""
            for pain in client.get('pain_points', [])[:3]:
                report += f"- {pain}\n"
            
            report += "\n**核心需求**:\n"
            for need in client.get('needs', [])[:3]:
                report += f"- {need}\n"
        
        # 添加项目策划
        report += """

## 三、项目机会矩阵

### 3.1 全景式项目机会矩阵表

| 领域 | 对应咨询服务核心职能 | 可能的具体项目机会与服务产品 | 价值与转化要点 |
|---|---|---|---|
| [领域1] | [职能] | [具体项目机会] | [价值转化] |

## 四、策划项目建议

### 4.1 高价值项目推荐

"""
        
        projects = self.results["step3"].get("projects", [])
        for i, proj in enumerate(projects, 1):
            v_score = proj.get('v_score', {})
            report += f"""
#### 项目{i}: {proj['name']}

**V公式评分**: {v_score.get('total', 0)} 分 ({v_score.get('level', '未知')})

| 维度 | 评分 | 说明 |
|-----|------|------|
| I (战略影响力) | {v_score.get('scores', {}).get('I', '-')} | - |
| C (诉求连接度) | {v_score.get('scores', {}).get('C', '-')} | - |
| T (时间匹配度) | {v_score.get('scores', {}).get('T', '-')} | - |
| S (业务协同度) | {v_score.get('scores', {}).get('S', '-')} | - |

**服务模块**:
- 基础包: {', '.join(proj.get('service_modules', {}).get('basic', [])[:2])}
- 升级包: {', '.join(proj.get('service_modules', {}).get('upgrade', [])[:2])}
"""
        
        # 添加方案包装
        main_project = self.results["step4"].get("main_project", {})
        report += f"""

## 五、核心项目深度包装示例

### 5.1 项目基本信息

**项目名称**: {main_project.get('name', '未命名')}

**价值主张**: {main_project.get('value_proposition', '')}

### 5.2 核心创新亮点

"""
        
        for highlight in main_project.get('highlights', []):
            report += f"- {highlight}\n"
        
        report += """
### 5.3 关键数据锚点

"""
        
        for key, value in main_project.get('key_metrics', {}).items():
            report += f"- **{key}**: {value}\n"
        
        report += """

## 六、后续行动建议

### 6.1 汇报策略

| 汇报对象 | 侧重点 | 核心话术 |
|---------|-------|---------|
| 市委书记/市长 | 战略价值、政绩亮点 | 打造省级标杆，写入政府工作报告 |
| 分管副市长 | 实施路径、资金保障 | 分期实施，风险可控 |
| 部门负责人 | 操作便利、考核达标 | 工作流程清晰，成果可考核 |

### 6.2 下一步动作

1. 制作项目概念方案PPT（15分钟版）
2. 预约客户汇报时间
3. 准备类似案例和业绩材料
4. 组建项目工作团队

---

*本报告由政策文件项目机会解码与包装系统自动生成*
"""
        
        return report
    
    def decode(self, file_path: str) -> Dict:
        """
        执行完整解码流程
        
        Args:
            file_path: 政策文件路径
            
        Returns:
            完整分析结果
        """
        # 加载文件
        self.load_policy(file_path)
        
        # 执行四步分析
        self.step1_decoding()
        self.step2_mining()
        self.step3_planning()
        self.step4_packaging()
        
        return self.results


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='政策文件项目机会解码与包装工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python policy_decoder.py -i policy.txt -o ./output
  python policy_decoder.py -i policy.docx -o ./output -r "宜宾市"
  python policy_decoder.py -i policy.pdf -o ./output -l city
        """
    )
    
    parser.add_argument('-i', '--input', required=True, help='政策文件路径')
    parser.add_argument('-o', '--output', required=True, help='输出目录路径')
    parser.add_argument('-r', '--region', default='', help='目标区域名称')
    parser.add_argument('-l', '--level', default='', help='政策层级')
    parser.add_argument('-t', '--template', default='', help='报告模板路径')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("政策文件项目机会解码与包装工具")
    print("=" * 50)
    
    # 创建解码器
    decoder = PolicyDecoder(
        region=args.region,
        level=args.level
    )
    
    try:
        # 执行解码
        results = decoder.decode(args.input)
        
        # 生成报告
        report_path = decoder.generate_report(args.output)
        
        print("\n" + "=" * 50)
        print(f"✓ 分析完成！")
        print(f"✓ 报告路径: {report_path}")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
