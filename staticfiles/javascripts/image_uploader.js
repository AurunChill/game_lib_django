let file_uploader = document.getElementById('image')
console.log(file_uploader)

file_uploader.addEventListener('dragover', e => {
    e.preventDefault();
    console.log('drag over');
});

file_uploader.addEventListener('dragleave', e => {
    e.preventDefault();
    console.log('drag leave');
});

file_uploader.addEventListener('drop', e => {
    e.preventDefault(); // This is crucial for drop to work
    console.log('drop');
    let file = e.dataTransfer.files[0];
    displayPreview(file);
});

file_uploader.addEventListener('change', e => {
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