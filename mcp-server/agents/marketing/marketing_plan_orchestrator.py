"""
Marketing Plan Orchestrator - Coordinates all agents to generate complete marketing plans
"""
import json
from datetime import datetime
from typing import Dict, Optional
from .market_research_agent import market_research_agent
from .creative_strategy_agent import creative_strategy_agent
from .evaluator_agent import evaluator_agent


class MarketingPlanOrchestrator:
    """
    Orchestrates the marketing plan generation process.
    Coordinates: Research Agent → Strategy Agent → Evaluator Agent → Final Plan
    """
    
    def __init__(self):
        self.research_agent = market_research_agent
        self.strategy_agent = creative_strategy_agent
        self.evaluator_agent = evaluator_agent
    
    def generate_marketing_plan(
        self, 
        product_data: Dict, 
        auto_iterate: bool = False,
        max_iterations: int = 1
    ) -> Dict:
        """
        Generate a complete marketing plan with all 12 sections.
        
        Args:
            product_data: Dictionary containing product information
            auto_iterate: If True, automatically improve plan based on evaluation
            max_iterations: Maximum number of improvement iterations
            
        Returns:
            Complete marketing plan with all sections and metadata
        """
        print("=" * 80)
        print("🚀 MARKETING PLAN GENERATION STARTED")
        print("=" * 80)
        print(f"Product: {product_data.get('product_name', 'Unknown')}")
        print(f"Category: {product_data.get('product_category', 'Unknown')}")
        print(f"Auto-iterate: {auto_iterate}")
        print("=" * 80)
        
        # Phase 1: Market Research
        print("\n" + "=" * 80)
        print("PHASE 1: MARKET RESEARCH & ANALYSIS")
        print("=" * 80)
        research_data = self.research_agent.conduct_full_research(product_data)
        print("\n✅ Research phase completed!")
        
        # Phase 2: Strategy Development
        print("\n" + "=" * 80)
        print("PHASE 2: MARKETING STRATEGY DEVELOPMENT")
        print("=" * 80)
        strategy_data = self.strategy_agent.develop_full_strategy(product_data, research_data)
        print("\n✅ Strategy phase completed!")
        
        # Phase 3: Evaluation
        print("\n" + "=" * 80)
        print("PHASE 3: EVALUATION & QUALITY ASSESSMENT")
        print("=" * 80)
        evaluation_data = self.evaluator_agent.evaluate_full_plan(
            product_data, 
            research_data, 
            strategy_data
        )
        print("\n✅ Evaluation phase completed!")
        
        # Optional: Iteration based on evaluation
        iteration_count = 0
        if auto_iterate and evaluation_data.get('overall_score', 0) < 8.0 and iteration_count < max_iterations:
            print("\n" + "=" * 80)
            print(f"PHASE 4: ITERATION {iteration_count + 1}/{max_iterations}")
            print("=" * 80)
            print(f"Current score: {evaluation_data.get('overall_score', 0):.1f}/10")
            print("Attempting to improve based on feedback...")
            
            # Re-generate strategy with improvement suggestions
            strategy_data = self._iterate_strategy(
                product_data, 
                research_data, 
                strategy_data,
                evaluation_data
            )
            
            # Re-evaluate
            evaluation_data = self.evaluator_agent.evaluate_full_plan(
                product_data, 
                research_data, 
                strategy_data
            )
            iteration_count += 1
            print(f"\n✅ Iteration completed! New score: {evaluation_data.get('overall_score', 0):.1f}/10")
        
        # Phase 4: Compile Final Plan
        print("\n" + "=" * 80)
        print("PHASE 5: COMPILING FINAL MARKETING PLAN")
        print("=" * 80)
        marketing_plan = self._compile_final_plan(
            product_data,
            research_data,
            strategy_data,
            evaluation_data,
            iteration_count
        )
        
        print("\n" + "=" * 80)
        print("✅ MARKETING PLAN GENERATION COMPLETED!")
        print("=" * 80)
        print(f"Overall Quality Score: {evaluation_data.get('overall_score', 0):.1f}/10")
        print(f"Sections Generated: {len(marketing_plan.get('sections', {}))}/12")
        print(f"Total Iterations: {iteration_count}")
        print("=" * 80)
        
        return marketing_plan
    
    def _iterate_strategy(
        self,
        product_data: Dict,
        research_data: Dict,
        current_strategy: Dict,
        evaluation: Dict
    ) -> Dict:
        """
        Improve strategy based on evaluation feedback.
        
        Returns:
            Improved strategy data
        """
        # For now, we'll re-generate the strategy
        # In a more sophisticated version, we could provide the feedback to the LLM
        print("  🔄 Re-generating strategy with improvements...")
        
        # Add improvement context to product data
        enhanced_product_data = product_data.copy()
        enhanced_product_data['_improvement_notes'] = {
            'weaknesses': evaluation.get('weaknesses', [])[:3],
            'suggestions': evaluation.get('improvement_suggestions', [])[:3],
            'focus_areas': evaluation.get('final_recommendations', [])[:2]
        }
        
        return self.strategy_agent.develop_full_strategy(enhanced_product_data, research_data)
    
    def _compile_final_plan(
        self,
        product_data: Dict,
        research_data: Dict,
        strategy_data: Dict,
        evaluation_data: Dict,
        iterations: int
    ) -> Dict:
        """
        Compile all data into a structured 12-section marketing plan.
        
        Returns:
            Complete marketing plan document
        """
        print("  📝 Compiling 12-section marketing plan...")
        
        marketing_plan = {
            "metadata": {
                "product_name": product_data.get('product_name', 'Unknown Product'),
                "generated_at": datetime.now().isoformat(),
                "version": f"1.{iterations}",
                "quality_score": evaluation_data.get('overall_score', 0),
                "status": "draft"
            },
            "sections": {
                "1_executive_summary": self._build_section_1(product_data, strategy_data),
                "2_mission_vision_value": self._build_section_2(strategy_data),
                "3_situation_market_analysis": self._build_section_3(research_data),
                "4_swot_analysis": self._build_section_4(research_data),
                "5_target_audience_positioning": self._build_section_5(research_data, strategy_data),
                "6_marketing_goals_kpis": self._build_section_6(strategy_data),
                "7_strategy_marketing_mix": self._build_section_7(strategy_data),
                "8_tactics_action_plan": self._build_section_8(strategy_data),
                "9_budget_resources": self._build_section_9(strategy_data),
                "10_monitoring_evaluation": self._build_section_10(strategy_data),
                "11_risks_mitigation": self._build_section_11(strategy_data),
                "12_launch_strategy": self._build_section_12(strategy_data)
            },
            "evaluation": {
                "overall_score": evaluation_data.get('overall_score', 0),
                "criterion_scores": evaluation_data.get('criterion_scores', {}),
                "strengths": evaluation_data.get('strengths', []),
                "weaknesses": evaluation_data.get('weaknesses', []),
                "recommendations": evaluation_data.get('final_recommendations', [])
            },
            "raw_data": {
                "research": research_data,
                "strategy": strategy_data,
                "evaluation": evaluation_data
            }
        }
        
        print("  ✅ All 12 sections compiled!")
        return marketing_plan
    
    def _build_section_1(self, product_data: Dict, strategy_data: Dict) -> Dict:
        """Section 1: Executive Summary"""
        exec_summary = strategy_data.get('executive_summary', {})
        return {
            "title": "Executive Summary",
            "content": {
                "product_overview": exec_summary.get('overview', ''),
                "market_opportunity": exec_summary.get('market_opportunity', ''),
                "target_audience": exec_summary.get('target', ''),
                "strategic_approach": exec_summary.get('strategy', ''),
                "expected_outcomes": exec_summary.get('expected_outcomes', '')
            }
        }
    
    def _build_section_2(self, strategy_data: Dict) -> Dict:
        """Section 2: Mission, Vision, and Value Proposition"""
        mvv = strategy_data.get('mission_vision_value', {})
        return {
            "title": "Mission, Vision, and Value Proposition",
            "content": {
                "mission": mvv.get('mission', ''),
                "vision": mvv.get('vision', ''),
                "value_proposition": mvv.get('value_proposition', ''),
                "core_values": mvv.get('core_values', [])
            }
        }
    
    def _build_section_3(self, research_data: Dict) -> Dict:
        """Section 3: Situation and Market Analysis"""
        market = research_data.get('market_analysis', {})
        trends = research_data.get('trends', {})
        competitors = research_data.get('competitor_analysis', {})
        
        return {
            "title": "Situation and Market Analysis",
            "content": {
                "market_overview": {
                    "market_size": market.get('market_size', ''),
                    "growth_potential": market.get('growth_potential', ''),
                    "maturity_stage": market.get('maturity_stage', ''),
                    "market_segments": market.get('segments', [])
                },
                "market_trends": {
                    "current_trends": trends.get('current_trends', []),
                    "emerging_trends": trends.get('emerging_trends', []),
                    "consumer_trends": trends.get('consumer_trends', []),
                    "technology_trends": trends.get('technology_trends', [])
                },
                "competitive_landscape": {
                    "key_competitors": competitors.get('competitors', []),
                    "competitive_intensity": competitors.get('competitive_intensity', ''),
                    "market_gaps": competitors.get('gaps', [])
                }
            }
        }
    
    def _build_section_4(self, research_data: Dict) -> Dict:
        """Section 4: SWOT Analysis"""
        swot = research_data.get('swot_analysis', {})
        return {
            "title": "SWOT Analysis",
            "content": {
                "strengths": swot.get('strengths', []),
                "weaknesses": swot.get('weaknesses', []),
                "opportunities": swot.get('opportunities', []),
                "threats": swot.get('threats', [])
            }
        }
    
    def _build_section_5(self, research_data: Dict, strategy_data: Dict) -> Dict:
        """Section 5: Target Audience and Positioning"""
        audience = research_data.get('target_audience', {})
        personas = research_data.get('personas', [])
        positioning = strategy_data.get('positioning', {})
        messaging = strategy_data.get('messaging', {})
        
        return {
            "title": "Target Audience and Positioning",
            "content": {
                "target_audience": {
                    "primary_segment": audience.get('primary_segment', ''),
                    "secondary_segments": audience.get('secondary_segments', []),
                    "audience_size": audience.get('audience_size', ''),
                    "characteristics": audience.get('characteristics', []),
                    "pain_points": audience.get('pain_points', []),
                    "motivations": audience.get('motivations', [])
                },
                "buyer_personas": personas,
                "positioning": {
                    "positioning_statement": positioning.get('positioning_statement', ''),
                    "competitive_positioning": positioning.get('competitive_positioning', ''),
                    "positioning_pillars": positioning.get('positioning_pillars', []),
                    "perceptual_map": positioning.get('perceptual_map_axes', {})
                },
                "messaging": {
                    "tone_of_voice": messaging.get('tone_of_voice', {}),
                    "key_messages": messaging.get('key_messages', []),
                    "messaging_pillars": messaging.get('messaging_pillars', []),
                    "tagline_options": messaging.get('tagline_options', [])
                }
            }
        }
    
    def _build_section_6(self, strategy_data: Dict) -> Dict:
        """Section 6: Marketing Goals and KPIs"""
        goals = strategy_data.get('marketing_goals', {})
        return {
            "title": "Marketing Goals and KPIs",
            "content": {
                "primary_goals": goals.get('primary_goals', []),
                "short_term_goals": goals.get('short_term_goals', []),
                "long_term_goals": goals.get('long_term_goals', []),
                "success_criteria": goals.get('success_criteria', [])
            }
        }
    
    def _build_section_7(self, strategy_data: Dict) -> Dict:
        """Section 7: Strategy and Marketing Mix (7Ps)"""
        mix = strategy_data.get('marketing_mix', {})
        return {
            "title": "Strategy and Marketing Mix",
            "content": {
                "product": mix.get('product', {}),
                "price": mix.get('price', {}),
                "place": mix.get('place', {}),
                "promotion": mix.get('promotion', {}),
                "people": mix.get('people', {}),
                "process": mix.get('process', {}),
                "physical_evidence": mix.get('physical_evidence', {})
            }
        }
    
    def _build_section_8(self, strategy_data: Dict) -> Dict:
        """Section 8: Tactics and Action Plan"""
        action_plan = strategy_data.get('action_plan', {})
        return {
            "title": "Tactics and Action Plan",
            "content": {
                "pre_launch": action_plan.get('pre_launch', []),
                "launch": action_plan.get('launch', []),
                "post_launch": action_plan.get('post_launch', [])
            }
        }
    
    def _build_section_9(self, strategy_data: Dict) -> Dict:
        """Section 9: Budget and Resources"""
        budget = strategy_data.get('budget', {})
        return {
            "title": "Budget and Resources",
            "content": {
                "total_budget": budget.get('total_budget', ''),
                "budget_breakdown": budget.get('budget_breakdown', {}),
                "phase_allocation": budget.get('phase_allocation', {}),
                "roi_projections": budget.get('roi_projections', {}),
                "resource_requirements": budget.get('resource_requirements', [])
            }
        }
    
    def _build_section_10(self, strategy_data: Dict) -> Dict:
        """Section 10: Monitoring and Evaluation"""
        monitoring = strategy_data.get('monitoring', {})
        return {
            "title": "Monitoring and Evaluation",
            "content": {
                "key_metrics": monitoring.get('key_metrics', {}),
                "tracking_tools": monitoring.get('tracking_tools', []),
                "reporting_schedule": monitoring.get('reporting_schedule', {}),
                "review_milestones": monitoring.get('review_milestones', []),
                "success_thresholds": monitoring.get('success_thresholds', {})
            }
        }
    
    def _build_section_11(self, strategy_data: Dict) -> Dict:
        """Section 11: Risks and Mitigation"""
        risks = strategy_data.get('risks', {})
        return {
            "title": "Risks and Mitigation",
            "content": {
                "identified_risks": risks.get('risks', [])
            }
        }
    
    def _build_section_12(self, strategy_data: Dict) -> Dict:
        """Section 12: Launch Strategy"""
        launch = strategy_data.get('launch_strategy', {})
        return {
            "title": "Launch Strategy",
            "content": {
                "launch_approach": launch.get('launch_approach', ''),
                "pre_launch_phase": launch.get('pre_launch', {}),
                "launch_phase": launch.get('launch_phase', {}),
                "post_launch_phase": launch.get('post_launch_phase', {}),
                "adoption_strategy": launch.get('adoption_strategy', {}),
                "timeline": launch.get('timeline', [])
            }
        }
    
    def save_plan_to_file(self, marketing_plan: Dict, output_path: str) -> str:
        """
        Save the marketing plan to a JSON file.
        
        Args:
            marketing_plan: The complete marketing plan
            output_path: Path where to save the file
            
        Returns:
            Path to the saved file
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(marketing_plan, f, indent=2, ensure_ascii=False)
            print(f"✅ Marketing plan saved to: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Error saving marketing plan: {e}")
            return ""
    
    def export_plan_to_markdown(self, marketing_plan: Dict, output_path: str) -> str:
        """
        Export the marketing plan to a readable Markdown file.
        
        Args:
            marketing_plan: The complete marketing plan
            output_path: Path where to save the markdown file
            
        Returns:
            Path to the saved file
        """
        try:
            md_content = self._generate_markdown(marketing_plan)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"✅ Marketing plan exported to: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Error exporting marketing plan: {e}")
            return ""
    
    def _generate_markdown(self, plan: Dict) -> str:
        """Generate markdown content from the marketing plan."""
        metadata = plan.get('metadata', {})
        sections = plan.get('sections', {})
        evaluation = plan.get('evaluation', {})
        
        md = f"""# Marketing Plan: {metadata.get('product_name', 'Unknown Product')}

