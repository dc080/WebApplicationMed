window.onload = init;


function init() {
    var isAdvancedUpload = function () {
        var div = document.createElement('div');
        return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
    }();

    var form = document.getElementById("boxForUploadImage");
    var input = document.getElementById("uploadFile");


    if (isAdvancedUpload) {
        form.classList.add('has-advanced-upload');
    }

    var droppedFiles = false;

    form.addEventListener('drag', dragPrevent)
    form.addEventListener('dragstart', dragPrevent) //prevent
    form.addEventListener('dragend', dragLeave)
    form.addEventListener('dragover', dragOver)
    form.addEventListener('dragenter', dragEnter)
    form.addEventListener('dragleave', dragLeave)
    form.addEventListener('drop', dragDrop)

    input.addEventListener('change', inputOnChange)
}

var counter = 0;

function dragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    this.classList.add('is-dragover');
    //console.log("dragOver");
}

function dragEnter(event) {
    event.preventDefault();
    event.stopPropagation();
    this.classList.add('is-dragover');
    counter++;
    //console.log("Enter" + counter);
}

function dragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    counter--;
    if (counter === 0) {
        this.classList.remove('is-dragover');
    }
    //console.log("leave" + counter);
}

function dragPrevent(event) {
    event.preventDefault();
    event.stopPropagation();
    //console.log("Prevent");
}

function dragDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    this.classList.remove('is-dragover');
    counter = 0;
    var droppedFile = event.dataTransfer.files;
    showFile(droppedFile);
    document.getElementById("uploadFile").files = droppedFile;
    /*console.log(droppedFile)*/
}

function inputOnChange(event) {
    showFile(event.target.files)
}

function showFile(file) {
    var label = document.getElementById("label");
    //console.log(file[0].name);
    label.textContent = file[0].name;
}
