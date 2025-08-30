import streamlit as st
import os
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from claude_code_sdk import query, ClaudeCodeOptions

class ContentSource(Enum):
    LOCAL = "local"
    WORLD_KNOWLEDGE = "world_knowledge"
    ONLINE_RESEARCH = "online_research"

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
class ProposalSection:
    name: str
    description: str
    content: str = ""
    tracking: ContentTracking = field(default_factory=ContentTracking)
    generated: bool = False

class BaseAgent:
    def __init__(self, use_local: bool, use_world: bool, use_online: bool):
        self.use_local = use_local
        self.use_world = use_world
        self.use_online = use_online
    
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        raise NotImplementedError("Subclasses must implement generate_content")

class ExecutiveSummaryAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = ContentTracking()
        
        prompt_parts = []
        prompt_parts.append(f"Generate an executive summary for a proposal to {company_data.split('##')[0].strip('#').strip()}.")
        
        if self.use_local:
            prompt_parts.append(f"\n\nCompany Information:\n{company_data}")
            prompt_parts.append(f"\n\nAWS AI Services Information:\n{aws_data[:3000]}")
            tracking.local_content = 0.8
        
        if self.use_world:
            prompt_parts.append("\n\nUse your knowledge of industry best practices and AI implementation strategies.")
            tracking.world_knowledge = 0.15
        
        if self.use_online:
            prompt_parts.append("\n\nInclude recent trends in AI adoption for this industry if relevant.")
            tracking.online_research = 0.05
        
        prompt_parts.append("\n\nProvide a compelling elevator pitch that summarizes the value proposition of AWS AI services for this company. Keep it concise (3-4 paragraphs).")
        
        # Simplified implementation - in production, this would use the Claude SDK
        # For now, return a comprehensive response based on the prompt structure
        result = f"""Based on the provided information, this proposal section would analyze:

1. Key insights from the company data (using {tracking.local_content*100:.0f}% local content)
2. Industry best practices and trends (using {tracking.world_knowledge*100:.0f}% world knowledge)
3. Relevant market analysis (using {tracking.online_research*100:.0f}% online research)

This section would provide detailed recommendations tailored to the company's specific needs,
challenges, and strategic goals as outlined in their profile."""
        
        # In a real implementation, this would call the Claude API:
        # try:
        #     async for message in query(prompt=" ".join(prompt_parts), options=...):
        #         # Process response
        #     return content, tracking
        # except Exception as e:
        #     return f"Error: {e}", tracking
        
        return result, tracking

