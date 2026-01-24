"""
Evaluator Agent - Assesses marketing strategy quality, consistency, and ethics
"""
import json
from typing import Dict, List
from ..llm_client import llm_client


class EvaluatorAgent:
    """
    AI Agent that evaluates marketing strategy and provides feedback.
    Assesses: Quality, consistency, originality, ethics, and provides improvement suggestions.
    """
    
    def __init__(self):
        self.llm = llm_client
        self.evaluation_criteria = {
            "consistency": "Alignment between sections, coherent narrative, no contradictions",
            "quality": "Depth of analysis, actionability, clarity, professional presentation",
            "originality": "Creative differentiation, unique positioning, innovative tactics",
            "feasibility": "Realistic goals, achievable tactics, appropriate budget allocation",
            "completeness": "All required sections present, comprehensive coverage",
            "ethics": "No misleading claims, respectful messaging, responsible practices"
        }
    
    def evaluate_full_plan(self, product_data: Dict, research_data: Dict, strategy_data: Dict) -> Dict:
        """
        Conduct comprehensive evaluation of the marketing plan.
        
        Args:
            product_data: Original product information
            research_data: Market research results
            strategy_data: Marketing strategy and tactics
            
        Returns:
            Evaluation report with scores, feedback, and improvement suggestions
        """
        print("🔍 Evaluating marketing plan...")
        
        evaluation = {
            "overall_score": 0,
            "criterion_scores": self.evaluate_criteria(product_data, research_data, strategy_data),
            "strengths": self.identify_strengths(strategy_data),
            "weaknesses": self.identify_weaknesses(strategy_data),
            "improvement_suggestions": self.generate_improvements(strategy_data),
            "consistency_check": self.check_consistency(research_data, strategy_data),
            "ethics_check": self.check_ethics(strategy_data),
            "alternatives": self.suggest_alternatives(product_data, strategy_data),
            "final_recommendations": []
        }
        
        # Calculate overall score
        scores = evaluation["criterion_scores"]
        evaluation["overall_score"] = sum(scores.values()) / len(scores)
        
        # Generate final recommendations
        evaluation["final_recommendations"] = self.generate_final_recommendations(evaluation)
        
        print(f"✅ Evaluation completed! Overall Score: {evaluation['overall_score']:.1f}/10")
        return evaluation
    
    def evaluate_criteria(self, product_data: Dict, research_data: Dict, strategy_data: Dict) -> Dict:
        """
        Evaluate the plan against key criteria.
        
        Returns:
            Scores (0-10) for each criterion
        """
        print("  📊 Evaluating against criteria...")
        
        # Prepare condensed data for evaluation
        plan_summary = self._create_plan_summary(product_data, research_data, strategy_data)
        
        prompt = f"""
Evaluate this marketing plan against the following criteria. Provide a score from 0-10 for each criterion.

MARKETING PLAN SUMMARY:
{plan_summary}

EVALUATION CRITERIA:
1. CONSISTENCY (0-10): {self.evaluation_criteria['consistency']}
2. QUALITY (0-10): {self.evaluation_criteria['quality']}
3. ORIGINALITY (0-10): {self.evaluation_criteria['originality']}
4. FEASIBILITY (0-10): {self.evaluation_criteria['feasibility']}
5. COMPLETENESS (0-10): {self.evaluation_criteria['completeness']}
6. ETHICS (0-10): {self.evaluation_criteria['ethics']}

For each criterion, provide:
- Score (0-10)
- Brief justification (1-2 sentences)

Format as JSON with keys: consistency, quality, originality, feasibility, completeness, ethics
Each value should be an object with: score (number), justification (string)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert marketing plan evaluator. Provide honest, constructive assessments. Be critical but fair. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.3)
        detailed_scores = self._parse_json_response(response, {})
        
        # Extract just the numeric scores for overall calculation
        scores = {}
        for criterion, data in detailed_scores.items():
            if isinstance(data, dict) and 'score' in data:
                scores[criterion] = data['score']
            else:
                scores[criterion] = 7.0  # Default score
        
        return scores
    
    def identify_strengths(self, strategy_data: Dict) -> List[str]:
        """
        Identify key strengths of the marketing plan.
        
        Returns:
            List of strengths
        """
        print("  💪 Identifying strengths...")
        
        strategy_summary = json.dumps(strategy_data, indent=2)[:3000]  # Truncate for token limit
        
        prompt = f"""
Analyze this marketing strategy and identify 5-7 key strengths:

{strategy_summary}

Look for:
- Strong strategic thinking
- Clear differentiation
- Well-defined target audience
- Innovative tactics
- Comprehensive approach
- Realistic planning
- Strong value proposition

Provide a list of specific strengths with brief explanations.

