from pydantic import BaseModel, Field
from typing import List

# --------------------------
# 1. QUIZ SCHEMA
# --------------------------
class MultipleChoiceOption(BaseModel):
    """A single option for an MCQ."""
    key: str = Field(description="The letter label (A, B, C, or D).")
    text: str = Field(description="The full text of the option.")

class MultipleChoiceQuestion(BaseModel):
    """A single multiple-choice question."""
    question: str = Field(description="The question text derived from the source material.")
    options: List[MultipleChoiceOption]
    correct_key: str = Field(description="The key (A, B, C, or D) for the correct answer.")

class QuizOutput(BaseModel):
    """The full structured output for the quiz tool."""
    questions: List[MultipleChoiceQuestion] = Field(description="A list of 10 unique, non-trivial MCQs.")

# --------------------------
# 2. FLASHCARD SCHEMA
# --------------------------
class Flashcard(BaseModel):
    """A single term and its definition."""
    term: str = Field(description="The key term or concept.")
    definition: str = Field(description="The precise definition derived from the source text.")

class FlashcardOutput(BaseModel):
    """The full structured output for the flashcard tool."""
    flashcards: List[Flashcard] = Field(description="A list of 20 essential flashcards.")

# --------------------------
# 3. OUTLINE SCHEMA (Simpler)
# --------------------------
# For simplicity, the outline is often generated as simple structured text/Markdown,
# but can also be structured with Pydantic for high complexity.
class OutlineSection(BaseModel):
    """A section of the outline with nested concepts."""
    title: str
    concepts: List[str]

class OutlineOutput(BaseModel):
    """The high-level output for the outline tool."""
    major_sections: List[OutlineSection]
