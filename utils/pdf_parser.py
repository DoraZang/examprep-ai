import pypdf

def extract_text_from_pdf(uploaded_file):
    """
    Extract text content from an uploaded PDF file.
    uploaded_file: Streamlit file uploader object
    Returns: extracted text as a string
    """
    reader = pypdf.PdfReader(uploaded_file)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    return text.strip()


def chunk_text(text, chunk_size=3000):
    """
    Split long text into smaller chunks to avoid exceeding API token limits.
    chunk_size: approximate number of characters per chunk
    Returns: list of text chunks
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_length += len(word) + 1
        current_chunk.append(word)
        
        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks