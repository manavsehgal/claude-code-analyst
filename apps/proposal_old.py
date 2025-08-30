import streamlit as st
import os
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import re
import time
import requests
from claude_code_sdk import query, ClaudeCodeOptions

class ContentSource(Enum):
    LOCAL = "local"
    WORLD_KNOWLEDGE = "world_knowledge"
    ONLINE_RESEARCH = "online_research"

class AgentStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class ContentTracking:
    local_content: float = 0.0
    world_knowledge: float = 0.0
    online_research: float = 0.0
    
    def get_score_string(self) -> str:
        total = self.local_content + self.world_knowledge + self.online_research
        if total == 0:
            return "Content score: Not yet generated"
        local_pct = (self.local_content / total) * 100
        world_pct = (self.world_knowledge / total) * 100
        online_pct = (self.online_research / total) * 100
        return f"Content score: {local_pct:.0f}% local content, {world_pct:.0f}% world knowledge, {online_pct:.0f}% online research"

@dataclass
class AgentProgress:
    name: str
    status: AgentStatus = AgentStatus.PENDING
    progress: float = 0.0
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    error_message: Optional[str] = None
    
    def start(self):
        self.status = AgentStatus.IN_PROGRESS
        self.start_time = time.time()
        self.progress = 0.0
    
    def complete(self):
        self.status = AgentStatus.COMPLETED
        self.end_time = time.time()
        self.progress = 1.0
    
    def error(self, message: str):
        self.status = AgentStatus.ERROR
        self.end_time = time.time()
        self.error_message = message
    
    def get_duration(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

@dataclass
class ProposalSection:
    name: str
    description: str
    content: str = ""
    tracking: ContentTracking = field(default_factory=ContentTracking)
    generated: bool = False
    agent_progress: Optional[AgentProgress] = None

class BaseAgent:
    def __init__(self, use_local: bool, use_world: bool, use_online: bool):
        self.use_local = use_local
        self.use_world = use_world
        self.use_online = use_online
    
    def _calculate_content_weights(self, company_data: str, aws_data: str = "") -> ContentTracking:
        """Intelligently calculate content source weights based on data availability and quality"""
        tracking = ContentTracking()
        
        # Base weights
        local_weight = 0.0
        world_weight = 0.0
        online_weight = 0.0
        
        if self.use_local:
            # Calculate local content quality score
            local_quality = self._assess_local_content_quality(company_data, aws_data)
            local_weight = 0.3 + (local_quality * 0.6)  # 30-90% based on quality
        
        if self.use_world:
            # World knowledge weight varies inversely with local content quality
            world_weight = 0.4 if self.use_local else 0.7
            if self.use_local and company_data:
                world_weight = max(0.1, 0.5 - (len(company_data) / 10000))  # Reduce if lots of local data
        
        if self.use_online:
            # Online research fills gaps
            online_weight = 0.1 if (self.use_local and self.use_world) else 0.2
        
        # Normalize weights
        total_weight = local_weight + world_weight + online_weight
        if total_weight > 0:
            tracking.local_content = local_weight / total_weight
            tracking.world_knowledge = world_weight / total_weight
            tracking.online_research = online_weight / total_weight
        
        return tracking
    
    def _assess_local_content_quality(self, company_data: str, aws_data: str = "") -> float:
        """Assess the quality and relevance of local content (0.0-1.0)"""
        if not company_data:
            return 0.0
        
        quality_score = 0.0
        
        # Length factor (more content = potentially more insights)
        length_score = min(1.0, len(company_data) / 5000)
        quality_score += length_score * 0.3
        
        # Keyword relevance (AI, technology, strategy terms)
        relevant_keywords = [
            'artificial intelligence', 'AI', 'machine learning', 'automation',
            'technology', 'digital', 'data', 'analytics', 'cloud', 'innovation',
            'strategy', 'transformation', 'competitive', 'market', 'revenue'
        ]
        
        keyword_matches = sum(1 for keyword in relevant_keywords 
                             if keyword.lower() in company_data.lower())
        keyword_score = min(1.0, keyword_matches / len(relevant_keywords))
        quality_score += keyword_score * 0.4
        
        # Structure factor (presence of headers, sections)
        structure_indicators = ['##', '###', '####', '**', '*', '1.', '2.', '3.']
        structure_matches = sum(1 for indicator in structure_indicators 
                              if indicator in company_data)
        structure_score = min(1.0, structure_matches / 10)
        quality_score += structure_score * 0.3
        
        return min(1.0, quality_score)
    
    async def _perform_online_research(self, topic: str, company_name: str = "") -> str:
        """Simulate online research - in production this would use web APIs"""
        # This is a placeholder for online research functionality
        # In a real implementation, this might use search APIs, news APIs, etc.
        return f"Recent industry insights and trends related to {topic} and {company_name}"
    
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        raise NotImplementedError("Subclasses must implement generate_content")

class ExecutiveSummaryAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        # Use intelligent content scoring
        tracking = self._calculate_content_weights(company_data, aws_data)
        
        # Extract company name from data
        company_name = "the company"
        if company_data:
            first_line = company_data.split('\n')[0]
            company_name = first_line.strip('#').strip() or "the company"
        
        prompt_parts = []
        prompt_parts.append(f"Generate an executive summary for an AWS AI services proposal for {company_name}.")
        
        if self.use_local and company_data:
            prompt_parts.append(f"\n\nCompany Information:\n{company_data[:4000]}")
            if aws_data:
                prompt_parts.append(f"\n\nAWS AI Services Information:\n{aws_data[:3000]}")
        
        if self.use_world:
            prompt_parts.append("\n\nUse your knowledge of industry best practices and AI implementation strategies.")
        
        if self.use_online:
            # Perform online research
            research_results = await self._perform_online_research(f"AI adoption trends {company_name}", company_name)
            prompt_parts.append(f"\n\nRecent Market Research:\n{research_results}")
        
        prompt_parts.append("\n\nProvide a compelling executive summary that:")
        prompt_parts.append("1. Summarizes the key value proposition")
        prompt_parts.append("2. Highlights the most important benefits")
        prompt_parts.append("3. Provides a clear call to action")
        prompt_parts.append("Keep it concise but impactful (3-4 paragraphs).")
        
        try:
            final_prompt = " ".join(prompt_parts)
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            
            result_content = ""
            async for message in query(prompt=final_prompt, options=options):
                result_content += message
            
            return result_content.strip(), tracking
            
        except Exception as e:
            return f"Error generating executive summary: {str(e)}", tracking

class ProblemStatementAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        # Use intelligent content scoring
        tracking = self._calculate_content_weights(company_data, aws_data)
        
        prompt_parts = []
        prompt_parts.append("Analyze and articulate the company's problems, pain points, and strategic needs.")
        
        content_weight = 0
        if self.use_local and company_data:
            prompt_parts.append(f"\n\nCompany Information:\n{company_data}")
            tracking.local_content = 0.9
            content_weight += 0.9
        
        if self.use_world:
            prompt_parts.append("\n\nConsider typical challenges faced by companies in this industry.")
            tracking.world_knowledge = 0.1
            content_weight += 0.1
        
        prompt_parts.append("\n\nIdentify and analyze:")
        prompt_parts.append("1. Explicit problems and challenges stated")
        prompt_parts.append("2. Implicit/latent needs not directly mentioned")
        prompt_parts.append("3. Strategic pain points affecting growth")
        prompt_parts.append("4. Operational challenges that AI could address")
        prompt_parts.append("Provide specific examples and explain how AWS AI services could address each.")
        
        try:
            final_prompt = " ".join(prompt_parts)
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            
            result_content = ""
            async for message in query(prompt=final_prompt, options=options):
                result_content += message
            
            # Normalize tracking weights
            if content_weight > 0:
                tracking.local_content = tracking.local_content / content_weight
                tracking.world_knowledge = tracking.world_knowledge / content_weight
            
            return result_content.strip(), tracking
            
        except Exception as e:
            return f"Error generating problem statement: {str(e)}", tracking

class IndustryTrendsAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = ContentTracking()
        
        prompt_parts = []
        prompt_parts.append("Analyze relevant industry trends for the company's growth.")
        
        if self.use_local:
            prompt_parts.append(f"\n\nCompany Context:\n{company_data[:1500]}")
            tracking.local_content = 0.3
        
        if self.use_world:
            prompt_parts.append("\n\nInclude major industry trends and transformations.")
            tracking.world_knowledge = 0.5
        
        if self.use_online:
            prompt_parts.append("\n\nConsider recent market developments and emerging technologies.")
            tracking.online_research = 0.2
        
        try:
            final_prompt = " ".join(prompt_parts)
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            
            result_content = ""
            async for message in query(prompt=final_prompt, options=options):
                result_content += message
            
            return result_content.strip(), tracking
            
        except Exception as e:
            return f"Error generating industry trends analysis: {str(e)}", tracking

class CompetitionAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = ContentTracking()
        
        prompt_parts = []
        prompt_parts.append("Analyze competitive landscape and required responses.")
        
        if self.use_local:
            prompt_parts.append(f"\n\nCompany and Competition Info:\n{company_data}")
            tracking.local_content = 0.6
        
        if self.use_world:
            prompt_parts.append("\n\nAnalyze competitive AI adoption strategies in the industry.")
            tracking.world_knowledge = 0.3
        
        if self.use_online:
            prompt_parts.append("\n\nInclude recent competitive moves if relevant.")
            tracking.online_research = 0.1
        
        try:
            final_prompt = " ".join(prompt_parts)
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            
            result_content = ""
            async for message in query(prompt=final_prompt, options=options):
                result_content += message
            
            return result_content.strip(), tracking
            
        except Exception as e:
            return f"Error generating industry trends analysis: {str(e)}", tracking

class MarketSegmentsAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = ContentTracking()
        
        prompt_parts = []
        prompt_parts.append("Analyze market segments and opportunities.")
        
        if self.use_local:
            prompt_parts.append(f"\n\nCompany Information:\n{company_data}")
            tracking.local_content = 0.7
        
        if self.use_world:
            prompt_parts.append("\n\nIdentify market segment characteristics and growth potential.")
            tracking.world_knowledge = 0.3
        
        try:
            final_prompt = " ".join(prompt_parts)
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            
            result_content = ""
            async for message in query(prompt=final_prompt, options=options):
                result_content += message
            
            return result_content.strip(), tracking
            
        except Exception as e:
            return f"Error generating industry trends analysis: {str(e)}", tracking

class TechnologyStrategyAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = ContentTracking()
        
        prompt_parts = []
        prompt_parts.append("Analyze the company's technology strategy and recommend improvements.")
        
        if self.use_local:
            prompt_parts.append(f"\n\nCompany Tech Stack:\n{company_data}")
            tracking.local_content = 0.8
        
        if self.use_world:
            prompt_parts.append("\n\nSuggest modern technology patterns and best practices.")
            tracking.world_knowledge = 0.2
        
        try:
            final_prompt = " ".join(prompt_parts)
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            
            result_content = ""
            async for message in query(prompt=final_prompt, options=options):
                result_content += message
            
            return result_content.strip(), tracking
            
        except Exception as e:
            return f"Error generating competition analysis: {str(e)}", tracking

class AWSServicesAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = ContentTracking()
        
        prompt_parts = []
        prompt_parts.append("Match AWS AI services to company needs.")
        
        if self.use_local:
            prompt_parts.append(f"\n\nCompany Needs:\n{company_data}")
            prompt_parts.append(f"\n\nAWS AI Services:\n{aws_data}")
            tracking.local_content = 0.95
        
        if self.use_world:
            prompt_parts.append("\n\nExplain service benefits and integration patterns.")
            tracking.world_knowledge = 0.05
        
        prompt_parts.append("\n\nRecommend specific AWS services like SageMaker, Bedrock, Comprehend, etc. based on the company's needs.")
        
        try:
            final_prompt = " ".join(prompt_parts)
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            
            result_content = ""
            async for message in query(prompt=final_prompt, options=options):
                result_content += message
            
            return result_content.strip(), tracking
            
        except Exception as e:
            return f"Error generating industry trends analysis: {str(e)}", tracking

class AdoptionPlanAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = ContentTracking()
        
        prompt_parts = []
        prompt_parts.append("Create a phased adoption timeline for AWS AI services.")
        
        if self.use_local:
            prompt_parts.append(f"\n\nCompany Context:\n{company_data}")
            prompt_parts.append(f"\n\nAWS Services:\n{aws_data[:2000]}")
            tracking.local_content = 0.7
        
        if self.use_world:
            prompt_parts.append("\n\nInclude typical implementation timelines and milestones.")
            tracking.world_knowledge = 0.3
        
        prompt_parts.append("\n\nProvide a quarterly timeline with specific milestones and deliverables.")
        
        try:
            final_prompt = " ".join(prompt_parts)
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            
            result_content = ""
            async for message in query(prompt=final_prompt, options=options):
                result_content += message
            
            return result_content.strip(), tracking
            
        except Exception as e:
            return f"Error generating industry trends analysis: {str(e)}", tracking

class SpendAnalysisAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = ContentTracking()
        
        prompt_parts = []
        prompt_parts.append("Analyze AWS AI services pricing and predict spend.")
        
        if self.use_local:
            prompt_parts.append(f"\n\nCompany Scale:\n{company_data[:1500]}")
            prompt_parts.append(f"\n\nAWS Pricing Info:\n{aws_data[:2000]}")
            tracking.local_content = 0.6
        
        if self.use_world:
            prompt_parts.append("\n\nUse typical AWS pricing models and volume estimates.")
            tracking.world_knowledge = 0.4
        
        prompt_parts.append("\n\nProvide monthly and annual spend estimates with breakdown by service.")
        
        try:
            final_prompt = " ".join(prompt_parts)
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            
            result_content = ""
            async for message in query(prompt=final_prompt, options=options):
                result_content += message
            
            return result_content.strip(), tracking
            
        except Exception as e:
            return f"Error generating industry trends analysis: {str(e)}", tracking

class ROIAnalysisAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = ContentTracking()
        
        prompt_parts = []
        prompt_parts.append("Create a return on investment analysis.")
        
        if self.use_local:
            prompt_parts.append(f"\n\nCompany Business Metrics:\n{company_data[:1500]}")
            tracking.local_content = 0.5
        
        if self.use_world:
            prompt_parts.append("\n\nInclude typical ROI metrics for AI implementations.")
            tracking.world_knowledge = 0.5
        
        prompt_parts.append("\n\nShow spend vs returns timeline and break-even analysis.")
        
        try:
            final_prompt = " ".join(prompt_parts)
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            
            result_content = ""
            async for message in query(prompt=final_prompt, options=options):
                result_content += message
            
            return result_content.strip(), tracking
            
        except Exception as e:
            return f"Error generating industry trends analysis: {str(e)}", tracking

class ProposalOrchestrator:
    def __init__(self):
        self.sections = {
            "Executive Summary": ProposalSection(
                "Executive Summary", 
                "Elevator pitch and summary of the proposal"
            ),
            "Problem Statement": ProposalSection(
                "Problem Statement",
                "Problems, pain points, explicit asks, and latent needs"
            ),
            "Industry Trends": ProposalSection(
                "Industry Trends",
                "Relevant industry trends for company growth"
            ),
            "Competition": ProposalSection(
                "Competition",
                "Competitive landscape and required responses"
            ),
            "Market Segments": ProposalSection(
                "Market Segments",
                "Market segments and opportunity gaps"
            ),
            "Technology Strategy": ProposalSection(
                "Technology Strategy",
                "Current technology and strategic recommendations"
            ),
            "AWS AI Services": ProposalSection(
                "AWS AI Services",
                "Matching AWS AI services to company needs"
            ),
            "Adoption Plan": ProposalSection(
                "Adoption Plan",
                "Timeline for AWS AI services adoption"
            ),
            "Spend": ProposalSection(
                "Spend",
                "Monthly and annual spend predictions"
            ),
            "Returns": ProposalSection(
                "Returns",
                "Spend vs returns and break-even analysis"
            ),
        }
        
        self.agent_map = {
            "Executive Summary": ExecutiveSummaryAgent,
            "Problem Statement": ProblemStatementAgent,
            "Industry Trends": IndustryTrendsAgent,
            "Competition": CompetitionAgent,
            "Market Segments": MarketSegmentsAgent,
            "Technology Strategy": TechnologyStrategyAgent,
            "AWS AI Services": AWSServicesAgent,
            "Adoption Plan": AdoptionPlanAgent,
            "Spend": SpendAnalysisAgent,
            "Returns": ROIAnalysisAgent,
        }
    
    async def generate_section(self, section_name: str, company_data: str, aws_data: str, 
                               use_local: bool, use_world: bool, use_online: bool) -> ProposalSection:
        section = self.sections[section_name]
        section.agent_progress = AgentProgress(section_name)
        
        try:
            section.agent_progress.start()
            
            agent_class = self.agent_map[section_name]
            agent = agent_class(use_local, use_world, use_online)
            
            content, tracking = await agent.generate_content(company_data, aws_data, section)
            
            section.content = content
            section.tracking = tracking
            section.generated = True
            section.agent_progress.complete()
            
        except Exception as e:
            section.agent_progress.error(str(e))
            section.content = f"Error generating {section_name}: {str(e)}"
            section.generated = False
        
        return section

def load_company_data(company_name: str) -> str:
    company_dir = Path("companies") / company_name
    if company_dir.exists():
        md_files = list(company_dir.glob("*.md"))
        combined_content = []
        for md_file in md_files:
            combined_content.append(f"### {md_file.name}\n")
            combined_content.append(md_file.read_text())
            combined_content.append("\n\n")
        return "\n".join(combined_content)
    return ""

def load_aws_data() -> str:
    aws_path = Path("projects/llm-architectures-on-aws/report-03.md")
    if aws_path.exists():
        return aws_path.read_text()
    return ""

def save_proposal(company_name: str, sections: Dict[str, ProposalSection]):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    proposals_dir = Path("proposals") / company_name
    proposals_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"proposal-{timestamp}.md"
    filepath = proposals_dir / filename
    
    content = [f"# AWS AI Services Proposal for {company_name.title()}\n"]
    content.append(f"Generated: {datetime.now().strftime('%B %d, %Y')}\n\n")
    
    for section_name, section in sections.items():
        if section.generated:
            content.append(f"## {section_name}\n\n")
            content.append(f"*{section.tracking.get_score_string()}*\n\n")
            content.append(f"{section.content}\n\n")
    
    filepath.write_text("\n".join(content))
    return filepath

def main():
    st.set_page_config(page_title="AWS AI Proposal Generator", layout="wide")
    
    st.title("AWS AI Services Proposal Generator")
    st.markdown("Generate tailored proposals matching company needs with AWS AI offerings")
    
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = ProposalOrchestrator()
    
    if "generated_sections" not in st.session_state:
        st.session_state.generated_sections = {}
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Configuration")
        
        companies_dir = Path("companies")
        company_folders = [f for f in companies_dir.iterdir() if f.is_dir()] if companies_dir.exists() else []
        
        if not company_folders:
            st.error("No company folders found in companies/ directory")
            return
        
        company_names = [f.name for f in company_folders]
        selected_company = st.selectbox("Select Company", company_names)
        
        st.subheader("Proposal Sections")
        selected_sections = []
        for section_name in st.session_state.orchestrator.sections.keys():
            if st.checkbox(section_name, value=True):
                selected_sections.append(section_name)
        
        st.subheader("Content Sources")
        use_local = st.checkbox("Use local content (companys/ folder)", value=True)
        use_world = st.checkbox("Use LLM world knowledge", value=True)
        use_online = st.checkbox("Use online research", value=False)
        
        if not (use_local or use_world or use_online):
            st.error("Please select at least one content source")
        
        if st.button("Generate Proposal", type="primary", disabled=not selected_sections):
            company_data = load_company_data(selected_company)
            aws_data = load_aws_data()
            
            if not company_data:
                st.error("Failed to load company data")
                return
            
            if not aws_data:
                st.warning("AWS data not found, continuing with limited information")
            
            progress_container = st.container()
            with progress_container:
                st.subheader("Agent Progress")
                progress_placeholders = {}
                for section_name in selected_sections:
                    progress_placeholders[section_name] = st.empty()
            
            overall_progress = st.progress(0)
            status_text = st.empty()
            
            async def generate_all_sections():
                results = {}
                total = len(selected_sections)
                
                for idx, section_name in enumerate(selected_sections):
                    status_text.text(f"Starting agent for {section_name}...")
                    
                    # Initialize progress display
                    with progress_placeholders[section_name]:
                        st.info(f"🤖 {section_name} Agent: Starting...")
                    
                    section = await st.session_state.orchestrator.generate_section(
                        section_name, company_data, aws_data,
                        use_local, use_world, use_online
                    )
                    
                    # Update progress display
                    if section.agent_progress:
                        duration = section.agent_progress.get_duration()
                        if section.agent_progress.status == AgentStatus.COMPLETED:
                            with progress_placeholders[section_name]:
                                st.success(f"✅ {section_name} Agent: Completed in {duration:.1f}s")
                        elif section.agent_progress.status == AgentStatus.ERROR:
                            with progress_placeholders[section_name]:
                                st.error(f"❌ {section_name} Agent: Error - {section.agent_progress.error_message}")
                    
                    results[section_name] = section
                    overall_progress.progress((idx + 1) / total)
                
                return results
            
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                st.session_state.generated_sections = loop.run_until_complete(generate_all_sections())
                
                status_text.text("Saving proposal...")
                filepath = save_proposal(selected_company, st.session_state.generated_sections)
                
                status_text.success(f"Proposal saved to {filepath}")
                progress_bar.progress(1.0)
                
            except Exception as e:
                st.error(f"Error generating proposal: {str(e)}")
    
    with col2:
        st.subheader("Generated Proposal")
        
        if st.session_state.generated_sections:
            # Show summary metrics
            completed_sections = [s for s in st.session_state.generated_sections.values() if s.generated]
            total_sections = len(st.session_state.generated_sections)
            
            if completed_sections:
                avg_duration = sum(s.agent_progress.get_duration() or 0 for s in completed_sections) / len(completed_sections)
                st.metric("Sections Generated", f"{len(completed_sections)}/{total_sections}", f"Avg: {avg_duration:.1f}s")
            
            # Show sections with enhanced info
            for section_name, section in st.session_state.generated_sections.items():
                if section.generated:
                    # Create enhanced title with metrics
                    duration_text = ""
                    if section.agent_progress and section.agent_progress.get_duration():
                        duration_text = f" | ⏱️ {section.agent_progress.get_duration():.1f}s"
                    
                    title = f"{section_name} - {section.tracking.get_score_string()}{duration_text}"
                    
                    with st.expander(title, expanded=True):
                        # Show agent performance metrics
                        if section.agent_progress:
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.caption(f"Agent: {section.agent_progress.status.value.title()}")
                            with col_b:
                                if section.agent_progress.get_duration():
                                    st.caption(f"Duration: {section.agent_progress.get_duration():.1f}s")
                            with col_c:
                                st.caption(f"Content Sources: {'Local' if use_local else ''} {'World' if use_world else ''} {'Online' if use_online else ''}")
                        
                        st.markdown("---")
                        st.markdown(section.content)
        else:
            st.info("Select sections and click 'Generate Proposal' to begin")

if __name__ == "__main__":
    main()