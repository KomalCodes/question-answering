document.getElementById('askButton').addEventListener('click', function() {
    const query = document.getElementById('userQuery').value;
    const fileInput = document.getElementById('pdfUpload');
    
    
    if (!fileInput.files.length || fileInput.files.length !== 3 || !query) {
        alert('Please upload exactly 3 PDF files and type your question.');
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < fileInput.files.length; i++) {
        formData.append('pdf_files', fileInput.files[i]);
    }

    
    let fileNames = '';
    for (let i = 0; i < fileInput.files.length; i++) {
        fileNames += `<p>${fileInput.files[i].name}</p>`;
    }
    document.getElementById('fileNames').innerHTML = `Uploaded Files: ${fileNames}`;

    
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('answer').textContent = data.answer;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error processing the request.');
    });
});
