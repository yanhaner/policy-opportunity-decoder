#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V公式评分器 - 量化评估项目机会价值

功能：基于V公式（V = I + C + T + S）对项目机会进行量化评分
作者：区域发展规划设计咨询机构
版本：1.0.0
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class VScore:
    """V公式评分数据类"""
    I: int  # Impact 战略影响力
    C: int  # Connection 诉求连接度
    T: int  # Timing 时间匹配度
    S: int  # Synergy 业务协同度
    
    @property
    def total(self) -> int:
        """计算总分"""
        return self.I + self.C + self.T + self.S
    
    @property
    def average(self) -> float:
        """计算平均分"""
        return (self.I + self.C + self.T + self.S) / 4
    
    def get_level(self) -> str:
        """获取评分等级"""
        total = self.total
        if total >= 18:
            return "极高价值"
        elif total >= 15:
            return "高价值"
        elif total >= 12:
            return "中高价值"
        elif total >= 9:
            return "中等价值"
        elif total >= 6:
            return "较低价值"
        else:
            return "低价值"
    
    def get_action(self) -> str:
        """获取建议行动"""
        total = self.total
        if total >= 18:
            return "必须拿下 - 战略级项目，投入最优资源全力争取"
        elif total >= 15:
            return "优先推进 - 优质项目，优先配置资源重点跟进"
        elif total >= 12:
            return "积极争取 - 良好项目，积极争取合理投入"
        elif total >= 9:
            return "选择性跟进 - 一般项目，根据资源情况选择性跟进"
        elif total >= 6:
            return "谨慎评估 - 低价值项目，谨慎评估后决定是否跟进"
        else:
            return "建议放弃 - 价值较低，建议放弃或等待时机"


