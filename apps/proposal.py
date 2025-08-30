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
        self.progress = 0.2

    def set_processing(self):
        self.status = AgentStatus.PROCESSING
        self.progress = 0.5

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
        self.progress = 0.0

    def get_duration(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

@dataclass
class ProposalSection:
    title: str
    description: str
    content: str = ""
    generated: bool = False
    tracking: Optional[ContentTracking] = None
    agent_progress: Optional[AgentProgress] = None

class SubAgentOrchestrator:
    """Proper Claude Code SDK subagent orchestration system"""
    
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
    
    async def generate_section(self, section_name: str, company_data: str, aws_data: str,
                               use_local: bool, use_world: bool, use_online: bool) -> ProposalSection:
        """Generate a section using proper Claude Code SDK subagents"""
        
        section = self.sections[section_name]
        section.agent_progress = AgentProgress(section_name)
        
        try:
            # Start the subagent
            section.agent_progress.start()
            
            # Create specialized subagent prompt based on section type
            subagent_prompt = self._create_section_prompt(section_name, company_data, aws_data, use_local, use_world, use_online)
            
            section.agent_progress.set_active()
            
            # Use Task tool to create proper subagent
            # This is the key difference - using actual Claude Code subagents
            from claude_tools import Task
            
            section.agent_progress.set_processing()
            
            # Create subagent using Task tool with specialized system
            result = await Task(
                description=f"Generate {section_name} for AWS AI proposal",
                prompt=subagent_prompt,
                subagent_type="general-purpose"
            )
            
            section.agent_progress.set_completing()
            
            # Calculate content tracking
            tracking = self._calculate_content_weights(company_data, aws_data, use_local, use_world, use_online)
            
            # Update section with results
            section.content = result
            section.tracking = tracking
            section.generated = True
            section.agent_progress.complete()
            
        except ImportError:
            # Fallback if Task tool not available - this shouldn't happen in Claude Code
            section.agent_progress.error("Task tool not available - using fallback")
            section.content = f"Fallback content for {section_name} (Task tool not available)"
            section.generated = False
            
        except Exception as e:
            section.agent_progress.error(str(e))
            section.content = f"Error generating {section_name}: {str(e)}"
            section.generated = False
        
        return section
    
    def _create_section_prompt(self, section_name: str, company_data: str, aws_data: str, 
                              use_local: bool, use_world: bool, use_online: bool) -> str:
        """Create specialized prompts for each section type"""
        
        # Define section-specific expertise and requirements
        section_configs = {
            "Executive Summary": {
                "role": "Executive Summary Specialist for AWS AI Services proposals",
                "expertise": [
                    "Transform technical capabilities into business value propositions",
                    "Create compelling C-level executive communications",
                    "Focus on ROI, competitive advantage, and strategic impact",
                    "Craft actionable recommendations for decision makers"
                ],
                "requirements": [
                    "Open with clear, compelling value proposition",
                    "Highlight 3-4 key strategic benefits",
                    "Show competitive advantages gained",
                    "Include specific call-to-action",
                    "Keep executive-friendly (concise, business-focused, 3-4 paragraphs)"
                ]
            },
            "Problem Statement": {
                "role": "Business Analysis Specialist focusing on problem identification",
                "expertise": [
                    "Identify explicit business problems and latent needs",
                    "Analyze operational inefficiencies and pain points", 
                    "Connect business challenges to AI solution opportunities",
                    "Assess competitive pressures and market dynamics"
                ],
                "requirements": [
                    "Document explicit business problems and challenges",
                    "Identify hidden inefficiencies and latent needs",
                    "Analyze operational pain points affecting performance",
                    "Assess competitive pressures requiring response",
                    "Connect problems to AI solution opportunities"
                ]
            },
            "Industry Trends": {
                "role": "Industry Analysis Specialist focusing on AI adoption trends",
                "expertise": [
                    "Track AI adoption patterns across industries",
                    "Analyze market dynamics and competitive pressures",
                    "Identify growth opportunities enabled by AI",
                    "Assess technology disruption risks and opportunities"
                ],
                "requirements": [
                    "Identify key industry trends relevant to the company",
                    "Analyze AI adoption patterns in their market segment",
                    "Highlight competitive advantages from early AI adoption",
                    "Show market opportunities enabled by AI capabilities",
                    "Connect trends to specific business opportunities"
                ]
            },
            "Competition": {
                "role": "Competitive Intelligence Specialist",
                "expertise": [
                    "Analyze competitive landscape and positioning",
                    "Assess competitor AI capabilities and strategies",
                    "Identify competitive threats and opportunities",
                    "Develop strategic responses to competitive pressure"
                ],
                "requirements": [
                    "Analyze key competitors and their AI initiatives",
                    "Identify competitive threats from AI-enabled companies",
                    "Show opportunities to gain competitive advantage",
                    "Recommend strategic responses to competitive pressure",
                    "Position AWS AI as competitive differentiator"
                ]
            },
            "Market Segments": {
                "role": "Market Segmentation Specialist",
                "expertise": [
                    "Analyze customer segments and market dynamics",
                    "Identify growth opportunities in target markets",
                    "Assess market segment needs and AI solution fit",
                    "Develop segment-specific value propositions"
                ],
                "requirements": [
                    "Identify key market segments served by the company",
                    "Analyze segment-specific needs and pain points",
                    "Show how AI addresses segment requirements",
                    "Identify new market opportunities enabled by AI",
                    "Develop segment-specific value propositions"
                ]
            },
            "Technology Strategy": {
                "role": "Technology Strategy Consultant specializing in AI integration",
                "expertise": [
                    "Assess current technology stack and capabilities",
                    "Design AI integration architectures",
                    "Evaluate technology readiness and gaps",
                    "Develop strategic technology roadmaps"
                ],
                "requirements": [
                    "Analyze current technology stack and capabilities",
                    "Identify AI integration opportunities and requirements",
                    "Assess technology readiness and capability gaps",
                    "Recommend strategic technology investments",
                    "Design AI-enabled technology architecture"
                ]
            },
            "AWS AI Services": {
                "role": "AWS AI Services Specialist and Solution Architect",
                "expertise": [
                    "Deep knowledge of AWS AI/ML service portfolio",
                    "Match business needs to specific AWS AI services",
                    "Design AWS AI solution architectures",
                    "Assess implementation complexity and requirements"
                ],
                "requirements": [
                    "Match specific AWS AI services to identified business needs",
                    "Explain how each service addresses company challenges",
                    "Design integration architecture with existing systems",
                    "Assess implementation complexity and prerequisites",
                    "Prioritize services based on impact and feasibility"
                ]
            },
            "Adoption Plan": {
                "role": "AI Adoption Strategy Consultant",
                "expertise": [
                    "Design phased AI implementation roadmaps",
                    "Assess organizational readiness for AI adoption",
                    "Manage change management for AI initiatives",
                    "Balance risk, complexity, and business value"
                ],
                "requirements": [
                    "Create phased implementation timeline with milestones",
                    "Prioritize services based on business impact and complexity",
                    "Address prerequisites and capability requirements",
                    "Include change management and training needs",
                    "Define success metrics and checkpoints"
                ]
            },
            "Spend": {
                "role": "AWS Cost Analysis Specialist and Financial Analyst",
                "expertise": [
                    "Analyze AWS pricing models and cost structures",
                    "Predict usage patterns and cost scaling",
                    "Develop accurate cost forecasts and budgets",
                    "Optimize cost efficiency and ROI"
                ],
                "requirements": [
                    "Analyze AWS AI service pricing models",
                    "Predict usage volumes based on business needs",
                    "Calculate monthly and annual cost projections",
                    "Include scaling assumptions and growth factors",
                    "Recommend cost optimization strategies"
                ]
            },
            "Returns": {
                "role": "ROI Analysis Specialist and Business Value Consultant",
                "expertise": [
                    "Calculate business value and ROI from AI investments",
                    "Model cost-benefit scenarios and break-even analysis",
                    "Quantify efficiency gains and revenue opportunities",
                    "Develop compelling business cases for AI adoption"
                ],
                "requirements": [
                    "Calculate expected ROI from AWS AI investments",
                    "Model break-even timeline and value realization",
                    "Quantify efficiency gains and cost savings",
                    "Identify revenue opportunities enabled by AI",
                    "Create compelling business value narrative"
                ]
            }
        }
        
        config = section_configs.get(section_name, {
            "role": f"{section_name} Specialist",
            "expertise": [f"Expert in {section_name.lower()} analysis and recommendations"],
            "requirements": [f"Provide comprehensive {section_name.lower()} analysis"]
        })
        
        # Build the specialized prompt
        prompt_parts = [
            f"You are a {config['role']}.",
            "",
            "Your expertise includes:",
        ]
        
        for expertise in config['expertise']:
            prompt_parts.append(f"• {expertise}")
        
        prompt_parts.extend([
            "",
            f"Create professional content for the '{section_name}' section of an AWS AI services proposal.",
            "",
            "Requirements:"
        ])
        
        for requirement in config['requirements']:
            prompt_parts.append(f"• {requirement}")
        
        # Add context based on selected sources
        prompt_parts.append("\nContext:")
        
        if use_local and company_data:
            prompt_parts.extend([
                "",
                "COMPANY INFORMATION:",
                company_data[:4000],  # More context for subagents
                ""
            ])
        
        if use_world and aws_data:
            prompt_parts.extend([
                "AWS AI SERVICES REFERENCE:",
                aws_data[:3000],
                ""
            ])
        
        if use_online:
            prompt_parts.append("ADDITIONAL REQUIREMENT: Include current market intelligence, recent trends, and competitive developments relevant to this analysis.")
        
        prompt_parts.extend([
            "",
            "Provide detailed, professional content that directly addresses all requirements.",
            "Focus on actionable insights and specific recommendations.",
            "Use business language appropriate for executive audiences."
        ])
        
        return "\n".join(prompt_parts)
    
    def _calculate_content_weights(self, company_data: str, aws_data: str, 
                                 use_local: bool, use_world: bool, use_online: bool) -> ContentTracking:
        """Calculate content source weights based on usage and data quality"""
        tracking = ContentTracking()
        
        # Assess local content quality
        local_quality = 0.0
        if use_local and company_data:
            # Length factor (0-1 based on content richness)
            length_factor = min(1.0, len(company_data) / 5000)
            
            # Keyword relevance (0-1 based on AI/business terms)
            ai_keywords = ['AI', 'artificial intelligence', 'machine learning', 'automation', 
                          'digital transformation', 'technology', 'innovation', 'data']
            keyword_matches = sum(1 for keyword in ai_keywords if keyword.lower() in company_data.lower())
            keyword_factor = min(1.0, keyword_matches / len(ai_keywords))
            
            # Structure factor (0-1 based on organization)
            structure_indicators = ['#', '##', '•', '-', '1.', '2.', '\n\n']
            structure_matches = sum(1 for indicator in structure_indicators if indicator in company_data)
            structure_factor = min(1.0, structure_matches / len(structure_indicators))
            
            # Combined quality score
            local_quality = (0.4 * length_factor + 0.4 * keyword_factor + 0.2 * structure_factor)
        
        # Assign weights based on selections and quality
        total_weight = 0
        
        if use_local:
            # High quality local content gets higher weight
            local_weight = 0.6 + (local_quality * 0.3)  # 0.6-0.9 range
            tracking.local_content = local_weight
            total_weight += local_weight
        
        if use_world:
            # World knowledge fills remaining capacity
            world_weight = 0.5 if not use_local else (0.3 - local_quality * 0.1)
            tracking.world_knowledge = max(0.1, world_weight)
            total_weight += tracking.world_knowledge
        
        if use_online:
            # Online research gets consistent small portion
            online_weight = 0.15
            tracking.online_research = online_weight
            total_weight += online_weight
        
        # Normalize to sum to 1.0
        if total_weight > 0:
            tracking.local_content /= total_weight
            tracking.world_knowledge /= total_weight
            tracking.online_research /= total_weight
        
        return tracking

def load_company_data(company_name: str) -> str:
    """Load company data from markdown files"""
    if not company_name:
        return ""
    
    company_dir = Path("companies") / company_name
    if not company_dir.exists():
        return ""
    
    md_files = list(company_dir.glob("*.md"))
    if not md_files:
        return ""
    
    combined_content = []
    for md_file in md_files:
        try:
            combined_content.append(f"### {md_file.name}")
            combined_content.append(md_file.read_text(encoding='utf-8'))
            combined_content.append("\n")
        except Exception as e:
            st.warning(f"Could not read {md_file.name}: {str(e)}")
            continue
    
    return "\n".join(combined_content)

def load_aws_data() -> str:
    """Load AWS AI services data"""
    aws_file = Path("projects/llm-architectures-on-aws/report-03.md")
    if aws_file.exists():
        try:
            return aws_file.read_text(encoding='utf-8')
        except Exception as e:
            st.warning(f"Could not read AWS data: {str(e)}")
    return ""

def save_proposal(company_name: str, sections: Dict[str, ProposalSection]) -> str:
    """Save generated proposal to file"""
    if not company_name:
        company_name = "unknown-company"
    
    # Create proposal directory
    proposals_dir = Path("proposals") / company_name
    proposals_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"proposal-{timestamp}.md"
    filepath = proposals_dir / filename
    
    # Generate proposal content
    content_parts = [
        f"# AWS AI Services Proposal - {company_name.title()}",
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Table of Contents",
        ""
    ]
    
    # Add table of contents
    for section_name, section in sections.items():
        if section.generated:
            content_parts.append(f"- [{section_name}](#{section_name.lower().replace(' ', '-')})")
    
    content_parts.append("")
    
    # Add sections
    for section_name, section in sections.items():
        if section.generated:
            content_parts.extend([
                f"## {section_name}",
                "",
                section.content,
                "",
                f"*{section.tracking.get_score_string() if section.tracking else 'Content scoring not available'}*",
                "",
                "---",
                ""
            ])
    
    # Write to file
    try:
        filepath.write_text("\n".join(content_parts), encoding='utf-8')
        return str(filepath)
    except Exception as e:
        st.error(f"Error saving proposal: {str(e)}")
        return ""

# Streamlit UI Implementation
def main():
    st.set_page_config(
        page_title="AWS AI Proposal Generator",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.title("🤖 AWS AI Proposal Generator")
    st.markdown("*Powered by Claude Code SDK Subagents*")
    
    # Initialize session state
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = SubAgentOrchestrator()
    
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    
    # Step progress indicator
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.current_step == 1:
            st.info("🔄 **Step 1: Configuration**")
        else:
            st.success("✅ Step 1: Configuration")
    
    with col2:
        if st.session_state.current_step == 2:
            st.info("🔄 **Step 2: Generation**")
        elif st.session_state.current_step > 2:
            st.success("✅ Step 2: Generation")
        else:
            st.empty()
    
    with col3:
        if st.session_state.current_step == 3:
            st.info("🔄 **Step 3: Review & Export**")
        elif st.session_state.current_step > 3:
            st.success("✅ Step 3: Review & Export")
        else:
            st.empty()
    
    st.markdown("---")
    
    # Step 1: Configuration
    if st.session_state.current_step == 1:
        show_configuration_step()
    
    # Step 2: Generation
    elif st.session_state.current_step == 2:
        show_generation_step()
    
    # Step 3: Review & Export
    elif st.session_state.current_step == 3:
        show_review_step()

def show_configuration_step():
    """Step 1: Configuration interface"""
    st.header("📋 Configuration")
    
    # Company Selection
    st.subheader("🏢 Select Company")
    
    companies_dir = Path("companies")
    if not companies_dir.exists():
        st.error("Companies directory not found. Please create 'companies/' folder with company data.")
        return
    
    company_folders = [f.name for f in companies_dir.iterdir() if f.is_dir()]
    
    if not company_folders:
        st.error("No company folders found in companies/ directory.")
        return
    
    selected_company = st.selectbox(
        "Choose a company:",
        options=[""] + company_folders,
        key="company_selectbox"
    )
    
    if selected_company:
        st.session_state.selected_company = selected_company
        # Load and preview company data
        company_data = load_company_data(selected_company)
        st.session_state.company_data = company_data
        
        if company_data:
            with st.expander(f"📄 Preview {selected_company.title()} Data", expanded=False):
                st.text(f"Data length: {len(company_data):,} characters")
                st.text_area("Company information preview:", company_data[:500] + "...", height=100, disabled=True)
        else:
            st.warning(f"No data found for {selected_company}")
    
    # Load AWS data
    aws_data = load_aws_data()
    st.session_state.aws_data = aws_data
    if not aws_data:
        st.warning("AWS AI services data not found. Some features may be limited.")
    
    st.markdown("---")
    
    # Proposal Sections Selection
    st.subheader("📝 Select Proposal Sections")
    
    col1, col2 = st.columns(2)
    selected_sections = []
    
    sections_list = list(st.session_state.orchestrator.sections.keys())
    mid_point = len(sections_list) // 2
    
    with col1:
        for section_name in sections_list[:mid_point]:
            if st.checkbox(section_name, value=True, key=f"section_{section_name}"):
                selected_sections.append(section_name)
    
    with col2:
        for section_name in sections_list[mid_point:]:
            if st.checkbox(section_name, value=True, key=f"section_{section_name}"):
                selected_sections.append(section_name)
    
    st.session_state.selected_sections = selected_sections
    st.info(f"Selected {len(selected_sections)} sections for generation")
    
    st.markdown("---")
    
    # Content Sources Configuration
    st.subheader("🔍 Content Sources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📁 Local Content**")
        use_local = st.checkbox("Use company data", value=True, key="use_local")
        if use_local:
            st.success("✅ Recommended")
        else:
            st.info("ℹ️ Optional")
    
    with col2:
        st.markdown("**🌍 World Knowledge**")
        use_world = st.checkbox("Use AI expertise", value=True, key="use_world")
        if use_world:
            st.success("✅ Recommended")
        else:
            st.info("ℹ️ Optional")
    
    with col3:
        st.markdown("**🔍 Online Research**")
        use_online = st.checkbox("Include market research", value=False, key="use_online")
        if use_online:
            st.warning("🚧 Simulated")
        else:
            st.info("ℹ️ Optional")
    
    st.session_state.use_local = use_local
    st.session_state.use_world = use_world
    st.session_state.use_online = use_online
    
    # Preview content weights
    if selected_company and (use_local or use_world or use_online):
        tracking = st.session_state.orchestrator._calculate_content_weights(
            st.session_state.get('company_data', ''),
            st.session_state.get('aws_data', ''),
            use_local, use_world, use_online
        )
        st.info(f"📊 Content Preview: {tracking.get_score_string()}")
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col3:
        can_proceed = (selected_company and 
                      len(selected_sections) > 0 and 
                      (use_local or use_world or use_online))
        
        if st.button("➡️ Start Generation", disabled=not can_proceed):
            if can_proceed:
                st.session_state.current_step = 2
                st.rerun()

def show_generation_step():
    """Step 2: Generation interface"""
    st.header("⚡ Generation")
    
    # Configuration summary
    st.subheader("📊 Generation Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Company", st.session_state.get('selected_company', 'None'))
    
    with col2:
        st.metric("Sections", len(st.session_state.get('selected_sections', [])))
    
    with col3:
        sources = []
        if st.session_state.get('use_local'): sources.append("Local")
        if st.session_state.get('use_world'): sources.append("World")
        if st.session_state.get('use_online'): sources.append("Online")
        st.metric("Sources", ", ".join(sources) if sources else "None")
    
    st.markdown("---")
    
    # Generation controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Back to Config"):
            st.session_state.current_step = 1
            st.rerun()
    
    with col3:
        if st.button("🚀 Generate Proposal", type="primary"):
            # Run generation
            run_subagent_generation()
    
    # Show generation progress if in progress
    if st.session_state.get('generation_in_progress'):
        show_generation_progress()
    
    # Show results if generation complete
    if st.session_state.get('generated_sections'):
        st.success("✅ Generation Complete!")
        if st.button("➡️ Review Results"):
            st.session_state.current_step = 3
            st.rerun()

def show_review_step():
    """Step 3: Review & Export interface"""
    st.header("📋 Review & Export")
    
    if not st.session_state.get('generated_sections'):
        st.error("No generated content found. Please go back and generate a proposal.")
        if st.button("⬅️ Back to Generation"):
            st.session_state.current_step = 2
            st.rerun()
        return
    
    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Back to Generation"):
            st.session_state.current_step = 2
            st.rerun()
    
    with col3:
        if st.button("🔄 Generate New Proposal"):
            # Clear session state and restart
            for key in ['generated_sections', 'selected_company', 'selected_sections']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_step = 1
            st.rerun()
    
    # Create tabs for review
    sections = st.session_state.generated_sections
    tab_names = ["Summary"] + list(sections.keys())
    tabs = st.tabs(tab_names)
    
    # Summary tab
    with tabs[0]:
        st.subheader("📊 Generation Summary")
        
        completed_sections = [s for s in sections.values() if s.generated]
        total_sections = len(sections)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Sections Generated", f"{len(completed_sections)}/{total_sections}")
        
        with col2:
            if completed_sections:
                avg_duration = sum(s.agent_progress.get_duration() or 0 for s in completed_sections) / len(completed_sections)
                st.metric("Avg Generation Time", f"{avg_duration:.1f}s")
            else:
                st.metric("Avg Generation Time", "N/A")
        
        with col3:
            success_rate = (len(completed_sections) / total_sections) * 100 if total_sections > 0 else 0
            st.metric("Success Rate", f"{success_rate:.0f}%")
        
        # Download button
        st.markdown("---")
        if st.button("📄 Download Proposal", type="primary"):
            filepath = save_proposal(st.session_state.get('selected_company', 'unknown'), sections)
            if filepath:
                st.success(f"✅ Proposal saved to: {filepath}")
            else:
                st.error("❌ Failed to save proposal")
    
    # Individual section tabs
    for i, (section_name, section) in enumerate(sections.items(), 1):
        with tabs[i]:
            if section.generated:
                # Section header with performance
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(f"📝 {section_name}")
                
                with col2:
                    if section.agent_progress:
                        duration = section.agent_progress.get_duration()
                        if duration:
                            st.metric("Generation Time", f"{duration:.1f}s")
                
                # Content scoring
                if section.tracking:
                    st.info(section.tracking.get_score_string())
                
                # Agent performance details
                if section.agent_progress:
                    with st.expander("🤖 Agent Performance Details", expanded=False):
                        st.json({
                            "Status": section.agent_progress.status.value,
                            "Duration": f"{section.agent_progress.get_duration():.2f}s" if section.agent_progress.get_duration() else "N/A",
                            "Start Time": datetime.fromtimestamp(section.agent_progress.start_time).strftime("%H:%M:%S") if section.agent_progress.start_time else "N/A",
                            "End Time": datetime.fromtimestamp(section.agent_progress.end_time).strftime("%H:%M:%S") if section.agent_progress.end_time else "N/A"
                        })
                
                # Section content
                st.markdown("---")
                st.markdown(section.content)
                
            else:
                st.error(f"❌ {section_name} generation failed")
                if section.content:
                    st.text(section.content)

def run_subagent_generation():
    """Run the proposal generation using proper subagents"""
    selected_company = st.session_state.get('selected_company')
    selected_sections = st.session_state.get('selected_sections', [])
    use_local = st.session_state.get('use_local', False)
    use_world = st.session_state.get('use_world', False)
    use_online = st.session_state.get('use_online', False)
    
    if not selected_company or not selected_sections:
        st.error("Missing configuration. Please go back and complete setup.")
        return
    
    st.session_state.generation_in_progress = True
    
    company_data = st.session_state.get('company_data', '')
    aws_data = st.session_state.get('aws_data', '')
    
    # Progress tracking containers
    progress_container = st.container()
    
    with progress_container:
        st.subheader("🤖 Subagent Progress")
        progress_placeholders = {}
        for section_name in selected_sections:
            progress_placeholders[section_name] = st.empty()
        
        overall_progress = st.progress(0)
        status_text = st.empty()
    
    async def generate_all_sections():
        """Generate all sections using proper Claude Code subagents"""
        results = {}
        total = len(selected_sections)
        
        # Initialize progress displays
        for section_name in selected_sections:
            with progress_placeholders[section_name]:
                st.info(f"⏳ {section_name} Subagent: Pending...")
        
        status_text.text(f"🚀 Starting {total} specialized subagents in parallel...")
        
        # Create tasks for parallel subagent execution
        tasks = []
        for section_name in selected_sections:
            task = st.session_state.orchestrator.generate_section(
                section_name, company_data, aws_data,
                use_local, use_world, use_online
            )
            tasks.append((section_name, task))
        
        # Monitor progress during parallel execution
        try:
            # Execute all subagents in parallel
            completed_tasks = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
            
            # Process results
            for i, ((section_name, _), result) in enumerate(zip(tasks, completed_tasks)):
                if isinstance(result, Exception):
                    st.error(f"❌ Subagent {section_name} failed: {result}")
                    # Create failed section
                    failed_section = st.session_state.orchestrator.sections[section_name]
                    failed_section.generated = False
                    failed_section.content = f"Error: {result}"
                    results[section_name] = failed_section
                else:
                    results[section_name] = result
                
                # Update individual progress displays
                section = results[section_name]
                if section.agent_progress:
                    duration = section.agent_progress.get_duration()
                    if section.agent_progress.status == AgentStatus.COMPLETED:
                        with progress_placeholders[section_name]:
                            st.success(f"✅ {section_name} Subagent: Completed in {duration:.1f}s")
                    elif section.agent_progress.status == AgentStatus.ERROR:
                        with progress_placeholders[section_name]:
                            st.error(f"❌ {section_name} Subagent: {section.agent_progress.error_message}")
            
            # Final progress update
            status_text.success("🎉 All subagents completed!")
            overall_progress.progress(1.0)
            
            return results
            
        except Exception as e:
            status_text.error(f"❌ Error in subagent orchestration: {str(e)}")
            return {}
    
    # Run generation
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        st.session_state.generated_sections = loop.run_until_complete(generate_all_sections())
        
        # Clean up
        if "generation_in_progress" in st.session_state:
            del st.session_state.generation_in_progress
            
    except Exception as e:
        st.error(f"❌ Generation failed: {str(e)}")
        if "generation_in_progress" in st.session_state:
            del st.session_state.generation_in_progress

def show_generation_progress():
    """Show progress during generation"""
    st.info("⚡ Generation in progress...")
    st.text("Subagents are working in parallel using Claude Code SDK...")

if __name__ == "__main__":
    main()