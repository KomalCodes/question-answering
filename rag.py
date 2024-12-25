import openai
from retrieval import HierarchicalIndexer  # Import the retrieval process from the retrieval.py file

# Set your OpenAI API Key
openai.api_key = "not entering my own api key as it is personal. please use your own."

# Function to generate the answer using GPT-3, augmented by the retrieved content
def generate_answer_with_llm(retrieved_content, query):
    """
    Generate an answer using OpenAI's GPT-3 model, augmented by the retrieved content.
    Args:
        retrieved_content (list): The content retrieved from the index.
        query (str): The user's question.
    Returns:
        str: The generated answer.
    """
    # Combine the retrieved content into a single context
    context = " ".join([content['content'] for content in retrieved_content])  # Concatenate the content
    prompt = f"Answer the following question based on the given content:\n\nContent: {context}\n\nQuestion: {query}\nAnswer:"
    
    # Make a request to OpenAI API to generate the answer
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the appropriate model
        prompt=prompt,
        max_tokens=150,  # Limit response length
        temperature=0.7   # Adjust creativity of the answer
    )
    
    # Return the generated answer
    return response.choices[0].text.strip()


