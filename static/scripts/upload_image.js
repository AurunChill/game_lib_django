document.getElementById('file-upload').addEventListener('dragover', e => {
    e.preventDefault();
    console.log('drag over');
});

document.getElementById('file-upload').addEventListener('dragleave', e => {
    e.preventDefault();
    console.log('drag leave');
});

document.getElementById('file-upload').addEventListener('drop', e => {
    e.preventDefault(); // This is crucial for drop to work
    console.log('drop');
    let file = e.dataTransfer.files[0];
    displayPreview(file);
});

document.getElementById('file-upload').addEventListener('change', e => {
    console.log('change')
    let file = e.target.files[0];
    displayPreview(file);
});

function displayPreview(file) {
    console.log('display preview')
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
        let preview = document.getElementById('preview');
        preview.src = reader.result;
    };
} 