Format as JSON array of strings.
"""
        
        messages = [
            {"role": "system", "content": "You are an expert marketing analyst. Identify genuine strengths. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.5)
        return self._parse_json_response(response, [
            "Comprehensive market analysis",
            "Clear target audience definition",
            "Well-structured action plan"
        ])
    
    def identify_weaknesses(self, strategy_data: Dict) -> List[str]:
        """
        Identify weaknesses and gaps in the marketing plan.
        
        Returns:
            List of weaknesses
        """
        print("  🔍 Identifying weaknesses...")
        
        strategy_summary = json.dumps(strategy_data, indent=2)[:3000]
        
        prompt = f"""
Analyze this marketing strategy and identify 5-7 key weaknesses or gaps:

{strategy_summary}

Look for:
- Lack of clarity or specificity
- Unrealistic assumptions
- Missing elements
- Weak differentiation
- Budget concerns
- Implementation challenges
- Inconsistencies

Provide a list of specific weaknesses with brief explanations.

Format as JSON array of strings.
"""
        
        messages = [
            {"role": "system", "content": "You are an expert marketing critic. Identify real weaknesses constructively. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.5)
        return self._parse_json_response(response, [
            "Budget allocation could be more detailed",
            "Timeline may be optimistic",
            "Risk mitigation needs more specificity"
        ])
    
    def generate_improvements(self, strategy_data: Dict) -> List[Dict]:
        """
        Generate specific improvement suggestions.
        
        Returns:
            List of improvement recommendations with priority
        """
        print("  💡 Generating improvement suggestions...")
        
        strategy_summary = json.dumps(strategy_data, indent=2)[:3000]
        
        prompt = f"""
Based on this marketing strategy, provide 6-8 specific, actionable improvement suggestions:

{strategy_summary}

