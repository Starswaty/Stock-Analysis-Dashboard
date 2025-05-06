import fitz  # PyMuPDF
from transformers import pipeline
from fpdf import FPDF
import math
import os

# Load summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def chunk_text(text, max_chunk=1024):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chunk:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def summarize_pdf_content(text):
    original_length = len(text.split())
    target_length = max(80, math.ceil(original_length * 0.1))  # At least 80 words
    chunks = chunk_text(text)

    summarized = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=200, min_length=30, do_sample=False)[0]['summary_text']
        summarized.append(summary)

    # Join all chunks and truncate to ~10%
    combined_summary = ' '.join(summarized)
    summary_words = combined_summary.split()
    final_summary = ' '.join(summary_words[:target_length])
    return final_summary.strip()

def save_summary_to_pdf(summary_text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    lines = summary_text.split('. ')
    for line in lines:
        pdf.multi_cell(0, 10, line.strip() + '.')

    pdf.output(output_path)
    print(f"✅ Summary saved to: {output_path}")

def summarize_pdf(input_pdf_path, output_pdf_path):
    print(f"📄 Extracting from: {input_pdf_path}")
    text = extract_text_from_pdf(input_pdf_path)
    print(f"✂️ Summarizing ({len(text.split())} words)...")
    summary = summarize_pdf_content(text)
    save_summary_to_pdf(summary, output_pdf_path)

# Example usage
if __name__ == "__main__":
    input_pdf = "input.pdf"  # Replace with your input file
    output_pdf = "summary_output.pdf"
    
    if not os.path.exists(input_pdf):
        print("❌ Input PDF not found!")
    else:
        summarize_pdf(input_pdf, output_pdf)
