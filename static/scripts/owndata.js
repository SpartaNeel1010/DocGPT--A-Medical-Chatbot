

dropzone=document.getElementsByClassName('dropzone')[0]
fileInput=document.getElementById('files')
fileList = document.getElementById('filelist');
// document.getElementsByTagName('div')[0].setAttribute('style','display:none;')

dropzone.addEventListener('dragover', function(e) {
    e.preventDefault();
    dropzone.style.backgroundColor = '#212121';
});
dropzone.addEventListener('dragleave', function(e) {
    e.preventDefault();
    dropzone.style.backgroundColor = '#171717';
});
dropzone.addEventListener('drop', function(e) {
    e.preventDefault();
    dropzone.style.backgroundColor = '#171717';
    dropzone.getElementsByTagName('img')[0].setAttribute('style','display:none;')
    dropzone.getElementsByTagName('h2')[0].setAttribute('style','display:none;')
    

    var files = e.dataTransfer.files;
    console.log(files)
    fileInput.files = files;
    updateFileList(files);
});
document.getElementById('uploadform').addEventListener('submit',(e)=>{
    // e.preventDefault();
    console.log(fileInput.files)
    
})

dropzone.addEventListener('click', function() {
    fileInput.click();
});

fileInput.addEventListener('change', function() {
    // e.preventDefault();
    
    dropzone.getElementsByTagName('img')[0].setAttribute('style','display:none;')
    dropzone.getElementsByTagName('h2')[0].setAttribute('style','display:none;')

    // var files = e.dataTransfer.files;
    files=fileInput.files;
    updateFileList(files);
    
});

function updateFileList(files) {
    fileList.innerHTML = '';
    fileList.setAttribute('style','display:flex;')
    for (var i = 0; i < files.length; i++) {
        var listItem = document.createElement('div');

        listItem.setAttribute('style',`
            background-color: #212121;
            color: white;
            border-radius: 15px;
            padding:10px 20px;
            margin:10px;
            width:50%;
        `)
        listItem.textContent = files[i].name;
        fileList.appendChild(listItem);
    }
}