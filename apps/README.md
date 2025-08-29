# Applications

This folder contains standalone applications built as part of the Claude Code Analyst project. Each application lives in its own subfolder with its own documentation and dependencies.

## Structure

Each app should have its own subfolder containing:
- Main application file(s)
- App-specific README.md with usage instructions
- Test files (if applicable)
- Configuration files (if needed)
- `__init__.py` for Python package structure

## Available Applications

### 1. llm_report_chatbot
A minimalist Q&A chatbot for the LLM Architectures on AWS report. Uses TF-IDF text search to find relevant information and answer questions about AWS services, LLM architectures, and optimization strategies.

**Usage:**
```bash
uv run python apps/llm_report_chatbot/llm_report_chatbot.py
```

See [llm_report_chatbot/README.md](llm_report_chatbot/README.md) for detailed documentation.

## Creating New Applications

When adding a new application:
1. Create a new subfolder under `apps/` with a descriptive name
2. Include a README.md with usage instructions and features
3. Add an `__init__.py` file to make it a Python package
4. Update this main README to list the new application
5. Ensure all paths are relative to the project root