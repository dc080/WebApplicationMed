function getCorrectImgType(value) {
    //alert(radioButton.value)
    const request = new XMLHttpRequest()
    if (value === "orig") {
        request.open('GET', '/algorithms/getOrigImg')
    }
    else if (value === "edit") {
        request.open('GET', '/algorithms/getEditImg')
    }
    request.responseType='blob'
    request.send()
    request.addEventListener('load', requestListenerOnLoad)
}

function requestListenerOnLoad() {
    document.getElementById("image").src = URL.createObjectURL(this.response)
}

function applyBorders() {
    const bordersRequest = new XMLHttpRequest()
    bordersRequest.open('POST', '/algorithms/editImage')
    bordersRequest.setRequestHeader('content-type', 'application/json;charset=UTF-8')
    var upperBorder = document.getElementById("upperRangeNumber").value
    var lowerBorder = document.getElementById("lowerRangeNumber").value
    bordersRequest.send(JSON.stringify({"light": upperBorder, "dark": lowerBorder}))
    bordersRequest.addEventListener('load', bordersRequestListenerOnLoad)
}

function bordersRequestListenerOnLoad() {
    document.getElementById("edit").checked = true
    getCorrectImgType("edit")
}

function runAlgo() {
    document.getElementById("runAlgo").disabled = true
    //document.getElementById("applyBorders").disabled = true
    const runRequest = new XMLHttpRequest()
    runRequest.open('POST', '/algorithms/runAlgorithm')
    runRequest.setRequestHeader('content-type', 'application/json;charset=UTF-8')
    var upperBorder = document.getElementById("upperRangeNumber").value
    var lowerBorder = document.getElementById("lowerRangeNumber").value
    runRequest.send(JSON.stringify({"light": upperBorder, "dark": lowerBorder}))
    runRequest.addEventListener('readystatechange', requestListenerOnReadyState)
}

function requestListenerOnReadyState() {
    if (this.readyState==4) {
        //console.log('kekw: ', this.responseText)
        var resp = JSON.parse(this.responseText);
        document.getElementById("Borders").innerHTML = resp['Borders'];
        document.getElementById("fractNumber").innerHTML = resp['fractNumber'];
        document.getElementById("percentSquare").innerHTML = resp['percentSquare'];
        console.log('this.resp: ', resp);
        console.log('this.status: ', this.status);
        document.getElementById("runAlgo").disabled = false
        //document.getElementById("applyBorders").disabled = false
    }
}
