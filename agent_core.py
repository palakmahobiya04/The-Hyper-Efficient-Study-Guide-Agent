from tools import generate_mcq_quiz, extract_flashcards, generate_outline
from datetime import datetime

def format_final_report(quiz_data: QuizOutput, flashcard_data: FlashcardOutput, outline_text: str) -> str:
    """Synthesizes all structured tool outputs into a single Markdown report."""
    
    report = f"# Hyper-Efficient Study Guide: {datetime.now().strftime('%Y-%m-%d')}\n\n"
    report += "--- \n\n"
    
    # 1. Add Quiz Section
    report += "## 🧠 Multiple-Choice Quiz\n"
    for i, q in enumerate(quiz_data.questions):
        report += f"**{i+1}. {q.question}**\n"
        for opt in q.options:
            report += f"- ({opt.key}) {opt.text}\n"
        report += f"**Answer:** ({q.correct_key})\n\n"

    # 2. Add Flashcard Section
    report += "## 🃏 Flashcards (Term: Definition)\n"
    for i, fc in enumerate(flashcard_data.flashcards):
        report += f"**{i+1}. {fc.term}**\n"
        report += f"   > {fc.definition}\n"
    report += "\n"

    # 3. Add Outline Section
    report += "## 🗺️ Hierarchical Outline\n"
    report += outline_text
    report += "\n\n---\n\n*Agent created for the Concierge Agents Capstone Project.*"
    
    return report

def run_study_guide_agent(source_text: str) -> str:
    """
    The main Agent workflow (The Orchestrator).
    It executes tools sequentially and synthesizes the final output.
    """
    print("--- Agent Initiated: Starting Study Guide Generation ---")
    
    # 1. Execute Quiz Tool
    print("1/3: Generating Multiple-Choice Quiz...")
    quiz_output = generate_mcq_quiz(source_text)
    
    # 2. Execute Flashcard Tool
    print("2/3: Extracting Vocabulary Flashcards...")
    flashcard_output = extract_flashcards(source_text)
    
    # 3. Execute Outline Tool
    print("3/3: Creating Hierarchical Outline...")
    outline_text = generate_outline(source_text)
    
    # 4. Synthesize and Format
    if quiz_output and flashcard_output and outline_text:
        final_report = format_final_report(quiz_output, flashcard_output, outline_text)
        print("--- Agent Complete: Report Generated Successfully ---")
        return final_report
    else:
        return "ERROR: Agent failed to receive all structured outputs from the tools."


if __name__ == "__main__":
    # --- DEMO INPUT ---
    SAMPLE_TEXT = """
    Quantum entanglement is a phenomenon that occurs when a pair or group of particles are generated,
    interact, or share spatial proximity in a way that the quantum state of each particle cannot be
    described independently of the others, even when the particles are separated by a large distance. 
    This is often referred to as "spooky action at a distance." Entanglement is a critical resource 
    for quantum computing, enabling quantum communication and quantum cryptography. Superposition is 
    another key concept, stating that a quantum system exists in all its possible states simultaneously.
    A qubit, the basic unit of quantum information, leverages both superposition and entanglement to 
    perform complex computations far beyond the capability of classical bits.
    """
    
    report = run_study_guide_agent(SAMPLE_TEXT)
    
    with open("study_guide_report.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    print("\n--- FINAL REPORT ---")
    print(report)
