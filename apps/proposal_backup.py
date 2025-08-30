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
    STARTING = "starting"
    ACTIVE = "active"
    PROCESSING = "processing"
    COMPLETING = "completing"
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
        self.status = AgentStatus.STARTING
        self.start_time = time.time()
        self.progress = 0.1

    def set_active(self):
        self.status = AgentStatus.ACTIVE
        self.progress = 0.3
    
    def set_processing(self):
        self.status = AgentStatus.PROCESSING
        self.progress = 0.6
    
    def set_completing(self):
        self.status = AgentStatus.COMPLETING
        self.progress = 0.9

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
    
    def _extract_message_content(self, message) -> str:
        """Extract content from message object, handling both strings and SystemMessage objects"""
        if hasattr(message, 'content'):
            return str(message.content)
        elif hasattr(message, 'text'):
            return str(message.text)
        else:
            return str(message)

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
                result_content += self._extract_message_content(message)

            return result_content.strip(), tracking

        except Exception as e:
            return f"Error generating executive summary: {str(e)}", tracking

# Simplified agent implementations for other sections (using similar pattern)
class ProblemStatementAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = self._calculate_content_weights(company_data, aws_data)
        # Implementation similar to ExecutiveSummaryAgent...
        try:
            prompt = f"Analyze company problems and pain points based on: {company_data[:2000]}"
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            result_content = ""
            async for message in query(prompt=prompt, options=options):
                result_content += self._extract_message_content(message)
            return result_content.strip(), tracking
        except Exception as e:
            return f"Error generating problem statement: {str(e)}", tracking

# Additional agent classes follow same pattern...
class IndustryTrendsAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = self._calculate_content_weights(company_data, aws_data)
        try:
            prompt = f"Analyze industry trends relevant to: {company_data[:2000]}"
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            result_content = ""
            async for message in query(prompt=prompt, options=options):
                result_content += self._extract_message_content(message)
            return result_content.strip(), tracking
        except Exception as e:
            return f"Error generating industry trends: {str(e)}", tracking

# Simplified implementations for remaining agents
class CompetitionAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = self._calculate_content_weights(company_data, aws_data)
        try:
            prompt = f"Analyze competitive landscape for: {company_data[:2000]}"
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            result_content = ""
            async for message in query(prompt=prompt, options=options):
                result_content += self._extract_message_content(message)
            return result_content.strip(), tracking
        except Exception as e:
            return f"Error generating competition analysis: {str(e)}", tracking

class MarketSegmentsAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = self._calculate_content_weights(company_data, aws_data)
        try:
            prompt = f"Analyze market segments and opportunities for: {company_data[:2000]}"
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            result_content = ""
            async for message in query(prompt=prompt, options=options):
                result_content += self._extract_message_content(message)
            return result_content.strip(), tracking
        except Exception as e:
            return f"Error generating market segments analysis: {str(e)}", tracking

class TechnologyStrategyAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = self._calculate_content_weights(company_data, aws_data)
        try:
            prompt = f"Analyze technology strategy for: {company_data[:2000]}"
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            result_content = ""
            async for message in query(prompt=prompt, options=options):
                result_content += self._extract_message_content(message)
            return result_content.strip(), tracking
        except Exception as e:
            return f"Error generating technology strategy: {str(e)}", tracking

class AWSServicesAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = self._calculate_content_weights(company_data, aws_data)
        try:
            prompt = f"Match AWS AI services to company needs: {company_data[:2000]}\n\nAWS Services: {aws_data[:3000]}"
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            result_content = ""
            async for message in query(prompt=prompt, options=options):
                result_content += self._extract_message_content(message)
            return result_content.strip(), tracking
        except Exception as e:
            return f"Error generating AWS services analysis: {str(e)}", tracking

class AdoptionPlanAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = self._calculate_content_weights(company_data, aws_data)
        try:
            prompt = f"Create adoption timeline for AWS AI services based on: {company_data[:2000]}"
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            result_content = ""
            async for message in query(prompt=prompt, options=options):
                result_content += self._extract_message_content(message)
            return result_content.strip(), tracking
        except Exception as e:
            return f"Error generating adoption plan: {str(e)}", tracking

class SpendAnalysisAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = self._calculate_content_weights(company_data, aws_data)
        try:
            prompt = f"Analyze AWS spending and pricing for: {company_data[:2000]}"
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            result_content = ""
            async for message in query(prompt=prompt, options=options):
                result_content += self._extract_message_content(message)
            return result_content.strip(), tracking
        except Exception as e:
            return f"Error generating spend analysis: {str(e)}", tracking

class ROIAnalysisAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = self._calculate_content_weights(company_data, aws_data)
        try:
            prompt = f"Analyze ROI and returns for AWS AI investment: {company_data[:2000]}"
            options = ClaudeCodeOptions(model="claude-3-5-sonnet-20241022")
            result_content = ""
            async for message in query(prompt=prompt, options=options):
                result_content += self._extract_message_content(message)
            return result_content.strip(), tracking
        except Exception as e:
            return f"Error generating ROI analysis: {str(e)}", tracking

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
            # Start the agent
            section.agent_progress.start()
            
            # Set to active
            section.agent_progress.set_active()
            
            # Initialize agent
            agent_class = self.agent_map[section_name]
            agent = agent_class(use_local, use_world, use_online)
            
            # Set to processing
            section.agent_progress.set_processing()

            # Generate content
            content, tracking = await agent.generate_content(company_data, aws_data, section)

            # Set to completing
            section.agent_progress.set_completing()
            
            # Finalize
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
    if not company_name:
        return ""
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
    if not company_name:
        company_name = "unknown-company"
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

# UI Functions
def main():
    st.set_page_config(page_title="AWS AI Proposal Generator", layout="wide")

    # Initialize session state
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = ProposalOrchestrator()

    if "generated_sections" not in st.session_state:
        st.session_state.generated_sections = {}

    if "current_step" not in st.session_state:
        st.session_state.current_step = 1

    if "company_data" not in st.session_state:
        st.session_state.company_data = ""

    if "aws_data" not in st.session_state:
        st.session_state.aws_data = ""

    # Main title
    st.title("🤖 AWS AI Services Proposal Generator")
    st.markdown("Generate tailored proposals matching company needs with AWS AI offerings")

    # Progress indicator
    progress_steps = ["Configuration", "Generation", "Review & Export"]
    current_step = st.session_state.current_step

    # Create progress bar
    progress_cols = st.columns(len(progress_steps))
    for i, (col, step) in enumerate(zip(progress_cols, progress_steps), 1):
        with col:
            if i < current_step:
                st.success(f"✅ {i}. {step}")
            elif i == current_step:
                st.info(f"🔄 {i}. {step}")
            else:
                st.write(f"⏳ {i}. {step}")

    st.markdown("---")

    # Step routing
    if current_step == 1:
        show_configuration_step()
    elif current_step == 2:
        show_generation_step()
    elif current_step == 3:
        show_review_step()

