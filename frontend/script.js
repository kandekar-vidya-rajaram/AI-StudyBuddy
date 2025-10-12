document.getElementById('generateBtn').addEventListener('click', async () => {
  const fileInput = document.getElementById('fileInput');
  const outputDiv = document.getElementById('output');

  if (!fileInput.files.length) {
    alert('Please upload a PDF first!');
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  outputDiv.textContent = 'Processing... ⏳';

  try {
    const response = await fetch('http://127.0.0.1:5000/summarize', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    outputDiv.textContent = data.result;
  } catch (error) {
    outputDiv.textContent = 'Error: ' + error.message;
  }
});
