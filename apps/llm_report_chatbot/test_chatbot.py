#!/usr/bin/env python3
"""Quick test script for the chatbot"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from apps.llm_report_chatbot.llm_report_chatbot import ReportChatbot

def test_chatbot():
    # Get the report path
    script_dir = Path(__file__).parent.parent.parent
    report_path = script_dir / "projects" / "llm-architectures-on-aws" / "report-03.md"
    
    print("Testing LLM Report Chatbot...")
    print("=" * 50)
    
    try:
        chatbot = ReportChatbot(report_path)
        print(f"✅ Loaded {len(chatbot.chunks)} sections")
        
        # Test questions
        test_questions = [
            "What is SageMaker HyperPod?",
            "What are the benefits of MoE architectures?",
            "How much does training cost with AWS?",
            "What is DeepSeek-V3 architecture?",
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n📝 Test {i}: {question}")
            answer = chatbot.answer(question)
            print("💡 Answer preview:")
            print(answer[:300] + "..." if len(answer) > 300 else answer)
            print("-" * 40)
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_chatbot()