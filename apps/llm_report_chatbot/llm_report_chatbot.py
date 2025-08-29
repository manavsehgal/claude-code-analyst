#!/usr/bin/env python3
"""
Minimalist Q&A Chatbot for LLM Architectures on AWS Report
A simple, functional chatbot that answers questions based on the report content.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ReportChatbot:
    def __init__(self, report_path: str):
        """Initialize the chatbot with the report content."""
        self.report_path = Path(report_path)
        self.chunks = []
        self.chunk_headers = []
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.chunk_vectors = None
        
        self._load_and_process_report()
    
    def _load_and_process_report(self):
        """Load the report and chunk it into sections."""
        if not self.report_path.exists():
            raise FileNotFoundError(f"Report not found: {self.report_path}")
        
        with open(self.report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by headers (##, ###, ####)
        sections = re.split(r'\n(?=#{2,4}\s)', content)
        
        for section in sections:
            if section.strip():
                # Extract header if present
                header_match = re.match(r'^(#{2,4}\s+[^\n]+)', section)
                header = header_match.group(1) if header_match else "Introduction"
                
                # Clean the section text
                text = re.sub(r'^#{2,4}\s+[^\n]+\n', '', section)
                text = text.strip()
                
                if text:
                    self.chunks.append(text)
                    self.chunk_headers.append(header)
        
        # Vectorize all chunks
        if self.chunks:
            self.chunk_vectors = self.vectorizer.fit_transform(self.chunks)
    
    def find_relevant_chunks(self, query: str, top_k: int = 3) -> List[Tuple[str, str, float]]:
        """Find the most relevant chunks for a query."""
        if not self.chunks:
            return []
        
        # Vectorize the query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.chunk_vectors).flatten()
        
        # Get top k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Threshold for relevance
                results.append((
                    self.chunk_headers[idx],
                    self.chunks[idx],
                    similarities[idx]
                ))
        
        return results
    
    def answer(self, question: str) -> str:
        """Generate an answer based on the most relevant chunks."""
        relevant_chunks = self.find_relevant_chunks(question, top_k=3)
        
        if not relevant_chunks:
            return "I couldn't find relevant information in the report to answer your question."
        
        # Build the answer
        answer_parts = []
        
        # Add the most relevant section
        header, content, score = relevant_chunks[0]
        
        # Extract key points from the content
        answer_parts.append(f"Based on the report section '{header}':\n")
        
        # Try to extract specific relevant sentences
        sentences = re.split(r'[.!?]\s+', content)
        relevant_sentences = []
        
        # Simple keyword matching for relevance
        query_words = set(question.lower().split())
        for sentence in sentences[:10]:  # Limit to first 10 sentences
            sentence_words = set(sentence.lower().split())
            if len(query_words & sentence_words) > 0:
                relevant_sentences.append(sentence.strip())
        
        if relevant_sentences:
            answer_parts.append('\n'.join(relevant_sentences[:3]))
        else:
            # Fall back to first few sentences
            answer_parts.append('\n'.join(sentences[:3]))
        
        # Add additional context if other chunks are highly relevant
        if len(relevant_chunks) > 1 and relevant_chunks[1][2] > 0.3:
            answer_parts.append(f"\n\nAdditional information from '{relevant_chunks[1][0]}':")
            sentences = re.split(r'[.!?]\s+', relevant_chunks[1][1])
            answer_parts.append(sentences[0] if sentences else relevant_chunks[1][1][:200])
        
        return '\n'.join(answer_parts)


def main():
    """Main interactive loop for the chatbot."""
    # Get the report path
    script_dir = Path(__file__).parent.parent.parent
    report_path = script_dir / "projects" / "llm-architectures-on-aws" / "report-03.md"
    
    print("🤖 LLM Architectures on AWS - Q&A Chatbot")
    print("=" * 50)
    print("Loading report...")
    
    try:
        chatbot = ReportChatbot(report_path)
        print(f"✅ Loaded {len(chatbot.chunks)} sections from the report")
        print("\nYou can now ask questions about:")
        print("- LLM architectures (GPT, MoE, attention mechanisms)")
        print("- AWS services (SageMaker, HyperPod, EC2, Bedrock)")
        print("- Training and inference optimization")
        print("- Cost and performance considerations")
        print("\nType 'quit' or 'exit' to leave\n")
        
        while True:
            try:
                question = input("📝 Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not question:
                    continue
                
                print("\n🔍 Searching report...")
                answer = chatbot.answer(question)
                print("\n💡 Answer:")
                print("-" * 40)
                print(answer)
                print("-" * 40)
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
                
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()