def show_configuration_step():
    st.subheader("📋 Step 1: Configuration")

    # Company Selection
    with st.container():
        st.markdown("### 🏢 Select Target Company")

        companies_dir = Path("companies")
        company_folders = [f for f in companies_dir.iterdir() if f.is_dir()] if companies_dir.exists() else []

        if not company_folders:
            st.error("No company folders found in companies/ directory")
            st.info("Please add company data folders to the companies/ directory before proceeding.")
            return

        company_names = [f.name for f in company_folders]
        
        # Get previously selected company for default selection
        previous_selection = st.session_state.get("selected_company")
        default_index = 0
        if previous_selection and previous_selection in company_names:
            default_index = company_names.index(previous_selection)
        
        selected_company = st.selectbox(
            "Choose a company for proposal generation:",
            company_names,
            index=default_index,
            key="company_selectbox",
            help="Select the target company for your AWS AI services proposal"
        )
        
        # Store the selected company in session state for use across steps
        if selected_company:
            st.session_state.selected_company = selected_company
        
        # Debug information (can be removed in production)
        with st.expander("🔧 Debug Info", expanded=False):
            st.write("Current session state:")
            st.write(f"- selected_company: {st.session_state.get('selected_company', 'None')}")
            st.write(f"- company_data length: {len(st.session_state.get('company_data', ''))}")
            st.write(f"- current_step: {st.session_state.get('current_step', 'None')}")

        # Load and preview company data
        if selected_company:
            try:
                company_data = load_company_data(selected_company)
                st.session_state.company_data = company_data
                st.session_state.aws_data = load_aws_data()

                if company_data:
                    with st.expander(f"📄 Preview {selected_company.title()} Data", expanded=False):
                        st.text(f"Data length: {len(company_data):,} characters")
                        st.text_area("Company information preview:", company_data[:500] + "...", height=100, disabled=True)
                else:
                    st.warning(f"No data found for {selected_company}. Please check the company folder.")
            except Exception as e:
                st.error(f"Error loading company data: {str(e)}")
                st.session_state.company_data = ""
        else:
            # Clear company data if no company selected
            st.session_state.company_data = ""

    st.markdown("---")

    # Proposal Sections Selection
    with st.container():
        st.markdown("### 📝 Select Proposal Sections")
        st.markdown("Choose which sections to include in your proposal:")

        # Create a more organized section selection
        sections_cols = st.columns(2)
        selected_sections = []

        section_items = list(st.session_state.orchestrator.sections.items())
        mid_point = len(section_items) // 2

        with sections_cols[0]:
            for section_name, section in section_items[:mid_point]:
                if st.checkbox(section_name, value=True, key=f"section_{section_name}"):
                    selected_sections.append(section_name)
                st.caption(section.description)

        with sections_cols[1]:
            for section_name, section in section_items[mid_point:]:
                if st.checkbox(section_name, value=True, key=f"section_{section_name}"):
                    selected_sections.append(section_name)
                st.caption(section.description)

        # Store all selected sections
        all_selected_sections = []
        for section_name in st.session_state.orchestrator.sections.keys():
            if st.session_state.get(f"section_{section_name}", True):
                all_selected_sections.append(section_name)

        st.session_state.selected_sections = all_selected_sections

        if all_selected_sections:
            st.success(f"Selected {len(all_selected_sections)} sections for generation")
        else:
            st.error("Please select at least one proposal section")

    st.markdown("---")

    # Content Sources Configuration
    with st.container():
        st.markdown("### 🔍 Content Sources")
        st.markdown("Configure which sources the AI agents should use:")

        source_cols = st.columns(3)

        with source_cols[0]:
            use_local = st.checkbox(
                "📁 Local Content",
                value=True,
                key="use_local",
                help="Use company profiles and AWS documentation from local files"
            )
            if use_local:
                st.success("✅ Company-specific data")

        with source_cols[1]:
            use_world = st.checkbox(
                "🌍 World Knowledge",
                value=True,
                key="use_world",
                help="Include AI model's knowledge of industry best practices"
            )
            if use_world:
                st.success("✅ Industry expertise")

        with source_cols[2]:
            use_online = st.checkbox(
                "🔍 Online Research",
                value=False,
                key="use_online",
                help="Include recent market trends and developments"
            )
            if use_online:
                st.info("🚧 Simulated research")

        if not (use_local or use_world or use_online):
            st.error("⚠️ Please select at least one content source")

        # Content quality preview
        if use_local and st.session_state.company_data:
            # Create a temporary agent to calculate weights
            temp_agent = ExecutiveSummaryAgent(use_local, use_world, use_online)
            quality_score = temp_agent._calculate_content_weights(
                st.session_state.company_data, st.session_state.aws_data
            )

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Local Content", f"{quality_score.local_content*100:.0f}%")
            with col_b:
                st.metric("World Knowledge", f"{quality_score.world_knowledge*100:.0f}%")
            with col_c:
                st.metric("Online Research", f"{quality_score.online_research*100:.0f}%")

    # Navigation
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col2:
        # Check if company is selected and data loaded
        company_selected = (st.session_state.get("selected_company") is not None and
                          st.session_state.get("company_data", "") != "")
        can_proceed = (all_selected_sections and 
                      (use_local or use_world or use_online) and 
                      company_selected)
        
        if not st.session_state.get("selected_company"):
            st.error("⚠️ Please select a company first")
        elif not st.session_state.get("company_data"):
            st.error("⚠️ No data loaded for selected company")
        
        if st.button("Next: Generate Proposal ➡️", type="primary", disabled=not can_proceed):
            st.session_state.current_step = 2
            st.rerun()

