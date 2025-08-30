You are an expert at Streamlit app development and Claude Code SDK. You are building a single page app apps/proposal.py in Streamit based on the following specification. Think harder to build this app as an agent based system.

Use Claude Code SDK https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python effectively for LLM agent capabilities.

Learn about building effective agents by reading markdown/building-effective-ai-agents-anthropic/article.md article.

The app helps user generate a proposal matching customer needs with AWS AI offerings.
Information about AWS AI offerings is available in projects/llm-architectures-on-aws/report-03.md file.

List customers available in customers/ folder for the user to select one to target the proposal.

User can then select one or many of the proposal sections:
- Executive Summary: What is the elevator pitch and summary of the rest of the document?
- Problem Statement: What are the problems, pain points, explicit asks, and latent needs of the customer?
- Industry Trends: Which industry trends are relevant for the customer growth?
- Competition: What are competitors doing which may need a response from the customer?
- Market Segments: Which market segments is the customer serving and what are the opportunity gaps to address these markets?
- Technology Strategy: What are the technologies customer is using or developing and what is their strategy?
- AWS AI Services: Which AWS AI services match customer's needs and why?
- Adoption Plan: What is the recommended timeline for customer to adopt AWS AI services based on their needs and external factors (industry, competition, markets)?
- Spend: Analyze AWS AI services public pricing, predict usage volume based on customer needs, propose monthly and annual spend.
- Returns: Create a plan for spend vs returns to illustrate when the customer is able to break-even on their AWS spend.

Add check boxes to only use local content (customers/ folder content), use LLM world knowledge, use online research to create the proposal content.

When writing the proposal sections add a score to each section based on extent to which content from customers/ folder was used vs your world knowledge vs online research. Something like Content score: 80% local content, 10% world knowledge, 10% online research.

Create the most optiminal agent/subagent strategy to generate the proposal. Based on the selected proposal sections create subagents to write content for these sections. Create a progress indicator UI to show progress of each subagent. Compile the sections, format the proposal, and save it in the proposals/customer-name/proposal-yyyy-mm-dd.md file.

IMPORTANT: These instructions may be revised and rerun to update existing app. Note incremental changes in changelog.

# Changelog

