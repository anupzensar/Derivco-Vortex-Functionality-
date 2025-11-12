#!/usr/bin/env python3
"""
Test script to check Azure OpenAI connection
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.llm_service import test_llm_connection, is_llm_available

def main():
    print("Testing Azure OpenAI connection...")
    
    if not is_llm_available():
        print("❌ LLM client is not available")
        return
    
    print("✅ LLM client is initialized")
    
    if test_llm_connection():
        print("✅ Azure OpenAI connection successful!")
    else:
        print("❌ Azure OpenAI connection failed!")

if __name__ == "__main__":
    main()