def show_generation_step():
    st.subheader("⚡ Step 2: Proposal Generation")

    # Get configuration from session state
    selected_company = st.session_state.get("selected_company")
    selected_sections = st.session_state.get("selected_sections", [])
    use_local = st.session_state.get("use_local", True)
    use_world = st.session_state.get("use_world", True)
    use_online = st.session_state.get("use_online", False)

    # Show configuration summary
    with st.container():
        st.markdown("### 📊 Generation Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Target Company", selected_company or "Not selected")
        with col2:
            st.metric("Sections Selected", len(selected_sections))
        with col3:
            sources = []
            if use_local: sources.append("Local")
            if use_world: sources.append("World")
            if use_online: sources.append("Online")
            st.metric("Content Sources", ", ".join(sources))

    st.markdown("---")

    # Generation controls
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Back to Config"):
            st.session_state.current_step = 1
            st.rerun()

    with col2:
        if st.button("🚀 Start Generation", type="primary", disabled=not (selected_sections and selected_company)):
            run_proposal_generation(selected_company, selected_sections, use_local, use_world, use_online)

    with col3:
        if st.session_state.generated_sections:
            if st.button("Next: Review ➡️", type="secondary"):
                st.session_state.current_step = 3
                st.rerun()

    # Show generation progress and results
    if "generation_in_progress" in st.session_state or st.session_state.generated_sections:
        show_generation_progress()

def run_proposal_generation(selected_company, selected_sections, use_local, use_world, use_online):
    """Run the proposal generation process"""
    if not selected_company:
        st.error("No company selected. Please go back and select a company.")
        return
        
    if not selected_sections:
        st.error("No sections selected. Please go back and select proposal sections.")
        return
        
    st.session_state.generation_in_progress = True

    company_data = st.session_state.company_data
    aws_data = st.session_state.aws_data

    if not company_data:
        st.error("Failed to load company data")
        return

    if not aws_data:
        st.warning("AWS data not found, continuing with limited information")

    # Progress tracking containers
    progress_container = st.container()
    with progress_container:
        st.subheader("🤖 Agent Progress")
        progress_placeholders = {}
        for section_name in selected_sections:
            progress_placeholders[section_name] = st.empty()

        overall_progress = st.progress(0)
        status_text = st.empty()

    async def generate_all_sections():
        results = {}
        total = len(selected_sections)
        
        # Initialize all agent progress displays
        for section_name in selected_sections:
            with progress_placeholders[section_name]:
                st.info(f"⏳ {section_name} Agent: Pending...")
        
        status_text.text(f"Starting all {total} agents in parallel...")
        
        # Create tasks for parallel execution
        tasks = []
        for section_name in selected_sections:
            task = st.session_state.orchestrator.generate_section(
                section_name, company_data, aws_data,
                use_local, use_world, use_online
            )
            tasks.append(task)
        
        # Monitor progress while tasks run
        completed_tasks = []
        pending_tasks = tasks.copy()
        
        # Use asyncio.as_completed to handle tasks as they finish
        import asyncio
        
        # Start progress monitoring
        progress_monitor_task = asyncio.create_task(monitor_agent_progress(
            selected_sections, progress_placeholders, overall_progress, status_text, total
        ))
        
        # Execute all agents in parallel
        try:
            sections = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for section_name, section in zip(selected_sections, sections):
                if isinstance(section, Exception):
                    # Handle any exceptions that occurred
                    st.error(f"Error in {section_name}: {section}")
                    # Create a failed section
                    failed_section = st.session_state.orchestrator.sections[section_name]
                    failed_section.generated = False
                    failed_section.content = f"Error: {section}"
                    results[section_name] = failed_section
                else:
                    results[section_name] = section
            
            # Cancel progress monitoring
            progress_monitor_task.cancel()
            
            # Final progress update
            status_text.text("All agents completed! Processing results...")
            overall_progress.progress(1.0)
            
            # Update final progress displays
            for section_name, section in results.items():
                if section.agent_progress:
                    duration = section.agent_progress.get_duration()
                    if section.agent_progress.status == AgentStatus.COMPLETED:
                        with progress_placeholders[section_name]:
                            st.success(f"✅ {section_name} Agent: Completed in {duration:.1f}s")
                    elif section.agent_progress.status == AgentStatus.ERROR:
                        with progress_placeholders[section_name]:
                            st.error(f"❌ {section_name} Agent: Error - {section.agent_progress.error_message}")
        
        except Exception as e:
            progress_monitor_task.cancel()
            status_text.error(f"Error in parallel execution: {str(e)}")
            
        return results
        
    async def monitor_agent_progress(section_names, progress_placeholders, overall_progress, status_text, total):
        """Monitor agent progress and update UI in real-time"""
        import asyncio
        
        while True:
            try:
                completed_count = 0
                active_agents = []
                
                for section_name in section_names:
                    section = st.session_state.orchestrator.sections[section_name]
                    if hasattr(section, 'agent_progress') and section.agent_progress:
                        progress = section.agent_progress
                        status = progress.status
                        
                        # Update individual agent display
                        with progress_placeholders[section_name]:
                            if status == AgentStatus.PENDING:
                                st.info(f"⏳ {section_name} Agent: Pending...")
                            elif status == AgentStatus.STARTING:
                                st.info(f"🚀 {section_name} Agent: Starting...")
                                active_agents.append(section_name)
                            elif status == AgentStatus.ACTIVE:
                                st.info(f"⚡ {section_name} Agent: Active...")
                                active_agents.append(section_name)
                            elif status == AgentStatus.PROCESSING:
                                st.warning(f"🔄 {section_name} Agent: Processing...")
                                active_agents.append(section_name)
                            elif status == AgentStatus.COMPLETING:
                                st.warning(f"🔧 {section_name} Agent: Completing...")
                                active_agents.append(section_name)
                            elif status == AgentStatus.COMPLETED:
                                duration = progress.get_duration()
                                st.success(f"✅ {section_name} Agent: Completed in {duration:.1f}s")
                                completed_count += 1
                            elif status == AgentStatus.ERROR:
                                st.error(f"❌ {section_name} Agent: Error - {progress.error_message}")
                                completed_count += 1
                
                # Update overall progress
                if total > 0:
                    overall_progress.progress(completed_count / total)
                
                # Update status text
                if active_agents:
                    status_text.text(f"Active agents: {', '.join(active_agents)} ({completed_count}/{total} complete)")
                else:
                    status_text.text(f"Progress: {completed_count}/{total} agents completed")
                
                # If all completed, break
                if completed_count >= total:
                    break
                    
                # Wait before next update
                await asyncio.sleep(0.5)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                # Continue monitoring even if there's an error
                await asyncio.sleep(0.5)

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        st.session_state.generated_sections = loop.run_until_complete(generate_all_sections())

        status_text.text("Saving proposal...")
        filepath = save_proposal(selected_company, st.session_state.generated_sections)

        status_text.success(f"Proposal saved to {filepath}")
        overall_progress.progress(1.0)

        # Clean up generation flag
        if "generation_in_progress" in st.session_state:
            del st.session_state.generation_in_progress

    except Exception as e:
        st.error(f"Error generating proposal: {str(e)}")
        if "generation_in_progress" in st.session_state:
            del st.session_state.generation_in_progress

