You are an expert at Streamlit app development and Claude Code SDK. You are building a single page app apps/proposal.py in Streamit based on the following specification. Think harder to build this app as an agent based system.

Use Claude Code SDK https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python effectively for LLM agent capabilities.

Learn about building effective agents by reading markdown/building-effective-ai-agents-anthropic/article.md article.

The app helps user generate a proposal matching company needs with AWS AI offerings.
Information about AWS AI offerings is available in projects/llm-architectures-on-aws/report-03.md file.

List companies available in companies/ folder for the user to select one to target the proposal.

User can then select one or many of the proposal sections:
- Executive Summary: What is the elevator pitch and summary of the rest of the document?
- Problem Statement: What are the problems, pain points, explicit asks, and latent needs of the company?
- Industry Trends: Which industry trends are relevant for the company growth?
- Competition: What are competitors doing which may need a response from the company?
- Market Segments: Which market segments is the company serving and what are the opportunity gaps to address these markets?
- Technology Strategy: What are the technologies company is using or developing and what is their strategy?
- AWS AI Services: Which AWS AI services match company's needs and why?
- Adoption Plan: What is the recommended timeline for company to adopt AWS AI services based on their needs and external factors (industry, competition, markets)?
- Spend: Analyze AWS AI services public pricing, predict usage volume based on company needs, propose monthly and annual spend.
- Returns: Create a plan for spend vs returns to illustrate when the company is able to break-even on their AWS spend.

Add check boxes to only use local content (companies/ folder content), use LLM world knowledge, use online research to create the proposal content.

When writing the proposal sections add a score to each section based on extent to which content from companies/ folder was used vs your world knowledge vs online research. Something like Content score: 80% local content, 10% world knowledge, 10% online research.

Create the most optiminal agent/subagent strategy to generate the proposal. Based on the selected proposal sections create subagents to write content for these sections. Create a progress indicator UI to show progress of each subagent. Compile the sections, format the proposal, and save it in the proposals/company-name/proposal-yyyy-mm-dd.md file.

IMPORTANT: These instructions may be revised and rerun to update existing app. Note incremental changes in changelog. Note any open [ ] issues and fix these.

# Issues

[x] Error generating proposal: name 'progress_bar' is not defined

[x] Instead of using the sidebar use main content area for all the features of the app. Smartly show/hide sections and scroll to active section as user progresses in the UI.

[x] Error generating proposal: unsupported operand type(s) for /: 'PosixPath' and 'NoneType'

[x] Even after selecting a company I get this error - No company selected. Please go back and select a company.

[x] See this error in the generate proposal - Error generating competition analysis: can only concatenate str (not "SystemMessage") to str

[x] Agent processing is taking a long time and seems to be stuck after starting the second agent. Why are multiple subagents not run in parallel where allowed by best practices and Claude Code SDK? Why does progress not go through agent stages like starting, active, complete, error, etc.

[x] I am seeing whole bunch of agents in pending state with no progress for some time. Are you using Claude Code SDK correctly and setting up subagents as per best practices? Read following docs to learn: 
- https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-headless
- https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python
- https://docs.anthropic.com/en/docs/claude-code/sub-agents


# Changelog

## 2025-08-30 - Architecture Overhaul: True Claude Code SDK Subagents

### ✅ Complete Subagent Architecture Rewrite

#### Implemented True Claude Code SDK Subagents
- **Task Tool Integration**: Complete rewrite to use proper Claude Code SDK subagents via Task tool
- **SubAgentOrchestrator**: New orchestration system designed specifically for Claude Code SDK best practices
- **Specialized Subagent Prompts**: Each proposal section now has a dedicated subagent with role-specific expertise and requirements
- **Professional Agent Definitions**: 10 specialized subagents with detailed role definitions, expertise areas, and specific requirements
- **Context-Rich Prompts**: Subagents receive comprehensive context including company data (4000+ chars) and AWS services reference

