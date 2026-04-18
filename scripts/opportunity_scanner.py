#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机会扫描器 - 快速识别政策文件中的项目机会点

功能：扫描政策文件，识别潜在项目机会
作者：区域发展规划设计咨询机构
版本：1.0.0
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


class OpportunityScanner:
    """机会扫描器类"""
    
    # 预定义的业务领域映射
    BUSINESS_MAPPING = [
        {
            "id": "industry",
            "name": "产业规划与园区策划",
            "keywords": ["产业", "园区", "集群", "万亿级","千亿级","优势产业","新兴产业","未来产业","现代农业产业园区","产业链","培育品牌","工业", "制造业", "服务业"],
            "clients": ["园区管委会", "工信局", "发改局", "平台公司"],
            "business": ["规划类", "咨询类", "运营类"],
            "weight": 1.0
        },
        {
            "id": "urban_renewal",
            "name": "城市更新规划设计",
            "keywords": ["城市更新", "老旧小区", "危旧房","完整社区", "城中村", "棚户区"],
            "clients": ["住建局", "城投公司", "发改局", "街道办"],
            "business": ["规划类", "设计类", "投融资"],
            "weight": 1.0
        },
        {
            "id": "Spatial_Planning",
            "name": "国土空间规划",
            "keywords": ["国土空间规划", "村庄规划", "动态维护","城市体检"],
            "clients": ["自然资源局", "乡镇政府", "街道办"],
            "business": ["规划类", "设计类", "投融资"],
            "weight": 1.0
        }, 
        {
            "id": "regional_Planning",
            "name": "区域规划",
            "keywords": ["经济圈", "一体化发展", "都市圈","协同"],
            "clients": ["发改局", "省市政府"],
            "business": ["规划类", "咨询类"],
            "weight": 1.0
        },        
        {
            "id": "ecology",
            "name": "生态环保项目策划",
            "keywords": ["生态", "环保", "碳达峰", "碳中和", "绿色", "低碳", "生态保护修复","生态修复","石漠化","水土流失","治污"],
            "clients": ["生态环境局", "发改局", "环投公司","自然资源局", "水利局"],
            "business": ["规划类", "咨询类", "投融资"],
            "weight": 1.0
        },
        {
            "id": "rural_revitalization",
            "name": "乡村振兴规划",
            "keywords": ["乡村", "农业", "农村", "农民", "耕地", "高标准农田","全域土地综合整治","和美乡村", "千万工程"],
            "clients": ["农业农村局", "发改局", "农发投", "自然资源局","乡镇政府"],
            "business": ["规划类", "工程类", "运营类"],
            "weight": 1.0
        },
        {
            "id": "digital",
            "name": "数字化规划咨询",
            "keywords": ["数字", "智慧", "信息", "大数据", "人工智能", "互联网", "新基建", "场景规划"],
            "clients": ["大数据局", "工信局", "科技局"],
            "business": ["规划类", "咨询类", "数字化"],
            "weight": 1.0
        },
        {
            "id": "infrastructure",
            "name": "基础设施规划设计",
            "keywords": ["交通", "水利", "能源", "市政", "基建", "公路", "铁路", "机场","新型基础设施", "水库"],
            "clients": ["交通局", "水利局", "发改局", "交投公司", "建投公司"],
            "business": ["规划类", "工程类", "设计类"],
            "weight": 1.0
        },
        {
            "id": "culture",
            "name": "文化旅游策划",
            "keywords": ["文化", "旅游", "文旅","文旅融合", "旅游目的地","景观大道","研学","科普","红色旅游","低空旅游","乡村旅游","体育经济","赛事经济"，"旅游度假","休闲度假","康养","文旅品牌","文旅消费精品","旅游公共服务提升","考古遗址","文化街区","历史文化资源保护利用","历史文化名城","历史文化名镇","文旅资源","景区", "文物", "非遗", "文创"],
            "clients": ["文广旅局", "文旅投", "宣传部", "景区管委会"],
            "business": ["咨询类", "运营类", "规划类"],
            "weight": 1.0
        },
        {
            "id": "social",
            "name": "社会民生规划",
            "keywords": ["教育", "医疗", "卫生", "养老", "托育", "民生", "公共服务"],
            "clients": ["教育局", "卫健委", "民政局", "人社局"],
            "business": ["规划类", "工程类", "设计类"],
            "weight": 0.8
        }
    ]
    
    def __init__(self, keyword_file: str = None):
        """
        初始化扫描器
        
        Args:
            keyword_file: 自定义关键词文件路径
        """
        self.policy_text = ""
        self.keywords = self._load_keywords(keyword_file)
        self.results = []
    
    def _load_keywords(self, keyword_file: str = None) -> Dict:
        """加载关键词"""
        keywords = {
            "business": self.BUSINESS_MAPPING,
            "development": [
                "发展", "建设", "推进", "实施", "加快", "促进",
                "提升", "优化", "完善", "加强", "深化", "扩大"
            ],
            "funding": [
                "资金", "投资", "财政", "专项", "债券", "基金",
                "补贴", "奖励", "扶持", "融资", "贷款", "预算"
            ],
            "targets": [
                "目标", "指标", "任务", "计划", "规划", "方案",
                "到202", "到203", "年末", "年底", "期间"
            ]
        }
        
        # 如果提供了关键词文件，加载自定义关键词
        if keyword_file and Path(keyword_file).exists():
            with open(keyword_file, 'r', encoding='utf-8') as f:
                custom_keywords = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                keywords["custom"] = custom_keywords
        
        return keywords
    
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
        
        if suffix == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                self.policy_text = f.read()
        elif suffix == '.docx':
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
    
    def scan(self) -> List[Dict]:
        """
        扫描政策文件，识别机会点
        
        Returns:
            机会点列表
        """
        opportunities = []
        
        # 按业务领域扫描
        for business in self.BUSINESS_MAPPING:
            matches = self._scan_business_area(business)
            if matches:
                opportunity = {
                    "id": business["id"],
                    "name": business["name"],
                    "matched_keywords": matches["keywords"],
                    "match_count": matches["count"],
                    "confidence": matches["confidence"],
                    "potential_clients": business["clients"],
                    "business_areas": business["business"],
                    "priority": self._determine_priority(matches)
                }
                opportunities.append(opportunity)
        
        # 按置信度排序
        opportunities.sort(key=lambda x: x["confidence"], reverse=True)
        
        self.results = opportunities
        return opportunities
    
    def _scan_business_area(self, business: Dict) -> Dict:
        """
        扫描特定业务领域
        
        Args:
            business: 业务领域定义
            
        Returns:
            匹配结果
        """
        matched_keywords = []
        total_count = 0
        
        for keyword in business["keywords"]:
            count = self.policy_text.count(keyword)
            if count > 0:
                matched_keywords.append({
                    "keyword": keyword,
                    "count": count
                })
                total_count += count
        
        # 计算置信度
        if matched_keywords:
            coverage = len(matched_keywords) / len(business["keywords"])
            frequency = min(total_count / 5, 1.0)  # 最多5次计为满分
            confidence = (coverage * 0.6 + frequency * 0.4) * business["weight"]
        else:
            confidence = 0
        
        return {
            "keywords": matched_keywords,
            "count": total_count,
            "confidence": round(confidence, 2)
        }
    
    def _determine_priority(self, matches: Dict) -> str:
        """
        确定机会优先级
        
        Args:
            matches: 匹配结果
            
        Returns:
            优先级（高/中/低）
        """
        confidence = matches["confidence"]
        count = matches["count"]
        
        if confidence >= 0.7 and count >= 3:
            return "高"
        elif confidence >= 0.4 and count >= 1:
            return "中"
        else:
            return "低"
    
    def extract_key_sentences(self, keyword: str, context: int = 50) -> List[str]:
        """
        提取包含关键词的关键句子
        
        Args:
            keyword: 关键词
            context: 上下文长度
            
        Returns:
            关键句子列表
        """
        sentences = []
        pattern = re.compile(f'.{{0,{context}}}{keyword}.{{0,{context}}}')
        matches = pattern.findall(self.policy_text)
        
        for match in matches[:5]:  # 最多返回5条
            sentences.append(match.strip())
        
        return sentences
    
    def generate_summary(self) -> Dict:
        """
        生成扫描摘要
        
        Returns:
            摘要信息
        """
        if not self.results:
            self.scan()
        
        high_priority = [o for o in self.results if o["priority"] == "高"]
        medium_priority = [o for o in self.results if o["priority"] == "中"]
        low_priority = [o for o in self.results if o["priority"] == "低"]
        
        # 统计业务领域
        business_areas = defaultdict(int)
        for opp in self.results:
            for area in opp["business_areas"]:
                business_areas[area] += 1
        
        # 统计潜在客户
        potential_clients = defaultdict(int)
        for opp in self.results:
            for client in opp["potential_clients"]:
                potential_clients[client] += 1
        
        return {
            "total_opportunities": len(self.results),
            "high_priority": len(high_priority),
            "medium_priority": len(medium_priority),
            "low_priority": len(low_priority),
            "top_business_areas": dict(sorted(business_areas.items(), key=lambda x: x[1], reverse=True)[:5]),
            "top_clients": dict(sorted(potential_clients.items(), key=lambda x: x[1], reverse=True)[:5]),
            "recommendations": [o["name"] for o in high_priority[:3]]
        }
    
    def export_to_json(self, output_file: str):
        """
        导出结果为JSON
        
        Args:
            output_file: 输出文件路径
        """
        output = {
            "scan_results": self.results,
            "summary": self.generate_summary()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    
    def export_to_csv(self, output_file: str):
        """
        导出结果为CSV
        
        Args:
            output_file: 输出文件路径
        """
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([
                "序号", "机会方向", "匹配关键词", "匹配次数",
                "置信度", "潜在客户", "业务板块", "优先级"
            ])
            
            for i, opp in enumerate(self.results, 1):
                keywords = ", ".join([k["keyword"] for k in opp["matched_keywords"]])
                clients = ", ".join(opp["potential_clients"])
                business = ", ".join(opp["business_areas"])
                
                writer.writerow([
                    i, opp["name"], keywords, opp["match_count"],
                    opp["confidence"], clients, business, opp["priority"]
                ])
    
    def export_to_markdown(self, output_file: str):
        """
        导出结果为Markdown
        
        Args:
            output_file: 输出文件路径
        """
        summary = self.generate_summary()
        
        content = f"""# 政策文件机会扫描报告

## 扫描摘要

| 指标 | 数值 |
|-----|------|
| 识别机会总数 | {summary['total_opportunities']} |
| 高优先级机会 | {summary['high_priority']} |
| 中优先级机会 | {summary['medium_priority']} |
| 低优先级机会 | {summary['low_priority']} |

## 重点推荐机会

"""
        
        for i, rec in enumerate(summary['recommendations'], 1):
            content += f"{i}. {rec}\n"
        
        content += """

## 详细机会列表

| 序号 | 机会方向 | 置信度 | 优先级 | 潜在客户 |
|-----|---------|-------|-------|---------|
"""
        
        for i, opp in enumerate(self.results, 1):
            clients = ", ".join(opp["potential_clients"][:2])
            content += f"| {i} | {opp['name']} | {opp['confidence']} | {opp['priority']} | {clients} |\n"
        
        content += """

## 业务领域分布

"""
        
        for area, count in summary['top_business_areas'].items():
            content += f"- **{area}**: {count} 个机会\n"
        
        content += """

## 潜在客户分布

"""
        
        for client, count in summary['top_clients'].items():
            content += f"- **{client}**: {count} 个机会\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='政策文件机会扫描器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python opportunity_scanner.py -i policy.txt
  python opportunity_scanner.py -i policy.txt -k keywords.txt
  python opportunity_scanner.py -i policy.txt -o opportunities.xlsx -f csv
        """
    )
    
    parser.add_argument('-i', '--input', required=True, help='政策文件路径')
    parser.add_argument('-k', '--keywords', default=None, help='关键词列表文件')
    parser.add_argument('-o', '--output', default=None, help='输出文件路径')
    parser.add_argument('-f', '--format', default='json', 
                        choices=['json', 'csv', 'md'],
                        help='输出格式（默认: json）')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("政策文件机会扫描器")
    print("=" * 50)
    
    # 创建扫描器
    scanner = OpportunityScanner(keyword_file=args.keywords)
    
    try:
        # 加载文件
        print(f"\n正在加载文件: {args.input}")
        scanner.load_policy(args.input)
        print(f"✓ 文件加载完成，文本长度: {len(scanner.policy_text)} 字符")
        
        # 执行扫描
        print("\n正在扫描机会点...")
        opportunities = scanner.scan()
        
        # 生成摘要
        summary = scanner.generate_summary()
        
        print(f"\n扫描结果:")
        print(f"- 识别机会总数: {summary['total_opportunities']}")
        print(f"- 高优先级机会: {summary['high_priority']}")
        print(f"- 中优先级机会: {summary['medium_priority']}")
        print(f"- 低优先级机会: {summary['low_priority']}")
        
        if summary['recommendations']:
            print(f"\n重点推荐:")
            for i, rec in enumerate(summary['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        # 导出结果
        if args.output:
            print(f"\n正在导出结果: {args.output}")
            if args.format == 'json':
                scanner.export_to_json(args.output)
            elif args.format == 'csv':
                scanner.export_to_csv(args.output)
            elif args.format == 'md':
                scanner.export_to_markdown(args.output)
            print(f"✓ 导出完成")
        
        print("\n" + "=" * 50)
        print("扫描完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
