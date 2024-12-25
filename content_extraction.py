import os
import re
import PyPDF2
import spacy
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from spacy import displacy
from spacy.matcher import PhraseMatcher

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        str: Extracted text.
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def extract_text_from_pdfs(pdf_paths):
    """
    Extract text from a list of PDF files.
    Args:
        pdf_paths (list): List of PDF file paths.
    Returns:
        dict: Dictionary with file paths and extracted text.
    """
    all_text = {}
    for pdf_path in pdf_paths:
        text = extract_text_from_pdf(pdf_path)
        all_text[pdf_path] = text
    return all_text

def preprocess_text(text):
    """
    Preprocess the extracted text: tokenization, stopword removal, lemmatization, and cleaning.
    Args:
        text (str): Raw text.
    Returns:
        list: Preprocessed text (list of lemmatized words).
    """
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Clean the text
    text = text.lower()  # Lowercase the text
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespaces
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation

    # Tokenize the text into words
    words = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Lemmatize the words
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

    return lemmatized_words

def named_entity_recognition(text):
    """
    Perform Named Entity Recognition (NER) using spaCy.
    Args:
        text (str): Text to extract named entities.
    Returns:
        list: List of extracted named entities.
    """
    # Process the text with spaCy
    doc = nlp(text)
    
    # Extract entities
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    
    return entities

def chunk_text(text, chunk_size=500):
    """
    Chunk large text into smaller chunks.
    Args:
        text (str): Text to chunk.
        chunk_size (int): Size of each chunk (in characters).
    Returns:
        list: List of text chunks.
    """
    # Split the text into manageable chunks
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    return chunks

def extract_keywords(text):
    """
    Extract keywords or important phrases using spaCy's PhraseMatcher.
    Args:
        text (str): Text to extract keywords from.
    Returns:
        list: List of keywords/phrases.
    """
    doc = nlp(text)
    matcher = PhraseMatcher(nlp.vocab)
    
    # Define some important patterns (can be modified)
    patterns = ["machine learning", "deep learning", "artificial intelligence", "data science"]
    pattern_docs = [nlp.make_doc(pattern) for pattern in patterns]
    matcher.add("KEYWORDS", None, *pattern_docs)
    
    matches = matcher(doc)
    keywords = [doc[start:end].text for _, start, end in matches]
    
    return keywords

def extract_and_process_text(pdf_paths):
    """
    Extract and process text from PDFs: clean, preprocess, and perform NLP tasks.
    Args:
        pdf_paths (list): List of PDF file paths.
    Returns:
        dict: Processed text with NLP tasks.
    """
    # Step 1: Extract text from PDFs
    extracted_text = extract_text_from_pdfs(pdf_paths)
    
    # Step 2: Process the extracted text
    processed_text = {}
    
    for file_path, text in extracted_text.items():
        # Preprocess the text
        preprocessed_words = preprocess_text(text)
        
        # Perform NER
        named_entities = named_entity_recognition(text)
        
        # Chunk the text
        text_chunks = chunk_text(text)
        
        # Extract keywords
        keywords = extract_keywords(text)
        
        processed_text[file_path] = {
            'preprocessed_words': preprocessed_words,
            'named_entities': named_entities,
            'text_chunks': text_chunks,
            'keywords': keywords
        }
    
    return processed_text