class VScoreCalculator:
    """V公式评分器类"""
    
    # 维度说明
    DIMENSIONS = {
        "I": {
            "name": "Impact",
            "label": "战略影响力",
            "description": "项目能否写入政府工作报告？能否成为区域标杆？",
            "criteria": [
                (5, "极高影响力", "可写入省级政府工作报告，可成为国家级示范/试点"),
                (4, "高影响力", "可写入市级政府工作报告，可成为省级示范/试点"),
                (3, "中等影响力", "可写入区县级政府工作报告，可成为市级示范/试点"),
                (2, "较低影响力", "可作为部门重点工作，在局部区域有影响力"),
                (1, "低影响力", "常规性项目，影响力局限于项目本身")
            ]
        },
        "C": {
            "name": "Connection",
            "label": "诉求连接度",
            "description": "是否直接解决核心决策者（如书记、市长）的KPI或痛点？",
            "criteria": [
                (5, "极高连接度", "直接解决一把手的核心KPI，客户有强烈意愿和明确预算"),
                (4, "高连接度", "直接解决分管领导的核心KPI，客户有明确需求和预算计划"),
                (3, "中等连接度", "解决部门负责人的工作任务，客户有需求但预算不确定"),
                (2, "较低连接度", "解决业务层面的常规需求，预算不明确或有限"),
                (1, "低连接度", "锦上添花型项目，客户需求不明确，无明确预算来源")
            ]
        },
        "T": {
            "name": "Timing",
            "label": "时间匹配度",
            "description": "是否契合政策窗口期和资金申报节奏？",
            "criteria": [
                (5, "极佳时机", "正值政策密集出台期，资金申报窗口即将开启，竞争尚不激烈"),
                (4, "良好时机", "政策环境有利，资金渠道畅通，客户有明确时间计划"),
                (3, "一般时机", "政策环境平稳，资金来源有保障，客户时间要求一般"),
                (2, "较差时机", "政策窗口即将关闭，资金申报刚结束，市场竞争激烈"),
                (1, "不佳时机", "政策红利期已过，资金渠道不畅，市场已饱和")
            ]
        },
        "S": {
            "name": "Synergy",
            "label": "业务协同度",
            "description": "能否带动机构内部3个及以上业务部门参与？",
            "criteria": [
                (5, "极高协同度", "可带动5个及以上业务部门，形成完整业务链条"),
                (4, "高协同度", "可带动4个业务部门，业务链条较完整"),
                (3, "中等协同度", "可带动3个业务部门，业务链条基本完整"),
                (2, "较低协同度", "可带动2个业务部门，业务链条不完整"),
                (1, "低协同度", "仅涉及1个业务部门，单一业务类型")
            ]
        }
    }
    
    def __init__(self, config_file: str = None):
        """
        初始化评分器
        
        Args:
            config_file: 配置文件路径
        """
        self.config = self._load_config(config_file)
        self.projects = []
    
    def _load_config(self, config_file: str = None) -> Dict:
        """加载配置文件"""
        default_config = {
            "thresholds": {
                "high_value": 12,
                "medium_value": 8,
                "low_value": 0
            },
            "dimensions": self.DIMENSIONS
        }
        
        if config_file and Path(config_file).exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)
                default_config.update(custom_config)
        
        return default_config
    
    def show_criteria(self, dimension: str = None):
        """
        显示评分标准
        
        Args:
            dimension: 维度代码（I/C/T/S），None表示显示全部
        """
        dimensions = [dimension] if dimension else ["I", "C", "T", "S"]
        
        for dim in dimensions:
            if dim in self.DIMENSIONS:
                info = self.DIMENSIONS[dim]
                print(f"\n{'='*50}")
                print(f"{dim} - {info['label']} ({info['name']})")
                print(f"{'='*50}")
                print(f"说明: {info['description']}")
                print(f"\n评分标准:")
                for score, level, desc in info['criteria']:
                    print(f"  {score}分 - {level}: {desc}")
    
    def interactive_score(self, project_name: str = None) -> Dict:
        """
        交互式评分
        
        Args:
            project_name: 项目名称
            
        Returns:
            评分结果
        """
        print("\n" + "="*50)
        print("V公式评分计算器")
        print("="*50)
        
        if not project_name:
            project_name = input("\n项目名称: ").strip()
        
        scores = {}
        reasons = {}
        
        for dim in ["I", "C", "T", "S"]:
            info = self.DIMENSIONS[dim]
            
            print(f"\n{'-'*50}")
            print(f"{dim} - {info['label']}")
            print(f"{'-'*50}")
            print(f"说明: {info['description']}")
            print("\n评分标准:")
            for score, level, desc in info['criteria']:
                print(f"  {score}分 - {level}")
            
            while True:
                try:
                    score = int(input(f"\n请输入评分 (1-5): ").strip())
                    if 1 <= score <= 5:
                        scores[dim] = score
                        break
                    else:
                        print("请输入1-5之间的数字")
                except ValueError:
                    print("请输入有效的数字")
            
            reason = input("请输入评分理由: ").strip()
            reasons[dim] = reason
        
        # 创建评分对象
        v_score = VScore(
            I=scores["I"],
            C=scores["C"],
            T=scores["T"],
            S=scores["S"]
        )
        
        # 显示结果
        print("\n" + "="*50)
        print("评分结果")
        print("="*50)
        print(f"项目名称: {project_name}")
        print(f"I (战略影响力): {v_score.I}")
        print(f"C (诉求连接度): {v_score.C}")
        print(f"T (时间匹配度): {v_score.T}")
        print(f"S (业务协同度): {v_score.S}")
        print(f"-"*50)
        print(f"总分: {v_score.total}")
        print(f"评估等级: {v_score.get_level()}")
        print(f"建议行动: {v_score.get_action()}")
        
        return {
            "project_name": project_name,
            "scores": scores,
            "reasons": reasons,
            "total": v_score.total,
            "level": v_score.get_level(),
            "action": v_score.get_action()
        }
    
    def batch_score(self, projects_file: str) -> List[Dict]:
        """
        批量评分
        
        Args:
            projects_file: 项目信息JSON文件路径
            
        Returns:
            评分结果列表
        """
        with open(projects_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        projects = data.get("projects", [])
        results = []
        
        for project in projects:
            name = project.get("name", "未命名")
            scores = project.get("scores", {})
            
            v_score = VScore(
                I=scores.get("I", 3),
                C=scores.get("C", 3),
                T=scores.get("T", 3),
                S=scores.get("S", 3)
            )
            
            result = {
                "project_name": name,
                "scores": scores,
                "total": v_score.total,
                "level": v_score.get_level(),
                "action": v_score.get_action()
            }
            results.append(result)
        
        return results
    
    def compare_projects(self, results: List[Dict]) -> Dict:
        """
        比较多个项目
        
        Args:
            results: 评分结果列表
            
        Returns:
            比较结果
        """
        if not results:
            return {}
        
        # 按总分排序
        sorted_results = sorted(results, key=lambda x: x["total"], reverse=True)
        
        # 计算统计信息
        totals = [r["total"] for r in results]
        avg_score = sum(totals) / len(totals)
        max_score = max(totals)
        min_score = min(totals)
        
        return {
            "ranking": sorted_results,
            "statistics": {
                "average": round(avg_score, 2),
                "max": max_score,
                "min": min_score,
                "count": len(results)
            },
            "recommendations": [r["project_name"] for r in sorted_results[:3]]
        }
    
    def export_results(self, results: List[Dict], output_file: str):
        """
        导出评分结果
        
        Args:
            results: 评分结果列表
            output_file: 输出文件路径
        """
        output = {
            "projects": results,
            "comparison": self.compare_projects(results)
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    
    def print_report(self, results: List[Dict]):
        """
        打印评分报告
        
        Args:
            results: 评分结果列表
        """
        comparison = self.compare_projects(results)
        
        print("\n" + "="*70)
        print("V公式评分报告")
        print("="*70)
        
        print("\n【项目评分详情】")
        print("-"*70)
        
        for i, result in enumerate(comparison["ranking"], 1):
            print(f"\n{i}. {result['project_name']}")
            print(f"   总分: {result['total']} 分")
            print(f"   等级: {result['level']}")
            print(f"   建议: {result['action']}")
            scores = result.get("scores", {})
            print(f"   分项: I={scores.get('I', '-')}, C={scores.get('C', '-')}, "
                  f"T={scores.get('T', '-')}, S={scores.get('S', '-')}")
        
        print("\n【统计信息】")
        print("-"*70)
        stats = comparison["statistics"]
        print(f"项目总数: {stats['count']}")
        print(f"平均得分: {stats['average']}")
        print(f"最高得分: {stats['max']}")
        print(f"最低得分: {stats['min']}")
        
        print("\n【重点推荐项目】")
        print("-"*70)
        for i, rec in enumerate(comparison["recommendations"], 1):
            print(f"{i}. {rec}")
        
        print("\n" + "="*70)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='V公式评分计算器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式评分
  python v_score_calculator.py -I
  
  # 批量评分
  python v_score_calculator.py -i projects.json -o scores.json
  
  # 查看评分标准
  python v_score_calculator.py --criteria
        """
    )
    
    parser.add_argument('-I', '--interactive', action='store_true',
                        help='交互式评分模式')
    parser.add_argument('-i', '--input', default=None,
                        help='项目信息JSON文件（批量评分）')
    parser.add_argument('-o', '--output', default=None,
                        help='评分结果输出文件')
    parser.add_argument('-c', '--config', default=None,
                        help='评分配置文件路径')
    parser.add_argument('--criteria', action='store_true',
                        help='显示评分标准')
    parser.add_argument('--dimension', default=None,
                        choices=['I', 'C', 'T', 'S'],
                        help='显示指定维度的评分标准')
    
    args = parser.parse_args()
    
    # 创建评分器
    calculator = VScoreCalculator(config_file=args.config)
    
    # 显示评分标准
    if args.criteria or args.dimension:
        calculator.show_criteria(args.dimension)
        return
    
    # 交互式评分
    if args.interactive:
        results = []
        while True:
            result = calculator.interactive_score()
            results.append(result)
            
            cont = input("\n是否继续评分下一个项目? (y/n): ").strip().lower()
            if cont != 'y':
                break
        
        if results:
            calculator.print_report(results)
            
            if args.output:
                calculator.export_results(results, args.output)
                print(f"\n✓ 结果已保存至: {args.output}")
        
        return
    
    # 批量评分
    if args.input:
        if not Path(args.input).exists():
            print(f"✗ 文件不存在: {args.input}")
            sys.exit(1)
        
        print("="*50)
        print("V公式批量评分")
        print("="*50)
        
        results = calculator.batch_score(args.input)
        calculator.print_report(results)
        
        if args.output:
            calculator.export_results(results, args.output)
            print(f"\n✓ 结果已保存至: {args.output}")
        
        return
    
    # 如果没有指定任何模式，显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()