**Generated:** {metadata.get('generated_at', '')}  
**Version:** {metadata.get('version', '1.0')}  
**Quality Score:** {evaluation.get('overall_score', 0):.1f}/10  

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Mission, Vision, and Value Proposition](#2-mission-vision-and-value-proposition)
3. [Situation and Market Analysis](#3-situation-and-market-analysis)
4. [SWOT Analysis](#4-swot-analysis)
5. [Target Audience and Positioning](#5-target-audience-and-positioning)
6. [Marketing Goals and KPIs](#6-marketing-goals-and-kpis)
7. [Strategy and Marketing Mix](#7-strategy-and-marketing-mix)
8. [Tactics and Action Plan](#8-tactics-and-action-plan)
9. [Budget and Resources](#9-budget-and-resources)
10. [Monitoring and Evaluation](#10-monitoring-and-evaluation)
11. [Risks and Mitigation](#11-risks-and-mitigation)
12. [Launch Strategy](#12-launch-strategy)

---

"""
        
        # Add each section
        for section_key in sorted(sections.keys()):
            section = sections[section_key]
            section_num = section_key.split('_')[0]
            md += f"\n## {section_num}. {section.get('title', '')}\n\n"
            md += self._format_section_content(section.get('content', {}))
            md += "\n---\n"
        
        # Add evaluation summary
        md += f"\n## Evaluation Summary\n\n"
        md += f"**Overall Score:** {evaluation.get('overall_score', 0):.1f}/10\n\n"
        
        if evaluation.get('strengths'):
            md += "### Strengths\n"
            for strength in evaluation.get('strengths', [])[:5]:
                md += f"- {strength}\n"
            md += "\n"
        
        if evaluation.get('recommendations'):
            md += "### Recommendations\n"
            for rec in evaluation.get('recommendations', []):
                md += f"- {rec}\n"
            md += "\n"
        
        return md
    
    def _format_section_content(self, content: Dict, level: int = 3) -> str:
        """Recursively format section content to markdown."""
        md = ""
        for key, value in content.items():
            header = key.replace('_', ' ').title()
            
            if isinstance(value, dict):
                md += f"{'#' * level} {header}\n\n"
                md += self._format_section_content(value, level + 1)
            elif isinstance(value, list):
                md += f"{'#' * level} {header}\n\n"
                for item in value:
                    if isinstance(item, dict):
                        md += self._format_dict_item(item)
                    else:
                        md += f"- {item}\n"
                md += "\n"
            else:
                md += f"**{header}:** {value}\n\n"
        
        return md
    
    def _format_dict_item(self, item: Dict) -> str:
        """Format a dictionary item for markdown."""
        md = ""
        for k, v in item.items():
            if isinstance(v, list):
                md += f"- **{k.replace('_', ' ').title()}:** {', '.join(str(x) for x in v)}\n"
            else:
                md += f"- **{k.replace('_', ' ').title()}:** {v}\n"
        md += "\n"
        return md


# Singleton instance
marketing_plan_orchestrator = MarketingPlanOrchestrator()