def show_generation_progress():
    """Show generation progress and results"""
    if st.session_state.generated_sections:
        st.markdown("### ✅ Generation Complete")

        # Show summary metrics
        completed_sections = [s for s in st.session_state.generated_sections.values() if s.generated]
        total_sections = len(st.session_state.generated_sections)

        if completed_sections:
            avg_duration = sum(s.agent_progress.get_duration() or 0 for s in completed_sections) / len(completed_sections)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sections Generated", f"{len(completed_sections)}/{total_sections}")
            with col2:
                st.metric("Average Time", f"{avg_duration:.1f}s")
            with col3:
                success_rate = len(completed_sections) / total_sections * 100
                st.metric("Success Rate", f"{success_rate:.0f}%")

def show_review_step():
    st.subheader("📋 Step 3: Review & Export")

    # Navigation
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("⬅️ Back to Generation"):
            st.session_state.current_step = 2
            st.rerun()

    if not st.session_state.generated_sections:
        st.warning("No proposal sections generated yet. Please go back and generate a proposal first.")
        return

    # Show generated sections
    st.markdown("### 📄 Generated Proposal Sections")

    # Create tabs for sections
    section_names = [name for name, section in st.session_state.generated_sections.items() if section.generated]

    if section_names:
        # Add summary tab
        tabs = st.tabs(["📊 Summary"] + [f"📝 {name}" for name in section_names])

        # Summary tab
        with tabs[0]:
            show_proposal_summary()

        # Individual section tabs
        for i, section_name in enumerate(section_names, 1):
            with tabs[i]:
                show_section_content(section_name)

        # Export options
        st.markdown("---")
        st.markdown("### 💾 Export Options")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📄 Download Markdown", type="secondary"):
                download_proposal_markdown()
        with col2:
            if st.button("🔄 Generate New Proposal", type="secondary"):
                # Reset to step 1
                st.session_state.current_step = 1
                st.session_state.generated_sections = {}
                st.rerun()
        with col3:
            st.success("✅ Proposal Ready")

    else:
        st.info("No sections have been generated yet.")

