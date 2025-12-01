import os
import json
from typing import Type
from pydantic import BaseModel
from openai import OpenAI # Using OpenAI as a generic LLM client

from schemas import QuizOutput, FlashcardOutput, OutlineOutput

# IMPORTANT: Replace with your chosen LLM client/integration (e.g., Gemini, Anthropic, or LangChain Runnable)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 
MODEL_NAME = "gpt-4o-mini" # A powerful and efficient model for structured output

def call_llm_with_structure(
    prompt: str,
    output_schema: Type[BaseModel]
) -> BaseModel:
    """Generic function to call the LLM and enforce structured Pydantic output."""
    
    # This is a conceptual example of a structured call. 
    # Actual implementation depends on your LLM client (e.g., LangChain's .with_structured_output())
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a content transformation engine. Output ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_model=output_schema, # Key feature for structured output
        )
        return response # In a real implementation, this would be the validated Pydantic object
    except Exception as e:
        print(f"LLM Tool Error: {e}")
        # In a real agent, you would implement a retry loop here
        return None

# --- Specialized Tools ---

def generate_mcq_quiz(source_text: str) -> QuizOutput:
    """Tool to generate a quiz with 10 questions."""
    prompt = f"""
    Analyze the following text and generate exactly 10 unique, challenging multiple-choice questions 
    suitable for advanced students. Provide 4 options for each question (A, B, C, D).

    Source Text: \"\"\"{source_text[:2000]}\"\"\"
    """
    return call_llm_with_structure(prompt, QuizOutput)

def extract_flashcards(source_text: str) -> FlashcardOutput:
    """Tool to extract 20 term and definition flashcards."""
    prompt = f"""
    Analyze the following text and extract exactly 20 of the most important concepts and their
    precise definitions. The definition must be directly relevant to the source text.

    Source Text: \"\"\"{source_text[:2000]}\"\"\"
    """
    return call_llm_with_structure(prompt, FlashcardOutput)

def generate_outline(source_text: str) -> str:
    """Tool to generate a hierarchical outline (output as Markdown text)."""
    # This one focuses on text output for simpler Markdown formatting
    prompt = f"""
    Analyze the following text. Generate a comprehensive, hierarchical 3-level outline 
    using Markdown formatting (e.g., # Main Topic, ## Sub-Topic, - Detail). 
    Do not exceed 300 words.

    Source Text: \"\"\"{source_text}\"\"\"
    """
    
    # Use a simpler text completion call for Markdown
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
