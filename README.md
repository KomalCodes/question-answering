 **Question Answering System**

 **Project Overview**

This **Question Answering System** leverages **Retrieval-Augmented Generation (RAG)**, integrating advanced **semantic search** with **GPT-3** to provide context-aware answers to user queries based on the content of **uploaded textbooks** (in PDF format). 

The system performs the following tasks:
- **Extract content** from uploaded PDF textbooks.
- **Index the content** hierarchically (chapters, sections, paragraphs).
- **Retrieve relevant content** based on user queries.
- **Generate answers** using **GPT-3**, augmented by the retrieved content.

 **Features**
- Upload and process **three PDF textbooks**.
- Extract and process text using **PyPDF2** and advanced **NLP techniques**.
- Build a **hierarchical tree** structure of textbooks for efficient content retrieval.
- Retrieve the most **relevant sections** based on the user’s query using **semantic search**.
- **Answer generation** powered by **GPT-3** to provide context-aware, detailed answers.

 **Technologies Used**
- **Python 3.x** (for the backend)
- **Flask** (for the web framework)
- **Sentence-BERT** (for semantic embeddings)
- **OpenAI GPT-3** (for answer generation)
- **spaCy** (for Named Entity Recognition)
- **PyPDF2** (for PDF text extraction)
- **NLTK** (for text preprocessing)
  
 **Table of Contents**
1. [Installation Instructions](#installation-instructions)
2. [Setup Guide](#setup-guide)
3. [Dependencies](#dependencies)
4. [Usage Instructions](#usage-instructions)
5. [Textbook Information](#textbook-information)
6. [Accessing the User Interface](#accessing-the-user-interface)

 **1. Installation Instructions**

Follow the steps below to set up and run the **Question Answering System** on your local machine.

### **1.1. Prerequisites**
Make sure you have the following installed:
- **Python 3.7 or later**.
- **Pip** (Python package manager).
- **Git** (for cloning the repository).

### **1.2. Clone the Repository**
Clone the repository to your local machine:

### **1.3. Set Up a Virtual Environment**
It is recommended to create a virtual environment to manage the dependencies for this project:

### **1.4. Install Dependencies**
Once the virtual environment is activated, install the required dependencies:
```bash
pip install -r requirements.txt
```

Alternatively, you can manually install the necessary packages:
```bash
pip install flask sentence-transformers openai nltk spacy PyPDF2
```

 **1.5. Install spaCy Model**
You need to install a pre-trained **spaCy** model for **Named Entity Recognition (NER)**:
```bash
python -m spacy download en_core_web_sm
```

 **1.6. Set Up OpenAI API Key**
To use **GPT-3** for answer generation, you need an **OpenAI API key**. If you don't have one, sign up at [OpenAI's API Platform](https://platform.openai.com/signup).

Once you have your API key, set it as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```
For Windows:
```bash
set OPENAI_API_KEY="your-api-key-here"
```

Alternatively, you can directly set the key in the **`rag.py`** file in the following way:
```python
openai.api_key = "your-api-key-here"
```

 **2. Setup Guide**

 **2.1. Folder Structure**
The folder structure should be like this:
```
/your_project_directory
    /uploads                    # Folder to store uploaded PDFs
    /templates                  # For storing HTML templates
    /static                     # For storing static files like CSS and JS
    app.py                      # Flask app
    retrieval.py                # Retrieval-related code
    rag.py                      # RAG-related code
    content_extraction.py       # For extracting text from PDFs
    hierarchical_indexing.py    # For creating hierarchical structure
    style.css                   # CSS styles
    script.js                   # Frontend JS
    index.html                  # HTML file
```

 **2.2. Running the Flask Application**
To start the **Flask** web server, run:
```bash
python app.py
```
 You can access the web interface in your browser.

---

**3. Dependencies**

**3.1. Required Python Libraries**
Here’s a list of the main Python libraries used in this project:

- **Flask**: Web framework used to build the application.
- **Sentence-Transformers**: For embedding text using **Sentence-BERT** to enable semantic search.
- **OpenAI**: Used for accessing the **GPT-3** API to generate answers.
- **NLTK**: For text preprocessing, tokenization, and stopwords removal.
- **spaCy**: For performing **Named Entity Recognition (NER)**.
- **PyPDF2**: To extract text content from PDF files.

**4. Usage Instructions**

 **4.1. Uploading PDF Files**
1. **Go to the homepage**.
2. **Click on the upload section** to choose **three PDF textbooks**.
3. After selecting, the system will process and extract text from the uploaded PDFs.

**4.2. Asking Questions**
1. After uploading the textbooks, **type a question** in the input box.
2. Click on the **"Ask"** button to submit the query.
3. The system will **retrieve relevant content** from the textbooks and generate an answer using **GPT-3**.

**4.3. Answer Generation**
Once you click on the **Ask** button:
- The system will perform **semantic search** using **Sentence-BERT** to find relevant content from the textbooks.
- The retrieved content will be passed to **GPT-3** for **answer generation**.
- The system will display the answer along with the **relevant sections** used for generating the answer.

---

## **5. Textbook Information**

Here are the selected textbooks used in the system:

1. **Textbook 1:** 
Data Science and Machine Learning Mathematical and Statistical Methods by Dirk P. Kroese, Zdravko I. Botev, Thomas Taimre, Radislav Vaisman
2. **Textbook 2:** 
The Data Science Handbook by Wiley
3. **Textbook 3:** 
Data Science & Big Data Analytics Discovering, Analyzing, Visualizing and Presenting Data by Wiley

 **6. Accessing the User Interface**

 **6.1. Navigating the UI**
1. **Homepage**:
   - Contains the **file upload section** to upload the three PDFs.
   - Input box to **ask a question** related to the content of the uploaded PDFs.

2. **File Upload Section**:
   - You can **select three PDFs** at once.
   - The system will process and index the content of the PDFs.

3. **Query Section**:
   - Once the PDFs are indexed, type your **question** and click the **"Ask"** button.
   - The system will process your query and return an answer.

4. **Answer Display**:
   - The answer generated by **GPT-3** will be displayed in this section.