def show_proposal_summary():
    """Show proposal generation summary"""
    completed_sections = [s for s in st.session_state.generated_sections.values() if s.generated]
    total_sections = len(st.session_state.generated_sections)

    if completed_sections:
        avg_duration = sum(s.agent_progress.get_duration() or 0 for s in completed_sections) / len(completed_sections)
        total_duration = sum(s.agent_progress.get_duration() or 0 for s in completed_sections)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Sections Generated", f"{len(completed_sections)}/{total_sections}")
        with col2:
            st.metric("Average Time", f"{avg_duration:.1f}s")
        with col3:
            st.metric("Total Time", f"{total_duration:.1f}s")
        with col4:
            success_rate = len(completed_sections) / total_sections * 100
            st.metric("Success Rate", f"{success_rate:.0f}%")

        st.markdown("---")

        # Content source breakdown
        st.markdown("### 📊 Content Sources Analysis")

        avg_local = sum(s.tracking.local_content for s in completed_sections) / len(completed_sections) * 100
        avg_world = sum(s.tracking.world_knowledge for s in completed_sections) / len(completed_sections) * 100
        avg_online = sum(s.tracking.online_research for s in completed_sections) / len(completed_sections) * 100

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Local Content", f"{avg_local:.0f}%")
        with col2:
            st.metric("World Knowledge", f"{avg_world:.0f}%")
        with col3:
            st.metric("Online Research", f"{avg_online:.0f}%")

def show_section_content(section_name):
    """Show individual section content"""
    section = st.session_state.generated_sections[section_name]

    if section.generated:
        # Section header with metrics
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"## {section_name}")
        with col2:
            if section.agent_progress and section.agent_progress.get_duration():
                st.metric("Generation Time", f"{section.agent_progress.get_duration():.1f}s")

        # Content scoring
        st.info(f"📊 {section.tracking.get_score_string()}")

        # Agent performance details
        if section.agent_progress:
            with st.expander("🤖 Agent Performance Details", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Status:** {section.agent_progress.status.value.title()}")
                with col2:
                    if section.agent_progress.get_duration():
                        st.write(f"**Duration:** {section.agent_progress.get_duration():.1f}s")
                with col3:
                    st.write(f"**Agent:** {section_name}Agent")

        st.markdown("---")

        # Section content
        st.markdown(section.content)

    else:
        st.error(f"Section {section_name} was not generated successfully.")
        if section.agent_progress and section.agent_progress.error_message:
            st.error(f"Error: {section.agent_progress.error_message}")

def download_proposal_markdown():
    """Generate and provide download for markdown proposal"""
    selected_company = st.session_state.get("selected_company", "Unknown")
    if not selected_company:
        selected_company = "Unknown"

    content = [f"# AWS AI Services Proposal for {selected_company.title()}\n"]
    content.append(f"Generated: {datetime.now().strftime('%B %d, %Y')}\n\n")

    for section_name, section in st.session_state.generated_sections.items():
        if section.generated:
            content.append(f"## {section_name}\n\n")
            content.append(f"*{section.tracking.get_score_string()}*\n\n")
            content.append(f"{section.content}\n\n")

    proposal_content = "\n".join(content)

    st.download_button(
        label="📥 Download Proposal (Markdown)",
        data=proposal_content,
        file_name=f"aws-ai-proposal-{selected_company or 'unknown'}-{datetime.now().strftime('%Y-%m-%d')}.md",
        mime="text/markdown"
    )

if __name__ == "__main__":
    main()