# LLM Report Q&A Chatbot

A minimalist chatbot for answering questions about the LLM Architectures on AWS report.

## Usage

Run the chatbot from project root:
```bash
uv run python apps/llm_report_chatbot/llm_report_chatbot.py
```

Or make it executable:
```bash
./apps/llm_report_chatbot/llm_report_chatbot.py
```

## Features
- Simple text-based Q&A interface
- Searches through report sections to find relevant information
- Returns context-aware answers based on report content
- Covers topics: LLM architectures, AWS services, training/inference optimization, costs

## Example Questions
- What is SageMaker HyperPod?
- What are the benefits of MoE architectures?
- How much does training cost with AWS?
- What is DeepSeek-V3 architecture?
- What are the key innovations in modern LLM architectures?
- How does Amazon Bedrock work?
- What instance types are best for LLM training?

Type 'quit' or 'exit' to leave the chatbot.