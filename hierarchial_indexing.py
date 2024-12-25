import re
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize

# Load Sentence-BERT model for semantic search
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

class HierarchicalIndexer:
    def __init__(self):
        self.tree = {"textbook": {"title": "Sample Textbook", "content": {}}}
        self.index = {}  # Memory-based index
        self.chunk_size = 500  # Maximum size of text chunks
        self.embeddings = {}

    def build_hierarchical_tree(self, text):
        """
        Build a hierarchical structure of content (root -> chapters -> sections -> paragraphs).
        Args:
            text (str): Raw text extracted from a PDF or document.
        """
        chapters = re.split(r'(Chapter \d+)', text)  # Split by chapters
        chapter_id = 1

        for chapter in chapters:
            if f"Chapter {chapter_id}" in chapter:
                chapter_data = {
                    "chapter_id": f"chapter_{chapter_id}",
                    "chapter_title": f"Chapter {chapter_id}",
                    "sections": {}
                }
                sections = re.split(r'(Section \d+\.\d+)', chapter)  # Split by sections
                section_id = 1

                for section in sections:
                    if f"Section {section_id}" in section:
                        section_data = {
                            "section_id": f"section_{chapter_id}_{section_id}",
                            "section_title": f"Section {section_id}",
                            "content": self.chunk_text(section)
                        }
                        chapter_data["sections"][f"section_{chapter_id}_{section_id}"] = section_data
                        section_id += 1

                self.tree["textbook"]["content"][f"chapter_{chapter_id}"] = chapter_data
                chapter_id += 1

    def chunk_text(self, text):
        """
        Split text into manageable chunks of a specified size (e.g., 500 characters).
        Args:
            text (str): Text to chunk.
        Returns:
            list: List of text chunks.
        """
        chunks = [text[i:i + self.chunk_size] for i in range(0, len(text), self.chunk_size)]
        return chunks

    def embed_text(self, text):
        """
        Create embeddings for a list of text chunks.
        Args:
            text (list): List of text chunks.
        Returns:
            list: List of text embeddings.
        """
        embeddings = model.encode(text, convert_to_tensor=True)
        return embeddings

    def build_index(self, text):
        """
        Build a memory-based index by embedding text chunks and associating them with hierarchical nodes.
        Args:
            text (str): Text extracted from the document.
        """
        # First, build the hierarchical tree
        self.build_hierarchical_tree(text)

        # Now, create embeddings for each chunk of text in the tree
        for chapter_key, chapter_data in self.tree["textbook"]["content"].items():
            for section_key, section_data in chapter_data["sections"].items():
                text_chunks = section_data["content"]
                embeddings = self.embed_text(text_chunks)
                self.embeddings[section_key] = embeddings

                # Store the embeddings and text in the memory index
                self.index[section_key] = {
                    "section_title": section_data["section_title"],
                    "embeddings": embeddings
                }

    def retrieve(self, query, top_n=3):
        """
        Retrieve the top N most relevant sections based on the user's query.
        Args:
            query (str): The query text.
            top_n (int): Number of top results to retrieve.
        Returns:
            list: List of top N retrieved sections.
        """
        query_embedding = model.encode([query])[0]
        similarities = []

        # Calculate similarity with each section's embeddings in the index
        for section_key, section_data in self.index.items():
            section_embeddings = section_data["embeddings"]
            similarity_scores = np.inner(query_embedding, section_embeddings)
            max_score_idx = np.argmax(similarity_scores)

            similarities.append({
                "section_key": section_key,
                "section_title": section_data["section_title"],
                "similarity_score": similarity_scores[max_score_idx],
                "content": self.tree["textbook"]["content"][section_key]["sections"][section_key]["content"][max_score_idx]
            })

        # Sort the results by similarity score in descending order and return top_n results
        similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
        return similarities[:top_n]

    def save_index(self, index_path):
        """
        Save the hierarchical index to a file (for persistence).
        Args:
            index_path (str): Path to the file where the index will be saved.
        """
        with open(index_path, 'w') as f:
            json.dump(self.index, f, indent=4)

    def load_index(self, index_path):
        """
        Load the hierarchical index from a file.
        Args:
            index_path (str): Path to the file containing the saved index.
        """
        with open(index_path, 'r') as f:
            self.index = json.load(f)