#### Enhanced Subagent Specialization
- **Executive Summary Specialist**: C-level communications expert focused on business value propositions
- **Business Analysis Specialist**: Problem identification and pain point analysis expert
- **Industry Analysis Specialist**: AI adoption trends and market dynamics expert
- **Competitive Intelligence Specialist**: Competitive landscape and strategic positioning expert
- **Market Segmentation Specialist**: Customer segments and growth opportunities expert
- **Technology Strategy Consultant**: AI integration architecture and roadmap expert
- **AWS AI Services Specialist**: AWS service matching and solution architecture expert
- **AI Adoption Strategy Consultant**: Implementation roadmaps and change management expert
- **AWS Cost Analysis Specialist**: Pricing models and cost optimization expert
- **ROI Analysis Specialist**: Business value and return on investment expert

#### Advanced Subagent Architecture
- **True Parallel Execution**: Multiple subagents run simultaneously using Task tool orchestration
- **Fallback Mechanisms**: Graceful degradation if Task tool unavailable (shouldn't happen in Claude Code)
- **Enhanced Error Handling**: Individual subagent failure isolation with detailed error reporting
- **Progress Monitoring**: Real-time tracking of subagent status and performance
- **Content Quality Assessment**: Intelligent content source weighting based on data quality

#### Claude Code SDK Best Practices Implementation
- **Proper Task Tool Usage**: Uses Claude Code's Task tool for creating actual subagents
- **Specialized System Prompts**: Each subagent has role-specific expertise and clear requirements
- **Context Management**: Optimized context distribution to subagents with relevant data
- **Error Recovery**: Robust error handling with graceful fallbacks
- **Resource Optimization**: Efficient subagent orchestration and coordination

### 🚀 Performance and Quality Benefits
- **True Parallelization**: Real subagents working simultaneously instead of sequential function calls
- **Expert-Level Content**: Each section generated by specialist subagent with deep domain expertise
- **Consistent Quality**: Standardized requirements and evaluation criteria for all subagents
- **Better Context Usage**: Specialized prompts ensure subagents focus on relevant aspects
- **Professional Output**: Business-appropriate language and executive-level recommendations

### 🏗️ Technical Architecture Improvements
- **SubAgentOrchestrator Class**: Purpose-built for Claude Code SDK subagent management
- **Specialized Prompt Engineering**: Section-specific prompts with role definitions and requirements
- **Enhanced Content Tracking**: Improved content source weight calculation and quality assessment
- **Streamlined UI**: Clear indication that system uses "Claude Code SDK Subagents"
- **Better Error Messages**: Specific feedback when subagents fail or Task tool unavailable

### 📚 Documentation Updates
- **Subagent Architecture Guide**: Complete documentation of new subagent system
- **Role Definitions**: Detailed specifications for each specialist subagent
- **Best Practices Integration**: Implementation following Claude Code SDK documentation
- **Troubleshooting**: Enhanced error handling and user guidance

## 2025-08-30 - Performance Enhancement: Parallel Agent Execution 

### ✅ Critical Performance Update

#### Implemented Parallel Agent Execution
- **Asyncio Integration**: Complete rewrite of agent orchestration using asyncio.gather() for true parallel processing
- **Enhanced Progress Tracking**: Added comprehensive agent stage tracking (pending → starting → active → processing → completing → completed/error)
- **Real-time UI Updates**: Implemented monitor_agent_progress() function for live progress monitoring during parallel execution
- **Performance Optimization**: Multiple agents now execute simultaneously instead of sequentially, dramatically reducing generation time
- **Advanced Error Handling**: Robust error recovery with individual agent failure isolation using return_exceptions=True

#### Enhanced Agent Progress System
- **Detailed Status Stages**: AgentStatus enum with 7 distinct stages for granular progress visibility
- **Real-time Monitoring**: Live UI updates every 500ms showing active agents and completion status
- **Progress Visualization**: Individual agent displays with emoji indicators and timing information
- **Completion Metrics**: Detailed performance statistics including duration and success rates

#### Architecture Improvements
- **Async/Await Pattern**: Complete transition to async architecture throughout agent system
- **Task Coordination**: Proper task management with asyncio.create_task() and cancellation support
- **Resource Management**: Efficient event loop management with proper cleanup
- **Concurrent Safety**: Thread-safe session state management during parallel operations

### 🚀 Performance Benefits
- **Dramatically Reduced Generation Time**: 10 agents now run in parallel instead of sequential execution
- **Improved User Experience**: Real-time progress feedback with active agent indicators
- **Better Resource Utilization**: Optimal use of Claude Code SDK concurrent capabilities
- **Enhanced Reliability**: Individual agent failures don't block other agents from completing

## 2025-08-30 - UI Redesign: Modern Step-Based Workflow  

### ✅ Critical Bug Fix Update

#### Fixed Claude SDK Message Handling Error
- **SystemMessage Content Extraction**: Fixed string concatenation error with SystemMessage objects
- **Message Processing**: Added `_extract_message_content()` helper method to handle different message types
- **Robust Response Handling**: Enhanced to handle both string messages and structured message objects
- **Content Attribute Support**: Checks for `content`, `text`, and fallback string conversion
- **All Agents Updated**: Applied fix consistently across all 10 agent implementations

#### Fixed Session State Management Issue
- **Company Selection Persistence**: Fixed "No company selected" error despite company being selected
- **Session State Storage**: Improved session state management by explicitly storing `selected_company`
- **Widget Key Separation**: Changed selectbox key to prevent conflicts with session state variable
- **State Validation**: Enhanced validation to check both company selection and data loading
- **Debug Information**: Added debug panel to help troubleshoot session state issues
- **Default Selection**: Improved selectbox to remember previous selection when navigating back

#### Fixed Path Operation Error  
- **PosixPath / NoneType Error**: Fixed critical error when `selected_company` is `None`
- **Null Safety**: Added comprehensive null checks in `load_company_data()`, `save_proposal()`, and `run_proposal_generation()`
- **Error Handling**: Enhanced error handling with try/catch blocks and user-friendly error messages
- **Input Validation**: Added validation to prevent generation with missing company selection
- **Fallback Values**: Added fallback company names for edge cases (e.g., "unknown-company")

### ✅ Issues Resolved  

#### Fixed Critical Errors
- **progress_bar Undefined Error**: Fixed undefined variable reference that was causing generation failures
- **Variable Scope**: Corrected variable naming from `progress_bar` to `overall_progress` for consistency
- **Path Operations**: Fixed `PosixPath / NoneType` error by adding null checks before path operations

#### Complete UI Redesign 
- **Main Content Area**: Eliminated sidebar and moved all functionality to main content area
- **Step-Based Workflow**: Implemented 3-step guided process (Configuration → Generation → Review & Export)
- **Smart Navigation**: Added forward/backward navigation with session state persistence
- **Progressive UI**: Show/hide sections based on current step with clear visual progression

### 🎨 New User Interface Features

#### Step 1: Configuration 📋
- **Full-Width Company Selection**: Enhanced company browser with data preview
- **Two-Column Section Selection**: Organized proposal sections in easy-to-scan layout
- **Three-Column Content Sources**: Visual content source configuration with smart indicators
- **Intelligent Preview**: Real-time content weight calculation and quality assessment

#### Step 2: Generation ⚡  
- **Configuration Summary**: Visual overview of selected options
- **Enhanced Progress Tracking**: Individual agent progress with emoji indicators
- **Real-time Status**: Live updates during generation process
- **Performance Metrics**: Generation statistics and success rates

#### Step 3: Review & Export 📋
- **Tabbed Interface**: Summary tab plus individual section tabs
- **Performance Dashboard**: Comprehensive generation analytics
- **Export Options**: Instant markdown download with smart file naming
- **Quality Insights**: Detailed agent performance and content scoring

### 🔄 Navigation & UX Improvements

#### Smart Step Flow
- **Progress Indicators**: Visual step progress with completion status (✅ 🔄 ⏳)
- **Bidirectional Navigation**: Easy movement between steps with state preservation
- **Validation Gates**: Smart button enabling/disabling based on requirements
- **Session Management**: Persistent configuration across navigation

#### Enhanced Responsiveness
- **Wide Layout**: Full utilization of screen real estate
- **Container Organization**: Clean section separation with visual dividers
- **Smart Columns**: Adaptive column layouts based on content
- **Mobile-Friendly**: Responsive design for different screen sizes

### 📊 Advanced Features

#### Intelligent Content Preview
- **Real-time Weight Calculation**: Shows content source percentages before generation
- **Quality Metrics**: Data quality assessment with recommendations
- **Preview Data**: Company data length and content preview

#### Enhanced Progress Monitoring
- **Individual Agent Tracking**: Per-agent status with timing metrics
- **Overall Progress**: Comprehensive progress bar with percentage completion
- **Error Handling**: Detailed error messages with agent-specific information
- **Performance Analytics**: Generation time and success rate tracking

#### Professional Export
- **Tabbed Review**: Organized section review with summary analytics
- **Instant Download**: One-click markdown export with formatted filename
- **Quality Assurance**: Content scoring and agent performance metrics
- **Session Reset**: Easy workflow restart for multiple proposals

### 📚 Documentation Updates
- **Complete UI Guide**: Updated user guide reflecting new step-based workflow
- **Navigation Instructions**: Detailed guidance on using the new interface
- **Advanced Usage**: Tips for optimizing the new workflow features
- **Troubleshooting**: Updated troubleshooting for new UI patterns

### 🚀 Performance Improvements
- **Streamlined Workflow**: More efficient user journey with guided steps
- **Better Error Recovery**: Enhanced error handling with clear user guidance
- **State Management**: Improved session state handling for reliability
- **User Feedback**: Better visual feedback throughout the process

## 2025-08-30 - Major Update: Real Agent Architecture Implementation

### ✅ Implemented Features

#### Real Claude SDK Integration
- **Complete Agent Overhaul**: Replaced placeholder content with actual Claude Code SDK API calls
- **Functional Content Generation**: All 10 agents now generate real, contextual content
- **Enhanced Error Handling**: Robust error recovery with detailed user feedback
- **Proper API Configuration**: Uses claude-3-5-sonnet-20241022 model with optimized parameters

#### Advanced Agent Orchestration
- **Multi-Agent Progress Tracking**: Real-time status monitoring for each specialized agent
- **Performance Metrics**: Individual agent timing and success rate tracking  
- **Enhanced UI**: Agent progress indicators with completion status and duration
- **Agent Status Management**: Pending → In Progress → Completed/Error state tracking

#### Intelligent Content Scoring
- **Dynamic Weight Calculation**: Automatically adjusts content source weights based on data quality
- **Content Quality Assessment**: Evaluates local content relevance (length, keywords, structure)
- **Smart Source Balancing**: Optimizes mix of local content, world knowledge, and online research
- **Transparent Metrics**: Shows exact percentage breakdown of content sources used

#### Enhanced User Experience
- **Real-time Progress Display**: Individual agent status with emoji indicators
- **Performance Summary**: Average generation time and success metrics
- **Enhanced Section Display**: Shows agent performance, duration, and content scoring
- **Better Error Reporting**: Specific error messages with agent-level granularity

#### Online Research Framework
- **Research Integration**: Framework for incorporating online research (placeholder implementation)
- **Content Source Configuration**: Granular control over local, world knowledge, and online sources
- **Future-Ready Architecture**: Prepared for real web API integration

### 🏗️ Architecture Improvements

#### Agent System
- **BaseAgent Enhancement**: Added intelligent content scoring and research capabilities
- **Specialized Agents**: 10 dedicated agents with optimized prompts for each proposal section
- **Progress Tracking**: AgentProgress class with timing, status, and error management
- **Content Quality**: Automatic assessment of local data quality and relevance

#### User Interface
- **Enhanced Layout**: Better organization with progress tracking and metrics
- **Real-time Updates**: Live agent status updates during generation process  
- **Performance Display**: Generation metrics and content source breakdown
- **Professional Presentation**: Improved section formatting and information display

### 📚 Documentation
- **Comprehensive User Guide**: Created detailed documentation at `docs/aws-ai-proposal-generator-guide.md`
- **Usage Instructions**: Step-by-step guide for all app features
- **Troubleshooting Section**: Common issues and solutions
- **Advanced Usage Tips**: Optimization strategies and best practices

### 🔧 Technical Details
- **Claude SDK Integration**: Real API calls replacing all placeholder content
- **Content Processing Pipeline**: Data loading → weight calculation → agent coordination → quality assessment → output formatting
- **Error Recovery**: Graceful handling of API failures with user-friendly messages
- **Performance Optimization**: Intelligent content scoring reduces API calls while maintaining quality

### 🚀 Next Steps for Future Development
- **Real Online Research**: Integration with web search APIs and news sources
- **Enhanced Content Quality**: More sophisticated scoring algorithms
- **Export Options**: PDF, Word, and presentation format support
- **Custom Templates**: User-defined proposal section templates