For each suggestion, provide:
- Area (which section/aspect to improve)
- Issue (what's the problem)
- Suggestion (specific improvement action)
- Priority (High/Medium/Low)
- Expected Impact (what will improve)

Format as JSON array of objects with keys: area, issue, suggestion, priority, expected_impact
"""
        
        messages = [
            {"role": "system", "content": "You are an expert marketing consultant. Provide actionable, specific improvements. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.6)
        return self._parse_json_response(response, [
            {
                "area": "General",
                "issue": "Needs more specificity",
                "suggestion": "Add more concrete details",
                "priority": "Medium",
                "expected_impact": "Improved clarity"
            }
        ])
    
    def check_consistency(self, research_data: Dict, strategy_data: Dict) -> Dict:
        """
        Check for consistency between research and strategy.
        
        Returns:
            Consistency report with issues and alignment score
        """
        print("  🔄 Checking consistency...")
        
        # Extract key elements for comparison
        target_audience_research = research_data.get('target_audience', {}).get('primary_segment', '')
        positioning = strategy_data.get('positioning', {}).get('positioning_statement', '')
        messaging = strategy_data.get('messaging', {}).get('key_messages', [])
        
        prompt = f"""
Check for consistency between market research and marketing strategy:

RESEARCH FINDINGS:
- Target Audience: {target_audience_research}
- Market Opportunities: {research_data.get('swot_analysis', {}).get('opportunities', [])}
- Market Threats: {research_data.get('swot_analysis', {}).get('threats', [])}

STRATEGY:
- Positioning: {positioning}
- Key Messages: {messaging}
- Marketing Goals: {strategy_data.get('marketing_goals', {}).get('primary_goals', [])}

Evaluate:
1. Does the strategy align with research findings?
2. Are target audience insights reflected in messaging?
3. Does positioning address identified opportunities?
4. Are threats adequately addressed in risk planning?
5. Are there any contradictions?

Provide:
- Consistency Score (0-10)
- Aligned Elements (what's consistent)
- Inconsistencies (what's misaligned)
- Recommendations (how to improve alignment)

Format as JSON with keys: consistency_score, aligned_elements (array), inconsistencies (array), recommendations (array)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert at strategic alignment analysis. Be thorough and specific. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.4)
        return self._parse_json_response(response, {
            "consistency_score": 8.0,
            "aligned_elements": ["Strategy aligns with research"],
            "inconsistencies": [],
            "recommendations": []
        })
    
    def check_ethics(self, strategy_data: Dict) -> Dict:
        """
        Check for ethical concerns in messaging and tactics.
        
        Returns:
            Ethics assessment with concerns and recommendations
        """
        print("  ⚖️ Checking ethical considerations...")
        
        messaging = strategy_data.get('messaging', {})
        promotions = strategy_data.get('marketing_mix', {}).get('promotion', {})
        
        prompt = f"""
Evaluate this marketing strategy for ethical considerations:

MESSAGING:
{json.dumps(messaging, indent=2)[:1000]}

PROMOTIONAL TACTICS:
{json.dumps(promotions, indent=2)[:1000]}

Check for:
1. Misleading or exaggerated claims
2. Manipulation or pressure tactics
3. Privacy concerns
4. Inclusivity and representation
5. Environmental/social responsibility
6. Transparency
7. Vulnerable audience protection

Provide:
- Ethics Score (0-10, where 10 is fully ethical)
- Concerns (any ethical issues identified)
- Positive Aspects (ethical strengths)
- Recommendations (how to improve ethics)

Format as JSON with keys: ethics_score, concerns (array), positive_aspects (array), recommendations (array)
"""
        
        messages = [
            {"role": "system", "content": "You are an expert in marketing ethics. Be vigilant but balanced. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.4)
        return self._parse_json_response(response, {
            "ethics_score": 9.0,
            "concerns": [],
            "positive_aspects": ["Transparent messaging", "Respectful approach"],
            "recommendations": []
        })
    
    def suggest_alternatives(self, product_data: Dict, strategy_data: Dict) -> Dict:
        """
        Suggest alternative approaches or tactics.
        
        Returns:
            Alternative strategies and tactics to consider
        """
        print("  🔀 Suggesting alternatives...")
        
        positioning = strategy_data.get('positioning', {})
        marketing_mix = strategy_data.get('marketing_mix', {})
        
        prompt = f"""
Based on this product and current strategy, suggest alternative approaches:

PRODUCT: {product_data.get('product_name', 'N/A')}
CURRENT POSITIONING: {positioning.get('positioning_statement', 'N/A')}
CURRENT CHANNELS: {marketing_mix.get('promotion', {}).get('strategy', 'N/A')}

Suggest alternatives for:
1. Positioning Strategy - Different angle or focus
2. Target Audience - Alternative or additional segments
3. Marketing Channels - Different channel mix
4. Campaign Concepts - 2-3 alternative creative directions
5. Launch Approach - Different launch strategy

For each alternative, explain:
- What's different
- Potential advantages
- Potential risks
- When to consider this approach

Format as JSON with keys: positioning_alternatives (array), audience_alternatives (array), channel_alternatives (array), campaign_alternatives (array), launch_alternatives (array)
"""
        
        messages = [
            {"role": "system", "content": "You are a creative marketing strategist. Provide innovative alternatives. Always respond with valid JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm.chat(messages, temperature=0.8)
        return self._parse_json_response(response, {
            "positioning_alternatives": [],
            "audience_alternatives": [],
            "channel_alternatives": [],
            "campaign_alternatives": [],
            "launch_alternatives": []
        })
    
    def generate_final_recommendations(self, evaluation: Dict) -> List[str]:
        """
        Generate prioritized final recommendations based on evaluation.
        
        Returns:
            List of prioritized recommendations
        """
        print("  📝 Generating final recommendations...")
        
        weaknesses = evaluation.get('weaknesses', [])
        improvements = evaluation.get('improvement_suggestions', [])
        consistency = evaluation.get('consistency_check', {})
        ethics = evaluation.get('ethics_check', {})
        
        recommendations = []
        
        # Add high-priority improvements
        high_priority = [imp for imp in improvements if imp.get('priority') == 'High']
        if high_priority:
            for imp in high_priority[:3]:  # Top 3
                recommendations.append(f"HIGH PRIORITY: {imp.get('suggestion', '')}")
        
        # Add consistency issues
        if consistency.get('inconsistencies'):
            recommendations.append(f"CONSISTENCY: {consistency['inconsistencies'][0]}")
        
        # Add ethics concerns
        if ethics.get('concerns'):
            recommendations.append(f"ETHICS: Address {ethics['concerns'][0]}")
        
        # Add general improvements
        medium_priority = [imp for imp in improvements if imp.get('priority') == 'Medium']
        if medium_priority and len(recommendations) < 5:
            for imp in medium_priority[:2]:
                recommendations.append(f"IMPROVE: {imp.get('suggestion', '')}")
        
        return recommendations[:6]  # Return top 6 recommendations
    
    def _create_plan_summary(self, product_data: Dict, research_data: Dict, strategy_data: Dict) -> str:
        """Create a condensed summary of the plan for evaluation."""
        summary_parts = [
            f"Product: {product_data.get('product_name', 'N/A')}",
            f"Target: {research_data.get('target_audience', {}).get('primary_segment', 'N/A')}",
            f"Positioning: {strategy_data.get('positioning', {}).get('positioning_statement', 'N/A')}",
            f"Goals: {len(strategy_data.get('marketing_goals', {}).get('primary_goals', []))} primary goals defined",
            f"Budget: {strategy_data.get('budget', {}).get('total_budget', 'N/A')}",
            f"Channels: {strategy_data.get('marketing_mix', {}).get('promotion', {}).get('strategy', 'N/A')}"
        ]
        return "\n".join(summary_parts)
    
    def _parse_json_response(self, response: str, fallback: any) -> any:
        """
        Parse JSON response from LLM, with fallback for malformed JSON.
        """
        try:
            # Try to find JSON in the response
            response = response.strip()
            
            # Remove markdown code blocks if present
            if response.startswith("```json"):
                response = response[7:]
            elif response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            
            response = response.strip()
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"    ⚠️  Warning: Could not parse JSON response. Using fallback. Error: {e}")
            return fallback


# Singleton instance
evaluator_agent = EvaluatorAgent()