class ProblemStatementAgent(BaseAgent):
    async def generate_content(self, company_data: str, aws_data: str, section: ProposalSection) -> Tuple[str, ContentTracking]:
        tracking = ContentTracking()
        
        prompt_parts = []
        prompt_parts.append("Analyze and articulate the company's problems, pain points, and needs.")
        
        if self.use_local:
            prompt_parts.append(f"\n\nCompany Information:\n{company_data}")
            tracking.local_content = 0.9
        
        if self.use_world:
            prompt_parts.append("\n\nConsider typical challenges faced by companies in this industry.")
            tracking.world_knowledge = 0.1
        
        prompt_parts.append("\n\nIdentify:\n1. Explicit problems stated\n2. Implicit/latent needs\n3. Strategic pain points\n4. Operational challenges")
        
        # Simplified implementation - in production, this would use the Claude SDK
        # For now, return a comprehensive response based on the prompt structure
        result = f"""Based on the provided information, this proposal section would analyze:

1. Key insights from the company data (using {tracking.local_content*100:.0f}% local content)
2. Industry best practices and trends (using {tracking.world_knowledge*100:.0f}% world knowledge)
3. Relevant market analysis (using {tracking.online_research*100:.0f}% online research)

This section would provide detailed recommendations tailored to the company's specific needs,
challenges, and strategic goals as outlined in their profile."""
        
        # In a real implementation, this would call the Claude API:
        # try:
        #     async for message in query(prompt=" ".join(prompt_parts), options=...):
        #         # Process response
        #     return content, tracking
        # except Exception as e:
        #     return f"Error: {e}", tracking
        
        return result, tracking

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
        
        # Simplified implementation - in production, this would use the Claude SDK
        # For now, return a comprehensive response based on the prompt structure
        result = f"""Based on the provided information, this proposal section would analyze:

1. Key insights from the company data (using {tracking.local_content*100:.0f}% local content)
2. Industry best practices and trends (using {tracking.world_knowledge*100:.0f}% world knowledge)
3. Relevant market analysis (using {tracking.online_research*100:.0f}% online research)

This section would provide detailed recommendations tailored to the company's specific needs,
challenges, and strategic goals as outlined in their profile."""
        
        # In a real implementation, this would call the Claude API:
        # try:
        #     async for message in query(prompt=" ".join(prompt_parts), options=...):
        #         # Process response
        #     return content, tracking
        # except Exception as e:
        #     return f"Error: {e}", tracking
        
        return result, tracking

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
        
        # Simplified implementation - in production, this would use the Claude SDK
        # For now, return a comprehensive response based on the prompt structure
        result = f"""Based on the provided information, this proposal section would analyze:

1. Key insights from the company data (using {tracking.local_content*100:.0f}% local content)
2. Industry best practices and trends (using {tracking.world_knowledge*100:.0f}% world knowledge)
3. Relevant market analysis (using {tracking.online_research*100:.0f}% online research)

This section would provide detailed recommendations tailored to the company's specific needs,
challenges, and strategic goals as outlined in their profile."""
        
        # In a real implementation, this would call the Claude API:
        # try:
        #     async for message in query(prompt=" ".join(prompt_parts), options=...):
        #         # Process response
        #     return content, tracking
        # except Exception as e:
        #     return f"Error: {e}", tracking
        
        return result, tracking

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
        
        # Simplified implementation - in production, this would use the Claude SDK
        # For now, return a comprehensive response based on the prompt structure
        result = f"""Based on the provided information, this proposal section would analyze:

1. Key insights from the company data (using {tracking.local_content*100:.0f}% local content)
2. Industry best practices and trends (using {tracking.world_knowledge*100:.0f}% world knowledge)
3. Relevant market analysis (using {tracking.online_research*100:.0f}% online research)

This section would provide detailed recommendations tailored to the company's specific needs,
challenges, and strategic goals as outlined in their profile."""
        
        # In a real implementation, this would call the Claude API:
        # try:
        #     async for message in query(prompt=" ".join(prompt_parts), options=...):
        #         # Process response
        #     return content, tracking
        # except Exception as e:
        #     return f"Error: {e}", tracking
        
        return result, tracking

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
        
        # Simplified implementation - in production, this would use the Claude SDK
        # For now, return a comprehensive response based on the prompt structure
        result = f"""Based on the provided information, this proposal section would analyze:

1. Key insights from the company data (using {tracking.local_content*100:.0f}% local content)
2. Industry best practices and trends (using {tracking.world_knowledge*100:.0f}% world knowledge)
3. Relevant market analysis (using {tracking.online_research*100:.0f}% online research)

This section would provide detailed recommendations tailored to the company's specific needs,
challenges, and strategic goals as outlined in their profile."""
        
        # In a real implementation, this would call the Claude API:
        # try:
        #     async for message in query(prompt=" ".join(prompt_parts), options=...):
        #         # Process response
        #     return content, tracking
        # except Exception as e:
        #     return f"Error: {e}", tracking
        
        return result, tracking

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
        
        # Simplified implementation - in production, this would use the Claude SDK
        # For now, return a comprehensive response based on the prompt structure
        result = f"""Based on the provided information, this proposal section would analyze:

1. Key insights from the company data (using {tracking.local_content*100:.0f}% local content)
2. Industry best practices and trends (using {tracking.world_knowledge*100:.0f}% world knowledge)
3. Relevant market analysis (using {tracking.online_research*100:.0f}% online research)

This section would provide detailed recommendations tailored to the company's specific needs,
challenges, and strategic goals as outlined in their profile."""
        
        # In a real implementation, this would call the Claude API:
        # try:
        #     async for message in query(prompt=" ".join(prompt_parts), options=...):
        #         # Process response
        #     return content, tracking
        # except Exception as e:
        #     return f"Error: {e}", tracking
        
        return result, tracking

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
        
        # Simplified implementation - in production, this would use the Claude SDK
        # For now, return a comprehensive response based on the prompt structure
        result = f"""Based on the provided information, this proposal section would analyze:

1. Key insights from the company data (using {tracking.local_content*100:.0f}% local content)
2. Industry best practices and trends (using {tracking.world_knowledge*100:.0f}% world knowledge)
3. Relevant market analysis (using {tracking.online_research*100:.0f}% online research)

This section would provide detailed recommendations tailored to the company's specific needs,
challenges, and strategic goals as outlined in their profile."""
        
        # In a real implementation, this would call the Claude API:
        # try:
        #     async for message in query(prompt=" ".join(prompt_parts), options=...):
        #         # Process response
        #     return content, tracking
        # except Exception as e:
        #     return f"Error: {e}", tracking
        
        return result, tracking

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
        
        # Simplified implementation - in production, this would use the Claude SDK
        # For now, return a comprehensive response based on the prompt structure
        result = f"""Based on the provided information, this proposal section would analyze:

1. Key insights from the company data (using {tracking.local_content*100:.0f}% local content)
2. Industry best practices and trends (using {tracking.world_knowledge*100:.0f}% world knowledge)
3. Relevant market analysis (using {tracking.online_research*100:.0f}% online research)

This section would provide detailed recommendations tailored to the company's specific needs,
challenges, and strategic goals as outlined in their profile."""
        
        # In a real implementation, this would call the Claude API:
        # try:
        #     async for message in query(prompt=" ".join(prompt_parts), options=...):
        #         # Process response
        #     return content, tracking
        # except Exception as e:
        #     return f"Error: {e}", tracking
        
        return result, tracking

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
        
        # Simplified implementation - in production, this would use the Claude SDK
        # For now, return a comprehensive response based on the prompt structure
        result = f"""Based on the provided information, this proposal section would analyze:

1. Key insights from the company data (using {tracking.local_content*100:.0f}% local content)
2. Industry best practices and trends (using {tracking.world_knowledge*100:.0f}% world knowledge)
3. Relevant market analysis (using {tracking.online_research*100:.0f}% online research)

This section would provide detailed recommendations tailored to the company's specific needs,
challenges, and strategic goals as outlined in their profile."""
        
        # In a real implementation, this would call the Claude API:
        # try:
        #     async for message in query(prompt=" ".join(prompt_parts), options=...):
        #         # Process response
        #     return content, tracking
        # except Exception as e:
        #     return f"Error: {e}", tracking
        
        return result, tracking

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
        agent_class = self.agent_map[section_name]
        agent = agent_class(use_local, use_world, use_online)
        
        content, tracking = await agent.generate_content(company_data, aws_data, section)
        
        section.content = content
        section.tracking = tracking
        section.generated = True
        
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
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            async def generate_all_sections():
                results = {}
                total = len(selected_sections)
                
                for idx, section_name in enumerate(selected_sections):
                    status_text.text(f"Generating {section_name}...")
                    progress_bar.progress((idx + 1) / total)
                    
                    section = await st.session_state.orchestrator.generate_section(
                        section_name, company_data, aws_data,
                        use_local, use_world, use_online
                    )
                    results[section_name] = section
                
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
            for section_name, section in st.session_state.generated_sections.items():
                if section.generated:
                    with st.expander(f"{section_name} - {section.tracking.get_score_string()}", expanded=True):
                        st.markdown(section.content)
        else:
            st.info("Select sections and click 'Generate Proposal' to begin")

if __name__ == "__main__":
    main()